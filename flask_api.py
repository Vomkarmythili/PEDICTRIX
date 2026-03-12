from flask import Flask, request, jsonify
from pymongo import MongoClient
import joblib
from datetime import datetime

app = Flask(__name__)

# Load ML Model
model = joblib.load("model.pkl")

# MongoDB
MongoClient("mongodb+srv://Vomkar:vomkar123@cluster0.s58phda.mongodb.net/peditrix?retryWrites=true&w=majority")
db = client["ai_machine"]
collection = db["sensor_data"]

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    temperature = float(data["temperature"])
    vibration = float(data["vibration"])

    prediction = model.predict([[temperature, vibration]])[0]

    status = "FAULT" if prediction == 1 else "NORMAL"

    health_score = 100 if status == "NORMAL" else 40

    record = {
        "temperature": temperature,
        "vibration": vibration,
        "status": status,
        "health_score": health_score,
        "timestamp": datetime.now()
    }

    collection.insert_one(record)

    return jsonify({
        "status": status,
        "health_score": health_score
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
