from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from ml_model import predict_price

app = Flask(__name__)
CORS(app)

# ================= HOME ROUTE =================

@app.route("/")
def home():
    return render_template("index.html")


# ================= PREDICTION API =================

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    date = data["date"]
    horizon = int(data["horizon"])

    prices = predict_price(date, horizon)

    # ================= BASIC ANALYTICS =================

    avg_price = sum(prices) / len(prices)
    peak_price = max(prices)
    low_price = min(prices)

    peak_hour = prices.index(peak_price)
    low_hour = prices.index(low_price)

    # ================= TIME LABELS =================

    hours = [f"{i:02d}:00" for i in range(horizon)]

    # ================= DEMAND ESTIMATION =================

    demand = [round(200 + p * 30, 2) for p in prices]

    # ================= SMART RECOMMENDATION =================

    if avg_price > 7:
        recommendation = "SELL (High Price)"

    elif avg_price < 4:
        recommendation = "BUY (Low Price)"

    else:
        recommendation = "HOLD (Moderate)"

    # ================= RESPONSE =================

    return jsonify({

        "prices": prices,
        "hours": hours,
        "demand": demand,

        "meta": {
            "avg_price": round(avg_price, 2),
            "peak_hour": peak_hour,
            "low_hour": low_hour
        },

        "recommendation": recommendation
    })


# ================= MAIN =================

if __name__ == "__main__":
    app.run(debug=True)