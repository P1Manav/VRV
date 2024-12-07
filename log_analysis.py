import csv
from collections import Counter

# Configuration
LOG_FILE = "sample.log"  # Replace with the actual log file path
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

# Main logic
def main():
    # Parse the logs
    ip_requests, endpoint_access, failed_logins = parse_logs(LOG_FILE)

    # Determine the most frequently accessed endpoint
    most_accessed_endpoint = endpoint_access.most_common(1)[0]

    # Display the results
    print("IP Address           Request Count")
    for ip, count in ip_requests.most_common():
        print(f"{ip:20} {count}")
    
    print("\nMost Frequently Accessed Endpoint:")
    print(f"{most_accessed_endpoint[0]} (Accessed {most_accessed_endpoint[1]} times)")

    print("\nSuspicious Activity Detected:")
    print("IP Address           Failed Login Attempts")
    for ip, count in failed_logins.items():
        if count > SUSPICIOUS_THRESHOLD:
            print(f"{ip:20} {count}")
    
    # Save the results to CSV
    save_to_csv(ip_requests, most_accessed_endpoint, failed_logins)
    print(f"\nResults saved to {OUTPUT_CSV}")

# Execute the script
if __name__ == "__main__":
    main()
