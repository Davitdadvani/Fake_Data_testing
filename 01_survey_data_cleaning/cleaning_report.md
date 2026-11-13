# Cleaning report (fake data)

| Step | Rows removed | Rows remaining |
|---|---:|---:|
| Raw export | 0 | 515 |
| Remove duplicate submissions | 15 | 500 |
| Remove respondents without consent | 10 | 490 |
| Remove speeders (< 120s) | 25 | 465 |
| Remove failed attention check | 18 | 447 |
| Remove straightliners | 20 | 427 |
| Remove respondents with > 25% missing scale items | 0 | 427 |

- Scale items still missing after cleaning: **26** (handled by averaging over answered items)
- Final sample: **427** respondents (83% of the raw rows)
- Invalid values (Likert outside 1-5, age outside 18-70) were set to missing, not silently kept.
