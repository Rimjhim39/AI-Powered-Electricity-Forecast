import pickle
import pandas as pd
import random

model = pickle.load(open("model.pkl", "rb"))

def get_dynamic_demand(hour):
    """Simulate realistic demand based on time of day"""

    if 6 <= hour < 12:
        base = 14000   # morning
    elif 12 <= hour < 18:
        base = 18000   # afternoon peak
    elif 18 <= hour < 23:
        base = 20000   # evening peak
    else:
        base = 12000   # night low

    # add slight randomness
    return base + random.randint(-500, 500)


def predict_price(date, horizon):

    predictions = []

    current = pd.to_datetime(date)

    # slightly varied initial lag values
    lag1 = 50 + random.uniform(-5, 5)
    lag2 = 48 + random.uniform(-5, 5)
    lag24 = 52 + random.uniform(-5, 5)

    for i in range(horizon):

        hour = current.hour
        day = current.day
        month = current.month

        # 🔥 dynamic demand instead of constant
        demand = get_dynamic_demand(hour)

        X = [[hour, day, month, demand, lag1, lag2, lag24]]

        price = model.predict(X)[0]

        predictions.append(round(float(price), 2))

        # update lag values
        lag24 = lag2
        lag2 = lag1
        lag1 = price

        current += pd.Timedelta(hours=1)

    return predictions