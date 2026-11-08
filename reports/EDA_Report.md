# EDA Report - Food Delivery Delay (Synthetic Data)

## 1. Data inspection
- Raw: 6,035 rows, 15 columns. Clean: 5,985 rows after removing 35 duplicates, 11 impossible distances (0 km or 99.9 km) and 4 negative delivery times.
- Fixed text problems (weather 120 rows, zone 80 rows), converted dates, filled 40 missing prep times with the cuisine median, labelled 25 missing traffic values "Unknown".
- 480 ratings are blank (8.0%). They stay blank because inventing customer opinions would be wrong.

## 2. Distribution
Delay = actual time - promised time. Average -2.2 min (negative = earlier than promised). The distribution is almost symmetric (skewness 0.05). 26 orders (0.4%) are IQR outliers (outside -22 to +18 min) and 11 have |z| > 3. Outliers occur on both sides: very early deliveries in low traffic, and very late ones mostly in high traffic.

## 3. Patterns
| Factor | Result |
|---|---|
| Hour | Late % peaks in lunch (12-14) and dinner (19-21): worst hour 21:00 at 23.8% |
| Weather | Clear 9.0%, Cloudy 10.1%, Fog 17.9%, Rain 29.0% late |
| Traffic | Low 2.7%, Medium 8.8%, High 28.2% late |
| Rain + High traffic | 57.2% late (362 orders) |
| Zone | Old Town 16.8%, Industrial Belt 16.0% ... Riverside 10.8% |
| Distance band | 0-2 km 10.8%, 2-4 km 12.5%, 4-6 km 13.9%, 6+ km 19.0% |
| Courier experience | 0-6 months 19.6% late, over 24 months 11.9% |
| Weekend | 16.3% late vs 12.7% on weekdays |

## 4. Correlations (Pearson with delay)
Traffic and weather are categories so they appear in the group tables and regression. Among numbers: distance r = 0.13, prep time r = 0.23, courier experience r = -0.10, customer rating r = -0.37. All are weak to moderate; delay has several small causes, not one big one.

## 5. Statistical tests
| Test | Result | Meaning |
|---|---|---|
| Welch t-test, Rain vs Clear delay | 1.7 vs -3.6 min, p < 0.001, Cohen d = 0.77 | Large, real difference |
| ANOVA across traffic levels | F = 967.6, p < 0.001 | Traffic level changes delay |
| Chi-square late vs zone | chi2 = 16.5, p = 0.021 | Zones differ, but effect is small |
| Pearson distance vs delay | r = 0.13, p < 0.001 | Small positive link |
| Spearman delay vs rating | rho = -0.36, p < 0.001 | Longer delay, lower rating |
| Mann-Whitney rating late vs on-time | 4.08 vs 4.63, p < 0.001 | Late orders rated lower |

## 6. Regression (minutes added to delay, other factors fixed)
High traffic +7.3, rain +5.3, fog +3.7, peak hour +3.1, medium traffic +3.0, weekend +1.4, each km +0.38, each prep minute +0.31, each courier month -0.04. R-squared = 0.46.

## 7. Rating impact
Average rating by delay band: on time or early 4.70; 0-5 min late 4.41; 5-10 min 4.16; 10-20 min 3.88.

## 8. Anomalies
Top late outliers: all in High traffic, several in Rain. Very early outliers: Low traffic, Clear weather, short distance.

## 9. Visualisations
See `visualizations/01` to `08`.
