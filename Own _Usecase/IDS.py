from collections import defaultdict
import time

LOG_FILE = "network.log"

logs = [
    (time.time(), "192.168.1.5", 22),
    (time.time(), "192.168.1.5", 23),
    (time.time(), "192.168.1.5", 25),
    (time.time(), "192.168.1.5", 80),
    (time.time(), "192.168.1.10", 80),
]

# Threshold for suspicious activity
THRESHOLD = 3  
TIME_WINDOW = 60 

# Track activity per IP
ip_activity = defaultdict(list)

def log_event(message):
    """Write log message to file and print it."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_entry = f"{timestamp} | {message}"
    print(log_entry)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

def process_log(timestamp, src_ip, dest_port):
    """Process a single network event."""
    ip_activity[src_ip].append(timestamp)
    # Remove old events outside the time window
    ip_activity[src_ip] = [t for t in ip_activity[src_ip] if t > time.time() - TIME_WINDOW]

    log_event(f"Connection from {src_ip} to port {dest_port}")

    if len(ip_activity[src_ip]) > THRESHOLD:
        log_event(f"[ALERT] Possible port scan detected from {src_ip}")

# Main loop: process logs
for log_item in logs:
    ts, ip, port = log_item
    process_log(ts, ip, port)
