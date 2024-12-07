from flask import Flask, request, render_template, send_file, url_for
import csv
from collections import Counter
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SUSPICIOUS_THRESHOLD = 10  # Threshold for flagging suspicious activity
OUTPUT_CSV = "log_analysis_results.csv"

# Function to parse the log file
def parse_logs(log_file):
    ip_requests = Counter()
    endpoint_access = Counter()
    failed_logins = Counter()

    with open(log_file, 'r') as file:
        for line in file:
            parts = line.split()
            ip = parts[0]
            endpoint = parts[6]
            status_code = parts[8]
            message = line.strip().split('"')[-1] if "Invalid credentials" in line else None

            # Count requests per IP
            ip_requests[ip] += 1

            # Count endpoint access
            endpoint_access[endpoint] += 1

            # Count failed login attempts
            if status_code == "401" or message == "Invalid credentials":
                failed_logins[ip] += 1

    return ip_requests, endpoint_access, failed_logins

# Function to save results to CSV
def save_to_csv(ip_requests, most_accessed_endpoint, failed_logins):
    with open(OUTPUT_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write Requests per IP
        writer.writerow(["IP Address", "Request Count"])
        for ip, count in ip_requests.most_common():
            writer.writerow([ip, count])

        # Write Most Accessed Endpoint
        writer.writerow([])
        writer.writerow(["Most Frequently Accessed Endpoint"])
        writer.writerow(["Endpoint", "Access Count"])
        writer.writerow(most_accessed_endpoint)

        # Write Suspicious Activity
        writer.writerow([])
        writer.writerow(["Suspicious Activity Detected"])
        writer.writerow(["IP Address", "Failed Login Count"])
        for ip, count in failed_logins.items():
            if count > SUSPICIOUS_THRESHOLD:
                writer.writerow([ip, count])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Parse the logs
        ip_requests, endpoint_access, failed_logins = parse_logs(file_path)

        # Determine the most frequently accessed endpoint
        most_accessed_endpoint = endpoint_access.most_common(1)[0]

        # Save results to CSV
        save_to_csv(ip_requests, most_accessed_endpoint, failed_logins)

        # Prepare data for display
        results = {
            "ip_requests": ip_requests.most_common(),
            "most_accessed_endpoint": most_accessed_endpoint,
            "suspicious_activity": [
                (ip, count)
                for ip, count in failed_logins.items()
                if count > SUSPICIOUS_THRESHOLD
            ]
        }

        return render_template('results.html', results=results)

@app.route('/download')
def download_file():
    return send_file(OUTPUT_CSV, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
