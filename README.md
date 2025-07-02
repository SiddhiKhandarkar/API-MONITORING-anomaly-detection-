
# 🔍 API Monitoring & Anomaly Detection System

This project is a lightweight, real-time API **log monitoring and anomaly detection system** that uses:

- 🧠 **Machine Learning** (Isolation Forest)
- 📊 **Flask-based Dashboard**
- 📡 **SocketIO for Live Updates**
- 📩 **Email Alerts**
- 🐳 **Dockerized Deployment**

Ideal for developers, DevOps, or backend teams who want a pluggable system for **detecting unusual behavior in API response times and status codes**.

---

## 📦 Components

### 1. `log_collector.py`
- Flask + SocketIO server
- Collects API logs via `/log` endpoint
- Stores logs in MongoDB
- Emits real-time anomaly updates to frontend

### 2. `generate_logs.py`
- Simulates traffic by sending random logs to the collector
- Mimics APIs like `auth_service`, `payment_service`, `order_service`

### 3. `anomaly_detection.py`
- Flask app for dashboard visualization
- Detects anomalies using **Isolation Forest**
- Sends email alerts if anomalies are found

---

## 📊 Features

- ✅ Real-time anomaly detection
- 📬 Email alerts on detected anomalies
- 📈 Charts for response time trends (Plotly)
- 🔌 Easily integratable with existing APIs
- 🧪 Test data generator
- 🐳 Docker support for quick deployment

---

## 🧪 Setup Instructions

### 🔧 1. Clone Repository
```bash
git clone https://github.com/your-username/api-anomaly-monitor.git
cd api-anomaly-monitor
```

### 📦 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 🔑 3. Set Environment Variables

Create a `.env` file:
```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECEIVER_EMAIL=recipient_email@gmail.com
```

Enable **Less Secure App Access** or use **App Passwords** for Gmail.

---

## 🚀 Run the System

### 1. Start Log Collector
```bash
python log_collector.py
```

### 2. Simulate Logs
```bash
python generate_logs.py
```

### 3. Start Anomaly Detector Dashboard
```bash
python anomaly_detection.py
```

Then open [http://localhost:5000](http://localhost:5000)

---

## 🐳 Docker Support

You can run the anomaly detection system using Docker:
```bash
docker build -t anomaly-detector .
docker run -p 5000:5000 anomaly-detector
```

---

## 📁 Project Structure

```bash
.
├── anomaly_detection.py       # Dashboard + Email Alerts
├── generate_logs.py           # Random log generator
├── log_collector.py           # Log receiver and emitter
├── Dockerfile                 # For Docker containerization
├── requirements.txt           # Python dependencies
├── templates/
│   └── prodashboard.html      # Dashboard UI
└── .env                       # Gmail credentials (not committed)
```

---

## ✨ Future Ideas

- 🌐 Streamlit or React-based frontend
- 📂 Historical anomaly archive
- 🔐 Authentication for dashboard
- 📦 Integrate with real-world API logs

---

## 🛡 License

This project is licensed under the MIT License.

---

## ❤️ Built by Team CodeFusion

Monitoring APIs has never been this easy.

