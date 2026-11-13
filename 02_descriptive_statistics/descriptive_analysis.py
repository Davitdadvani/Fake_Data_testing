"""
Descriptive and first inferential statistics on the cleaned fake survey.

Run after the cleaning script:
    python 02_descriptive_statistics/descriptive_analysis.py

Outputs:
    02_descriptive_statistics/results.md   tables in Markdown
    02_descriptive_statistics/charts/*.png (histogram, boxplot, scatter)
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "data" / "clean_survey.csv")

DC = [f"dc{k}" for k in range(1, 5)]
BURDEN = [f"burden{k}" for k in range(1, 5)]


def cronbach_alpha(items: pd.DataFrame) -> float:
    items = items.dropna()
    k = items.shape[1]
    item_var = items.var(axis=0, ddof=1).sum()
    total_var = items.sum(axis=1).var(ddof=1)
    return k / (k - 1) * (1 - item_var / total_var)


out = ["# Results on the fake dataset\n",
       f"Sample size after cleaning: **N = {len(df)}**\n"]

# 1. Sample description
out.append("## Sample description\n")
out.append(f"- Age: M = {df.age.mean():.1f}, SD = {df.age.std():.1f}, "
           f"range {df.age.min():.0f}-{df.age.max():.0f}")
out.append(f"- Years of experience: M = {df.years_experience.mean():.1f}, "
           f"SD = {df.years_experience.std():.1f}\n")
out.append("**Gender (%)**\n")
out.append(df.gender.value_counts(normalize=True).mul(100).round(1)
           .rename("%").to_frame().to_markdown() + "\n")
out.append("**Sector (n)**\n")
out.append(df.sector.value_counts().rename("n").to_frame().to_markdown() + "\n")

# 2. Scale reliability
out.append("## Scale reliability (Cronbach's alpha)\n")
out.append(f"- Digital competence (4 items): alpha = {cronbach_alpha(df[DC]):.2f}")
out.append(f"- Burden (4 items): alpha = {cronbach_alpha(df[BURDEN]):.2f}\n")

# 3. Descriptives of the main variables
main = ["digital_competence", "burden", "help_requests_per_week"]
desc = df[main].agg(["count", "mean", "std", "min", "max", "skew"]).T.round(2)
out.append("## Descriptive statistics of main variables\n")
out.append(desc.to_markdown() + "\n")

# 4. Group comparison by sector
out.append("## Mean burden by sector (excluding \"Not stated\")\n")
known_sector = df[df.sector != "Not stated"]  # drop tiny "Not stated" group
by_sector = (known_sector.groupby("sector")["burden"]
             .agg(["count", "mean", "std"]).round(2).sort_values("mean", ascending=False))
out.append(by_sector.to_markdown() + "\n")
groups = [g["burden"].dropna() for _, g in known_sector.groupby("sector")]
f_val, p_val = stats.f_oneway(*groups)
out.append(f"One-way ANOVA across sectors: F = {f_val:.2f}, p = {p_val:.3f}\n")

# 5. Correlation
out.append("## Correlation: digital competence and burden\n")
valid = df[["digital_competence", "burden"]].dropna()
r, p = stats.pearsonr(valid.digital_competence, valid.burden)
rho, p_s = stats.spearmanr(valid.digital_competence, valid.burden)
out.append(f"- Pearson r = {r:.2f}, p = {p:.3g}")
out.append(f"- Spearman rho = {rho:.2f}, p = {p_s:.3g}\n")
out.append("**Caution:** this is synthetic data, so the relationship was built into "
           "the generator. A real study would need to check assumptions, "
           "report effect sizes and avoid causal claims from correlations.\n")

(HERE / "results.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))

# 6. Charts
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    charts = HERE / "charts"
    charts.mkdir(exist_ok=True)

    plt.figure(figsize=(6, 4))
    plt.hist(df.burden.dropna(), bins=15, edgecolor="black")
    plt.xlabel("Burden score (1-5)")
    plt.ylabel("Respondents")
    plt.title("Distribution of burden (fake data)")
    plt.tight_layout()
    plt.savefig(charts / "burden_histogram.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 4))
    order = list(by_sector.index)
    plt.boxplot([df.loc[df.sector == s, "burden"].dropna() for s in order],
                tick_labels=order)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Burden score")
    plt.title("Burden by sector (fake data)")
    plt.tight_layout()
    plt.savefig(charts / "burden_by_sector.png", dpi=150)
    plt.close()

    plt.figure(figsize=(5, 4))
    plt.scatter(valid.digital_competence, valid.burden, alpha=.4)
    m, b = np.polyfit(valid.digital_competence, valid.burden, 1)
    xs = np.linspace(valid.digital_competence.min(), valid.digital_competence.max(), 50)
    plt.plot(xs, m * xs + b, color="red")
    plt.xlabel("Digital competence")
    plt.ylabel("Burden")
    plt.title("Competence vs burden (fake data)")
    plt.tight_layout()
    plt.savefig(charts / "competence_vs_burden.png", dpi=150)
    plt.close()
except ImportError:
    print("matplotlib not installed - skipped charts")
