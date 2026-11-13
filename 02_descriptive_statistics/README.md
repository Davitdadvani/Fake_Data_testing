# 02 - Descriptive statistics

First analysis of the cleaned fake survey (`data/clean_survey.csv`).

## What `descriptive_analysis.py` does

1. **Sample description:** age, experience, gender and sector distribution
2. **Scale reliability:** Cronbach's alpha for both four-item scales
3. **Descriptives:** mean, SD, min, max and skew of the main variables
4. **Group comparison:** mean burden by sector and a one-way ANOVA
5. **Association:** Pearson and Spearman correlation between digital competence and burden
6. **Charts:** histogram, boxplot by sector, scatter plot with trend line

## Output

- [`results.md`](results.md): all tables, regenerated on every run
- `charts/*.png`: created locally when the script runs

## How to read the results

- Cronbach's alpha around .70 is usually considered acceptable for short scales.
- The correlation between competence and burden (r around .29) exists because the
  generator was written that way. Finding it only shows the code recovers a known
  relationship, which is a useful sanity check for the pipeline.
- No sector differences were built in, and the ANOVA correctly finds none.

## Caveats

- Correlation does not show cause. In a real study, competence could lead to more
  burden, or the reverse, or a third factor could drive both.
- With real data I would also check normality, outliers and effect sizes, and
  report confidence intervals, not only p-values.
