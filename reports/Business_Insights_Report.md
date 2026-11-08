# Business Insights Report - Late Deliveries (Synthetic Data)

**Prepared by:** Adarsh Gawande. Data is synthetic; planted patterns mean this shows method, not real-world fact.

## Executive summary
13.7% of 5,985 orders arrived more than 5 minutes late. Lateness is driven mainly by **traffic and weather**, then by **peak hours**, and is made worse by **new couriers** and a few zones. Late orders get an average rating of 4.08 versus 4.63 for on-time orders, so each late delivery has a measurable customer cost.

## Business questions and answers
1. **Overall performance?** 13.7% late, average delay -2.2 min, average rating 4.55.
2. **When?** 12-14 and 19-21 (20.8% late vs 5.9% off-peak); 21:00 is worst (23.8%); weekends 16.3% vs 12.7%.
3. **What conditions?** Rain 29.0% late (clear 9.0%); high traffic 28.2% (low 2.7%); both together 57.2%.
4. **Where?** Old Town 16.8% and Industrial Belt 16.0% are worst; Riverside 10.8% best.
5. **Is distance the problem?** Only slightly: +0.4 min per km. The promise already includes travel time; weather and traffic are the real gap.
6. **Do new couriers matter?** Yes: 19.6% late for 0-6 months vs 11.9% for over 24 months.
7. **Does delay hurt ratings?** Yes: 4.08 vs 4.63 average; low ratings (3 or less) are 15.1% of late orders vs 1.8% of on-time orders.
8. **Which factors rank highest (regression)?** High traffic, rain, fog, peak hour.

## Recommendations
1. **Smart promise times:** add about 7 min under high traffic and 5 min in rain. Expected effect: fewer late orders without changing real speed. (Estimate from regression coefficients; test with an A/B pilot.)
2. **Peak capacity:** add couriers 12-14 and 19-21, weekends first.
3. **Courier onboarding:** route new couriers to short, low-traffic orders for 6 months; mentor programme.
4. **Zone review:** inspect Old Town and Industrial Belt pick-up points and routes.
5. **Service recovery:** auto-message and small credit when predicted lateness exceeds 10 min.
6. **Monitoring:** weekly dashboard of late % by hour, weather and zone.

## Limitations
Synthetic data; 3 months only; late threshold of 5 minutes is assumed; ratings missing for 8% of orders; regression shows association, not proof of cause; no courier supply, GPS or restaurant data.

## Conclusion
Most lateness comes from conditions the platform can predict (traffic, rain, peak hours). Better promises and peak staffing target the largest drivers found in this analysis.
