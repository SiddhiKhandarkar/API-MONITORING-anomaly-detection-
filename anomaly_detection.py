import smtplib
import ssl
import pandas as pd
import os
from pymongo import MongoClient
from sklearn.ensemble import IsolationForest
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
import plotly.express as px

load_dotenv()

client = MongoClient("mongodb://localhost:27017/")
db = client["api_monitoring"]
collection = db["logs"]

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

app = Flask(__name__, template_folder="templates")

def send_email_alert(anomalies):
    """Send an email alert for new anomalies with a dashboard link."""
    if anomalies.empty or not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
        return

    dashboard_url = "http://localhost:5000/"
    recent_anomalies = anomalies.tail(5)

    subject = "🚨 New API Anomaly Detected!"
    body = f"""
    One or more new anomalies have been detected in your API monitoring system.

    Summary:
    - Total new anomalies: {len(recent_anomalies)}

    View details: {dashboard_url}
    """

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print("🚀 Alert email sent successfully!")
    except Exception as e:
        print(f"⚠️ Failed to send email: {e}")

def fetch_logs():
    logs = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(logs)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.sort_values(by='timestamp', inplace=True)
    return df

def detect_anomalies():
    df = fetch_logs()
    if df.empty:
        return pd.DataFrame()

    features = df[['response_time', 'status_code']]
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly'] = model.fit_predict(features)

    anomalies = df[df['anomaly'] == -1]
    if not anomalies.empty:
        print("Anomalies detected!")
        send_email_alert(anomalies)
    return anomalies

@app.route('/')
def index():
    return render_template('prodashboard.html')

@app.route('/logs')
def logs():
    df = fetch_logs()
    return jsonify(df.to_dict(orient='records'))

@app.route('/anomalies')
def anomalies():
    df = detect_anomalies()
    return jsonify(df.to_dict(orient='records'))

@app.route('/charts')
def charts():
    df = fetch_logs()
    if df.empty:
        return jsonify({})
    fig = px.line(df, x='timestamp', y='response_time', color='api', title='Response Time Over Time')
    return jsonify(fig.to_json())

if __name__ == "__main__":
    app.run(debug=True)
