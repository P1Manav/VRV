import random
from datetime import datetime, timedelta
from collections import Counter

# Sample data for log generation
endpoints = [
    "/home", "/about", "/contact", "/dashboard", "/register", "/profile", "/feedback"
]
status_codes = [
    ("200", ""),  # 200 status code, no message
    ("401", "Invalid credentials")  # 401 status code, specific message
]
suspicious_threshold = 5  # Threshold for detecting suspicious activity

# Function to generate a random valid IP address
def generate_ip():
    return f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

# Function to generate a log entry
def generate_log_line(ip, endpoint, status_code, message=None):
    timestamp = datetime.now() - timedelta(seconds=random.randint(0, 3600))
    timestamp_str = timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")
    
    if status_code == "401" and message:
        return f'{ip} - - [{timestamp_str}] "POST {endpoint} HTTP/1.1" {status_code} 128 "{message}"'
    return f'{ip} - - [{timestamp_str}] "GET {endpoint} HTTP/1.1" {status_code} 512'

# Generate log data with multiple requests from the same IP
ip_requests = Counter()
log_entries = []

# Generate logs with varying activity, focusing on repetitive requests
for _ in range(200):  # Adjust the range for the desired number of logs
    ip = generate_ip()
    endpoint = random.choice(endpoints)
    status_code, message = random.choice(status_codes)
    
    ip_requests[ip] += 1
    
    # Simulate suspicious activity by adding repetitive requests
    if ip_requests[ip] > suspicious_threshold:
        status_code, message = ("401", "Invalid credentials")
    
    log_entries.append(generate_log_line(ip, endpoint, status_code, message))

# Save the generated logs to a file
output_file = "logical_log_file.log"
with open(output_file, "w") as file:
    for entry in log_entries:
        file.write(entry + "\n")

# Detect suspicious activity based on repetitive requests
suspicious_ips = [ip for ip, count in ip_requests.items() if count > suspicious_threshold]

print(f"Log file '{output_file}' generated successfully.")
print("\nSuspicious IPs detected (more than 5 requests):")
for ip in suspicious_ips:
    print(ip)
