"""
Generate a FAKE (synthetic) online-survey dataset that looks like a raw export
from a survey platform, including typical data-quality problems.

Nothing here is real participant data. The dataset exists only so that the
cleaning and analysis code in this repository can be practised and tested.

Injected problems (so the cleaning script has something to find):
  - duplicate submissions
  - missing values
  - "speeders" (finished far too quickly)
  - "straightliners" (same answer on every Likert item)
  - failed attention checks
  - missing consent
  - out-of-range Likert values and impossible ages
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_VALID = 500          # roughly the sample size of a typical online study
OUT = Path(__file__).resolve().parents[1] / "data" / "raw_survey.csv"

rng = np.random.default_rng(SEED)

SECTORS = ["IT & Software", "Healthcare", "Education", "Finance",
           "Retail", "Manufacturing", "Public Sector"]
GENDERS = ["Female", "Male", "Non-binary", "Prefer not to say"]


def likert(latent, noise=0.9):
    """Turn a latent score into a 1-5 Likert response."""
    raw = latent + rng.normal(0, noise)
    return int(np.clip(np.round(raw), 1, 5))


rows = []
for i in range(N_VALID):
    dc_latent = rng.normal(3.4, 0.8)                       # digital competence
    burden_latent = 1.6 + 0.35 * dc_latent + rng.normal(0, 0.7)  # weak link to burden
    sector = rng.choice(SECTORS, p=[.22, .15, .12, .14, .13, .12, .12])
    row = {
        "respondent_id": f"R{i + 1:04d}",
        "consent": "Yes",
        "age": int(np.clip(rng.normal(36, 10), 19, 66)),
        "gender": rng.choice(GENDERS, p=[.49, .47, .02, .02]),
        "sector": sector,
        "years_experience": int(np.clip(rng.normal(10, 7), 0, 40)),
        "duration_seconds": int(np.clip(rng.normal(420, 120), 150, 1200)),
        "help_requests_per_week": int(np.clip(rng.poisson(max(0.2, 2 + 1.2 * (dc_latent - 3))), 0, 30)),
    }
    for k in range(1, 5):
        row[f"dc{k}"] = likert(dc_latent)
    for k in range(1, 5):
        row[f"burden{k}"] = likert(burden_latent)
    row["attention_check"] = 4  # instructed response: "select 'Agree' (4)"
    rows.append(row)

df = pd.DataFrame(rows)

# ---- inject data-quality problems --------------------------------------
likert_cols = [f"dc{k}" for k in range(1, 5)] + [f"burden{k}" for k in range(1, 5)]


def pick(n):
    return rng.choice(df.index, size=n, replace=False)


speed_idx = pick(25)
df.loc[speed_idx, "duration_seconds"] = rng.integers(40, 110, size=25)

straight_idx = pick(20)
for idx in straight_idx:
    df.loc[idx, likert_cols] = int(rng.integers(1, 6))

fail_idx = pick(22)
df.loc[fail_idx, "attention_check"] = rng.choice([1, 2, 3, 5], size=22)

df.loc[pick(10), "consent"] = "No"

for col in rng.choice(likert_cols + ["age", "gender", "sector"], size=14):
    df.loc[pick(3), col] = np.nan

df.loc[pick(6), "dc1"] = rng.choice([0, 6, 7, 99], size=6)
df.loc[pick(4), "age"] = rng.choice([4, 12, 150, 999], size=4)

dupes = df.sample(15, random_state=SEED)
df = pd.concat([df, dupes], ignore_index=True)

df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

OUT.parent.mkdir(exist_ok=True)
df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} raw rows to {OUT}")
