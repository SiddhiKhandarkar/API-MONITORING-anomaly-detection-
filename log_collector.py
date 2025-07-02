from flask import Flask, request, jsonify  # Import request
from flask_socketio import SocketIO
import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import IsolationForest

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow frontend to connect

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["api_monitoring"]
collection = db["logs"]


@app.route("/log", methods=["POST"])  # ✅ ADD THIS API ROUTE
def receive_log():
    """Receive logs from API and store in MongoDB."""
    log_data = request.json  # Get JSON data from request
    if not log_data:
        return jsonify({"error": "Invalid log data"}), 400

    collection.insert_one(log_data)  # Store in MongoDB
    return jsonify({"message": "Log received"}), 201


def detect_anomalies():
    logs = list(collection.find({}, {"_id": 0}))
    if not logs:
        return []

    df = pd.DataFrame(logs)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by='timestamp', inplace=True)

    features = df[['response_time', 'status_code']]
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly'] = model.fit_predict(features)

    anomalies = df[df['anomaly'] == -1]

    # Emit anomalies to connected clients
    socketio.emit('update_anomalies', anomalies.to_dict(orient='records'))

    return anomalies.to_dict(orient='records')


@socketio.on('fetch_anomalies')
def handle_fetch_anomalies():
    anomalies = detect_anomalies()
    socketio.emit('update_anomalies', anomalies)


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0")
