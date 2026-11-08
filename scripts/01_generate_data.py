
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(OUT, exist_ok=True)

N = 6000
zones = ["Old Town", "Riverside", "Tech Park", "University Area", "Industrial Belt",
         "Lakeview", "Market Road", "Suburb North"]
zone_extra = {"Old Town": 4.0, "Riverside": 0.5, "Tech Park": 1.0, "University Area": 0.0,   
              "Industrial Belt": 3.0, "Lakeview": 0.5, "Market Road": 3.5, "Suburb North": 1.5}
cuisines = ["North Indian", "South Indian", "Chinese", "Fast Food", "Biryani", "Desserts", "Healthy"]
cuisine_prep = {"North Indian": 17, "South Indian": 12, "Chinese": 15, "Fast Food": 10,
                "Biryani": 20, "Desserts": 8, "Healthy": 11}

dates = pd.date_range("2025-01-01", "2025-03-31")
order_dates = rng.choice(dates, N)
hour_probs = np.array([0.5, 0.3, 0.2, 0.1, 0.1, 0.2, 0.5, 1.0, 1.5, 1.6, 2.5, 5.0, 6.0, 4.0, 2.5, 2.5,
                       3.0, 4.0, 5.5, 8.0, 8.5, 7.0, 3.5, 1.5])
hour_probs = hour_probs / hour_probs.sum()
hours = rng.choice(np.arange(24), N, p=hour_probs)
minutes = rng.integers(0, 60, N)
dt = pd.to_datetime(order_dates) + pd.to_timedelta(hours, unit="h") + pd.to_timedelta(minutes, unit="m")

zone = rng.choice(zones, N, p=[0.14, 0.13, 0.16, 0.15, 0.08, 0.12, 0.12, 0.10])
cuisine = rng.choice(cuisines, N)
distance = np.clip(rng.gamma(3.0, 1.35, N), 0.4, 14).round(1)
items = rng.integers(1, 8, N)
order_value = np.round(120 + items * rng.uniform(70, 130, N) + rng.normal(0, 25, N), 0).clip(80)
weather = rng.choice(["Clear", "Cloudy", "Rain", "Fog"], N, p=[0.52, 0.22, 0.20, 0.06])
is_peak = ((hours >= 12) & (hours <= 14)) | ((hours >= 19) & (hours <= 21))
traffic = np.where(is_peak, rng.choice(["Low", "Medium", "High"], N, p=[0.10, 0.40, 0.50]),
                   rng.choice(["Low", "Medium", "High"], N, p=[0.45, 0.40, 0.15]))
courier_exp = rng.integers(1, 61, N)                    
is_weekend = (pd.to_datetime(order_dates).dayofweek >= 5)

prep = np.array([cuisine_prep[c] for c in cuisine]) + rng.normal(0, 3, N) + items * 0.8
prep = np.clip(prep, 4, None)
nominal_prep = np.array([cuisine_prep[c] for c in cuisine]) + items * 0.8      #promised = np.round(15 + nominal_prep + distance * 3.2 + 12, 0)   

traffic_f = pd.Series(traffic).map({"Low": 0, "Medium": 3, "High": 8}).values
weather_f = pd.Series(weather).map({"Clear": 0, "Cloudy": 0.5, "Rain": 6, "Fog": 4}).values
zone_f = pd.Series(zone).map(zone_extra).values
travel = distance * 3.6 + traffic_f * 0.9 + weather_f * 0.9 + zone_f * 0.5
exp_f = np.clip((24 - courier_exp) * 0.12, 0, None)       
rush_f = np.where(is_peak, 3.0, 0) + np.where(is_weekend, 1.5, 0)
actual = 15 + prep + travel + exp_f + rush_f + rng.normal(0, 4.5, N)
actual = np.round(np.clip(actual, 12, None), 0)
delay = actual - promised


rating = 4.6 - np.clip(delay, -5, 40) * 0.055 + rng.normal(0, 0.55, N)
rating = np.clip(np.round(rating), 1, 5)

df = pd.DataFrame({
    "order_id": [f"FD{100000 + i}" for i in range(N)],
    "order_datetime": dt, "zone": zone, "cuisine": cuisine, "distance_km": distance,
    "items_count": items, "order_value": order_value, "weather": weather, "traffic_level": traffic,
    "courier_experience_months": courier_exp, "prep_time_min": prep.round(1),
    "promised_time_min": promised, "actual_time_min": actual, "customer_rating": rating,
    "payment_method": rng.choice(["UPI", "Card", "Cash", "Wallet"], N, p=[0.55, 0.2, 0.15, 0.1]),
})
df = df.sort_values("order_datetime").reset_index(drop=True)

df["order_datetime"] = df["order_datetime"].dt.strftime("%Y-%m-%d %H:%M")
i = rng.choice(N, 120, replace=False); df.loc[i[:60], "weather"] = df.loc[i[:60], "weather"].str.upper()
df.loc[i[60:], "weather"] = df.loc[i[60:], "weather"].str.lower() + " "
i = rng.choice(N, 80, replace=False); df.loc[i, "zone"] = df.loc[i, "zone"].str.lower()
df.loc[rng.choice(N, 480, replace=False), "customer_rating"] = np.nan          
df.loc[rng.choice(N, 40, replace=False), "prep_time_min"] = np.nan
df.loc[rng.choice(N, 25, replace=False), "traffic_level"] = np.nan
df.loc[rng.choice(N, 6, replace=False), "distance_km"] = 0                     
df.loc[rng.choice(N, 5, replace=False), "distance_km"] = 99.9                  
df.loc[rng.choice(N, 4, replace=False), "actual_time_min"] = -10               
dups = df.sample(35, random_state=1)
df = pd.concat([df, dups]).sample(frac=1, random_state=2).sort_values("order_id", kind="stable").reset_index(drop=True)
df.to_csv(os.path.join(OUT, "raw_deliveries.csv"), index=False)
print("raw rows:", len(df))
