import pandas as pd
import numpy as np
import os
# =========================
# 1. CREATE TIME RANGE
# =========================
date_range = pd.date_range(start="2023-01-01", end="2023-03-31", freq="h")
df = pd.DataFrame()
df['Datetime'] = date_range
# =========================
# 2. GENERATE DEMAND
# =========================
# Daily pattern
df['hour'] = df['Datetime'].dt.hour
daily_pattern = 100 + 50 * np.sin(2 * np.pi * df['hour'] / 24)
# Weekly pattern
df['day_of_week'] = df['Datetime'].dt.dayofweek
weekly_pattern = np.where(df['day_of_week'] < 5, 20, -10)
# Random noise
noise = np.random.normal(0, 5, len(df))
# Final demand
df['demand'] = daily_pattern + weekly_pattern + noise
# =========================
# 3. GENERATE PRICE
# =========================
df['price'] = df['demand'] * 0.5 + np.random.normal(0, 10, len(df))
# =========================
# 4. CLEAN DATA
# =========================
df = df[['Datetime', 'demand', 'price']]
# =========================
# 5. CREATE DATA FOLDER (FIX)
# =========================
os.makedirs("data", exist_ok=True)
# =========================
# 6. SAVE DATASET
# =========================
df.to_csv("data/synthetic_india_electricity.csv", index=False)

print("✅ Synthetic dataset generated successfully!")