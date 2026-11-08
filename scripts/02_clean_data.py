"""
02_clean_data.py - cleans raw_deliveries.csv, adds analysis columns, writes cleaned CSV + cleaning log.
Run: python scripts/02_clean_data.py
"""
import os
import pandas as pd

BASE = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(os.path.join(BASE, "cleaned"), exist_ok=True)
df = pd.read_csv(os.path.join(BASE, "raw", "raw_deliveries.csv"))
log = []
def note(step, n, why): log.append({"step": step, "rows_affected": int(n), "reason": why})

note("Raw rows loaded", len(df), "Starting point")

b = len(df); df = df.drop_duplicates(subset="order_id", keep="first")
note("Removed duplicate order_id", b - len(df), "Same order recorded twice")

for col in ("weather", "zone", "traffic_level"):
    before = df[col].copy()
    df[col] = df[col].str.strip().str.title()
    note(f"Standardised text in {col}", (before.fillna("") != df[col].fillna("")).sum(), f"Fix case and extra spaces in {col}")

df["order_datetime"] = pd.to_datetime(df["order_datetime"], format="%Y-%m-%d %H:%M")
note("Converted order_datetime to datetime", len(df), "Needed for hour / weekday features")

b = len(df); df = df[(df["distance_km"] > 0) & (df["distance_km"] <= 30)]
note("Removed impossible distance (0 or > 30 km)", b - len(df), "Delivery cannot be 0 km or 99.9 km in this city")

b = len(df); df = df[df["actual_time_min"] > 0]
note("Removed negative actual delivery time", b - len(df), "Time cannot be negative")

n = df["traffic_level"].isna().sum()
df["traffic_level"] = df["traffic_level"].fillna("Unknown")
note("Missing traffic_level -> 'Unknown'", n, "Kept rows; 'Unknown' is its own group")

n = df["prep_time_min"].isna().sum()
df["prep_time_min"] = df["prep_time_min"].fillna(df.groupby("cuisine")["prep_time_min"].transform("median"))
note("Missing prep_time -> median of same cuisine", n, "Prep time depends on cuisine, so cuisine median is fair")

note("Missing customer_rating kept as blank", df["customer_rating"].isna().sum(),
     "Not every customer rates; imputing would invent opinions")

# ---- new analysis columns
df["delay_min"] = df["actual_time_min"] - df["promised_time_min"]
df["is_late"] = (df["delay_min"] > 5).astype(int)          # late = more than 5 min over promise
df["hour"] = df["order_datetime"].dt.hour
df["day_of_week"] = df["order_datetime"].dt.day_name()
df["is_weekend"] = df["order_datetime"].dt.dayofweek >= 5
df["is_peak_hour"] = df["hour"].isin([12, 13, 14, 19, 20, 21])
df["month"] = df["order_datetime"].dt.month_name()
df["distance_band"] = pd.cut(df["distance_km"], [0, 2, 4, 6, 30], labels=["0-2 km", "2-4 km", "4-6 km", "6+ km"])
df = df.sort_values("order_datetime").reset_index(drop=True)
note("Final clean rows", len(df), "Ready for EDA")

df.to_csv(os.path.join(BASE, "cleaned", "clean_deliveries.csv"), index=False)
pd.DataFrame(log).to_csv(os.path.join(BASE, "cleaned", "cleaning_log.csv"), index=False)
print(pd.DataFrame(log).to_string(index=False))
