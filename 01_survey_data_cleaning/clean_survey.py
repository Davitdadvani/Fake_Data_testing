"""
Clean the fake raw survey export step by step and log what was removed.

Run order:
    python 01_survey_data_cleaning/generate_fake_survey.py
    python 01_survey_data_cleaning/clean_survey.py

Outputs:
    data/clean_survey.csv                         cleaned dataset
    01_survey_data_cleaning/cleaning_report.md    step-by-step log
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_survey.csv"
CLEAN = ROOT / "data" / "clean_survey.csv"
REPORT = Path(__file__).resolve().parent / "cleaning_report.md"

DC = [f"dc{k}" for k in range(1, 5)]
BURDEN = [f"burden{k}" for k in range(1, 5)]
LIKERT = DC + BURDEN

# Thresholds (document and justify these in a real study)
MIN_DURATION_SEC = 120      # faster than this is implausible for the questionnaire
MIN_AGE, MAX_AGE = 18, 70
ATTENTION_CORRECT = 4       # item said: "select 'Agree' (4)"

log = []  # (step, rows_removed, rows_remaining)


def step(df, name, keep_mask):
    removed = int((~keep_mask).sum())
    out = df[keep_mask].copy()
    log.append((name, removed, len(out)))
    return out


df = pd.read_csv(RAW)
log.append(("Raw export", 0, len(df)))

# 1. Exact duplicate submissions
df = step(df, "Remove duplicate submissions", ~df.duplicated(keep="first"))

# 2. No consent
df = step(df, "Remove respondents without consent", df["consent"].eq("Yes"))

# 3. Invalid values -> set to NaN first (they are errors, not real answers)
for col in LIKERT:
    df.loc[~df[col].between(1, 5), col] = np.nan
df.loc[~df["age"].between(MIN_AGE, MAX_AGE), "age"] = np.nan

# 4. Speeders
df = step(df, f"Remove speeders (< {MIN_DURATION_SEC}s)",
          df["duration_seconds"] >= MIN_DURATION_SEC)

# 5. Failed attention check
df = step(df, "Remove failed attention check",
          df["attention_check"].eq(ATTENTION_CORRECT))

# 6. Straightliners: zero variance across all Likert items
straight = df[LIKERT].std(axis=1, skipna=True).eq(0)
df = step(df, "Remove straightliners", ~straight)

# 7. Too many missing answers (> 25% of scale items)
too_missing = df[LIKERT].isna().mean(axis=1) > 0.25
df = step(df, "Remove respondents with > 25% missing scale items", ~too_missing)

# 8. Handle remaining missing values
n_missing_before = int(df[LIKERT].isna().sum().sum())
# Scale scores are computed with skipna=True, i.e. a respondent is scored on the
# items they did answer (fine when few items are missing).
df["digital_competence"] = df[DC].mean(axis=1, skipna=True).round(2)
df["burden"] = df[BURDEN].mean(axis=1, skipna=True).round(2)

# 9. Tidy types / categories
df["gender"] = df["gender"].fillna("Not stated")
df["sector"] = df["sector"].fillna("Not stated")
df = df.drop(columns=["consent", "attention_check"])

CLEAN.parent.mkdir(exist_ok=True)
df.to_csv(CLEAN, index=False)

# ---- report ------------------------------------------------------------
lines = ["# Cleaning report (fake data)\n",
         "| Step | Rows removed | Rows remaining |", "|---|---:|---:|"]
lines += [f"| {n} | {r} | {k} |" for n, r, k in log]
lines += ["",
          f"- Scale items still missing after cleaning: **{n_missing_before}** "
          "(handled by averaging over answered items)",
          f"- Final sample: **{len(df)}** respondents "
          f"({len(df) / log[0][2]:.0%} of the raw rows)",
          "- Invalid values (Likert outside 1-5, age outside "
          f"{MIN_AGE}-{MAX_AGE}) were set to missing, not silently kept."]
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
