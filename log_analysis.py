import csv
from collections import defaultdict

def analyze_logs(filepath):
    ip_access_counts = defaultdict(int)
    endpoint_access_counts = defaultdict(int)
    suspicious_activity = defaultdict(int)
    total_requests = 0

    # Read the log file and process it line by line
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split()
            if len(parts) > 6:  # Ensure the line has enough parts to parse
                ip = parts[0]
                endpoint = parts[6]
                status_code = int(parts[8])  # Assuming the status code is at index 8
                message = ' '.join(parts[9:])  # Capture the message part if present

                # Count total requests per IP
                ip_access_counts[ip] += 1
                total_requests += 1

                # Count endpoint accesses
                endpoint_access_counts[endpoint] += 1

                # Detect failed login attempts based on the message "Invalid credentials"
                if status_code == 401 and "Invalid credentials" in message:
                    suspicious_activity[ip] += 1

    # Identify the most accessed endpoint and its access count
    most_accessed_endpoint, most_accessed_count = max(endpoint_access_counts.items(), key=lambda item: item[1])

    # Identify suspicious IPs (IPs with more than 0 failed login attempts)
    suspicious_activity_list = [(ip, count) for ip, count in suspicious_activity.items() if count > 10]

    # Convert ip_access_counts to a list of tuples for template rendering
    ip_access_counts_list = list(ip_access_counts.items())

    # Save results to CSV file
    with open('log_analysis_results.csv', 'w', newline='') as csvfile:
        # Write IP access counts to CSV
        fieldnames = ['IP Address', 'Request Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ip, count in ip_access_counts_list:
            writer.writerow({'IP Address': ip, 'Request Count': count})

        # Add most accessed endpoint to the CSV
        csvfile.write('\n')
        writer = csv.DictWriter(csvfile, fieldnames=['Endpoint', 'Access Count'])
        writer.writeheader()
        writer.writerow({'Endpoint': most_accessed_endpoint, 'Access Count': most_accessed_count})

        # Add suspicious activity to the CSV
        csvfile.write('\n')
        writer = csv.DictWriter(csvfile, fieldnames=['IP Address', 'Failed Login Count'])
        writer.writeheader()
        for ip, count in suspicious_activity_list:
            writer.writerow({'IP Address': ip, 'Failed Login Count': count})

    return ip_access_counts_list, most_accessed_endpoint, most_accessed_count, suspicious_activity_list, total_requests
