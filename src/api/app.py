from flask import Flask, request, jsonify
from flask_cors import CORS
from ml_model import predict_price

app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json
    date = data["date"]
    horizon = int(data["horizon"])

    prices = predict_price(date, horizon)

    recommendation = "BUY" if prices[-1] > prices[0] else "SELL"

    return jsonify({
        "prices": prices,
        "recommendation": recommendation
    })

if __name__ == "__main__":
    app.run(debug=True)