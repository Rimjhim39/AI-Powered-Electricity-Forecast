import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

# =========================
# 1. LOAD DATA
# =========================
df = pd.read_csv("data/ontario_electricity_demand.csv")

# Convert to datetime
df['Datetime'] = pd.to_datetime(df['Datetime'])
df.set_index('Datetime', inplace=True)

# Rename column if needed (adjust based on your dataset)
df.rename(columns={'Ontario Demand': 'demand'}, inplace=True)

# =========================
# 2. FEATURE ENGINEERING
# =========================

# Time features
df['hour'] = df.index.hour
df['day_of_week'] = df.index.dayofweek
df['month'] = df.index.month

# Lag features
df['lag_1'] = df['demand'].shift(1)
df['lag_24'] = df['demand'].shift(24)

# Rolling feature
df['rolling_mean_24'] = df['demand'].rolling(window=24).mean()

# Drop missing values
df.dropna(inplace=True)

# =========================
# 3. DEFINE FEATURES & TARGET
# =========================
X = df.drop('demand', axis=1)
y = df['demand']

# =========================
# 4. TIME-SERIES SPLIT
# =========================
train_size = int(len(df) * 0.8)

X_train = X.iloc[:train_size]
X_test = X.iloc[train_size:]

y_train = y.iloc[:train_size]
y_test = y.iloc[train_size:]

# =========================
# 5. MODEL (XGBOOST)
# =========================
model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# 6. PREDICTION
# =========================
y_pred = model.predict(X_test)

# =========================
# 7. EVALUATION
# =========================
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("MAE:", mae)
print("RMSE:", rmse)

# =========================
# 8. SAVE MODEL
# =========================
joblib.dump(model, "models/model.pkl")

print("Model saved successfully!")