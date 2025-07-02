import requests
import time
import random
from datetime import datetime

API_URL = "http://127.0.0.1:5000/log"  # Log collector endpoint

def generate_log():
    log = {
        "api": random.choice(["auth_service", "payment_service", "order_service"]),
        "response_time": random.randint(100, 1000),  # Simulate API latency
        "status_code": random.choices([200, 200, 200, 500, 502], weights=[85, 5, 5, 3, 2])[0],  # Simulate errors
        "timestamp": datetime.utcnow().isoformat()
    }
    return log

while True:
    log_data = generate_log()
    response = requests.post(API_URL, json=log_data)
    print(f"Sent log: {log_data} | Status: {response.status_code}")
    time.sleep(2)  # Simulate API calls every 2 seconds
