# Results on the fake dataset

Sample size after cleaning: **N = 427**

## Sample description

- Age: M = 35.5, SD = 9.4, range 19-66
- Years of experience: M = 10.2, SD = 6.4

**Gender (%)**

| gender            |    % |
|:------------------|-----:|
| Female            | 52.2 |
| Male              | 43.1 |
| Prefer not to say |  3.3 |
| Non-binary        |  1.4 |

**Sector (n)**

| sector        |   n |
|:--------------|----:|
| IT & Software |  84 |
| Healthcare    |  74 |
| Finance       |  63 |
| Retail        |  57 |
| Manufacturing |  51 |
| Public Sector |  49 |
| Education     |  47 |
| Not stated    |   2 |

## Scale reliability (Cronbach's alpha)

- Digital competence (4 items): alpha = 0.72
- Burden (4 items): alpha = 0.74

## Descriptive statistics of main variables

|                        |   count |   mean |   std |   min |   max |   skew |
|:-----------------------|--------:|-------:|------:|------:|------:|-------:|
| digital_competence     |     427 |   3.32 |  0.83 |  1.25 |  5    |  -0.31 |
| burden                 |     427 |   2.78 |  0.85 |  1    |  4.75 |   0.16 |
| help_requests_per_week |     427 |   2.44 |  1.8  |  0    |  8    |   0.75 |

## Mean burden by sector (excluding "Not stated")

| sector        |   count |   mean |   std |
|:--------------|--------:|-------:|------:|
| Education     |      47 |   2.89 |  0.86 |
| Public Sector |      49 |   2.82 |  0.89 |
| Healthcare    |      74 |   2.81 |  0.81 |
| Retail        |      57 |   2.8  |  0.89 |
| Finance       |      63 |   2.76 |  0.85 |
| Manufacturing |      51 |   2.74 |  0.88 |
| IT & Software |      84 |   2.71 |  0.82 |

One-way ANOVA across sectors: F = 0.30, p = 0.936

## Correlation: digital competence and burden

- Pearson r = 0.29, p = 6.77e-10
- Spearman rho = 0.28, p = 6.34e-09

**Caution:** this is synthetic data, so the relationship was built into the generator. A real study would need to check assumptions, report effect sizes and avoid causal claims from correlations.
