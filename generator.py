import json
import random
import time
from datetime import datetime

FILE_PATH = "data/sample_telemetry.json"

SOURCE_IPS = ["192.168.1.50", "10.0.0.99", "172.16.0.12", "192.168.1.105"]
EVENT_TYPES = ["auth", "scan", "exfiltration", "routine"]

def generate_random_log():
    ip = random.choice(SOURCE_IPS)
    event = random.choice(EVENT_TYPES)
    
    # Attack pattern condition simulation
    if event == "auth":
        bytes_sent = random.randint(100, 1000)
        auth_status = "FAILED" if random.random() < 0.7 else "SUCCESS"
        dest_port = 22
    elif event == "scan":
        bytes_sent = random.randint(200, 800)
        auth_status = "FAILED"
        dest_port = random.randint(20, 1000)
    elif event == "exfiltration":
        bytes_sent = random.randint(10000000, 60000000)
        auth_status = "SUCCESS"
        dest_port = 443
    else:
        bytes_sent = random.randint(500, 5000)
        auth_status = "SUCCESS"
        dest_port = 80

    return {
        "timestamp": datetime.now().isoformat(),
        "source_ip": ip,
        "dest_ip": "10.0.0.1",
        "src_port": random.randint(40000, 60000),
        "dest_port": dest_port,
        "bytes": bytes_sent,
        "auth_status": auth_status,
        "event_type": event
    }

def start_generator():
    print("🚀 Telemetry Live Data Generator Started... (Press Ctrl+C to stop)")
    while True:
        try:
            # Read existing logs
            try:
                with open(FILE_PATH, "r") as f:
                    logs = json.load(f)
            except Exception:
                logs = []

            # Append new random telemetry log
            new_log = generate_random_log()
            logs.append(new_log)

            # Keep only last 50 logs to prevent file bloat
            logs = logs[-50:]

            with open(FILE_PATH, "w") as f:
                json.dump(logs, f, indent=2)

            print(f"[+] Live log generated | Source IP: {new_log['source_ip']} | Event: {new_log['event_type']}")
            time.sleep(3) # Generates new log every 3 seconds

        except KeyboardInterrupt:
            print("\nGenerator stopped.")
            break

if __name__ == "__main__":
    start_generator()