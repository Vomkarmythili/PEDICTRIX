from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
import joblib
from datetime import datetime

app = Flask(__name__)

# ---------------- LOAD ML MODEL ----------------
model = joblib.load("model.pkl")

# ---------------- MONGODB CONNECTION ----------------
try:
    client = MongoClient(
        "mongodb+srv://Vomkar:vomkar123@cluster0.s58phda.mongodb.net/peditrix?retryWrites=true&w=majority",
        serverSelectionTimeoutMS=10000  # 10 seconds timeout
    )
    db = client["ai_machine"]
    collection = db["sensor_data"]
except errors.ServerSelectionTimeoutError:
    print("Cannot connect to MongoDB Atlas. Check network access or credentials.")
    collection = None  # Safe fallback

# ---------------- API ROUTE ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if collection is None:
        return jsonify({"error": "MongoDB connection not established"}), 500

    data = request.get_json()

    try:
        temperature = float(data["temperature"])
        vibration = float(data["vibration"])
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

    # Make prediction
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

    # Insert into MongoDB
    collection.insert_one(record)

    return jsonify({
        "status": status,
        "health_score": health_score
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
