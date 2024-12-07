from flask import Flask, request, render_template, redirect, url_for, send_file # type: ignore
import os
import random
import csv
from log_analysis import analyze_logs

app = Flask(__name__)

# Define the upload directory for files
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['logfile']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Read and display the log content
            with open(filepath, 'r') as f:
                log_content = f.read()
            
            return render_template('preview.html', log_content=log_content, filepath=filepath)
    return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate_file():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'generated_log_file.txt')
    generate_log_file(filepath)
    with open(filepath, 'r') as f:
        log_content = f.read()
    
    return render_template('preview.html', log_content=log_content, filepath=filepath)

@app.route('/analyze/<filepath>', methods=['GET'])
def analyze(filepath):
    ip_access_counts, most_accessed_endpoint, most_accessed_count, suspicious_activity, total_requests = analyze_logs(filepath)
    print("Suspicious Activity List:", suspicious_activity)
    
    # Save the analysis results to a CSV file in the static folder
    csv_path = os.path.join(app.config['STATIC_FOLDER'], 'log_analysis_results.csv')
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['IP Address', 'Access Count'])
        for ip, count in ip_access_counts:
            writer.writerow([ip, count])
        
        writer.writerow([])
        writer.writerow(['Most Accessed Endpoint', 'Access Count'])
        writer.writerow([most_accessed_endpoint, most_accessed_count])
        
        writer.writerow([])
        writer.writerow(['IP Address', 'Failed Login Count'])
        for ip, count in suspicious_activity:
            writer.writerow([ip, count])

    # Render the results page with the analysis
    return render_template('results.html',
                           ip_access_counts=ip_access_counts,
                           most_accessed_endpoint=most_accessed_endpoint,
                           most_accessed_count=most_accessed_count,
                           suspicious_activity=suspicious_activity,
                           total_requests=total_requests,
                           csv_file_path='log_analysis_results.csv')

@app.route('/download_csv')
def download_csv():
    csv_path = os.path.join(app.config['STATIC_FOLDER'], 'log_analysis_results.csv')
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True)
    return "CSV file not found."

def generate_log_file(filename):
    endpoints = ["/home", "/login", "/about", "/dashboard", "/contact", "/profile", "/register", "/feedback"]
    status_codes = [200, 401, 404, 500]
    ip_count = random.randint(7, 15)
    suspicious_ips_count = random.randint(1, 5)
    total_logs = random.randint(100, 200)

    # Generate unique IP addresses
    ip_pool = set()
    while len(ip_pool) < ip_count:
        ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        ip_pool.add(ip)
    ip_pool = list(ip_pool)
    
    suspicious_ips = random.sample(ip_pool, suspicious_ips_count)

    with open(filename, 'w') as file:
        for _ in range(total_logs):
            ip = random.choice(ip_pool)
            endpoint = random.choice(endpoints)
            status_code = random.choice(status_codes)
            message = "Invalid credentials" if status_code == 401 and endpoint == "/login" else None
            log_entry = f'{ip} - - [07/Dec/2024:10:{random.randint(10,59)}:{random.randint(10,59)} +0000] "GET {endpoint} HTTP/1.1" {status_code} {random.randint(128, 1024)}'
            if message:
                log_entry += f' "{message}"'
            log_entry += "\n"
            file.write(log_entry)

if __name__ == '__main__':
    app.run(debug=True)
