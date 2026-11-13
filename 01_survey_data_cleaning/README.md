# 01 - Survey data cleaning

Turns a messy raw survey export into an analysis-ready dataset, and logs what was
removed at each step.

## Scripts

| Script | Purpose |
|---|---|
| `generate_fake_survey.py` | Creates `data/raw_survey.csv` (515 rows, seed 42) with deliberately injected problems |
| `clean_survey.py` | Cleans it and writes `data/clean_survey.csv` plus `cleaning_report.md` |

## Problems injected into the fake data

| Problem | How it is handled |
|---|---|
| Duplicate submissions | Keep the first, drop the rest |
| No consent | Remove the respondent |
| Impossible values (Likert 0, 6, 99; age 4, 150, 999) | Set to missing rather than keep or guess |
| Speeders (under 120 s) | Remove |
| Failed attention check | Remove |
| Straightliners (identical answer on all 8 items) | Remove |
| Many missing scale items (over 25%) | Remove (no one met this rule in this dataset) |
| Few missing items | Compute scale scores over answered items |

## Result

Run `clean_survey.py` and read [`cleaning_report.md`](cleaning_report.md) for the
exact counts. Of 515 raw rows, 427 remain (83%).

## Design decisions worth noting

- **Order matters.** Duplicates and consent are removed first, then invalid values
  are set to missing before the quality filters, so errors do not count as answers.
- **Every step is logged**, so the cleaning can be reported in a methods section.
- **Exclusion rules should be fixed before looking at results.** Here they are
  constants at the top of the script, so changing them is visible and deliberate.
