# VRV
# Log Analysis Web Application

## Project Overview
This project is a web application built with Flask that allows users to generate and analyze log files. The logs contain IP addresses, endpoints, status codes, and messages that simulate user requests to a web server. The main purpose of this project is to provide insights into web traffic, detect suspicious activity, and display statistics in a user-friendly manner.

## Features
- **Log Generation**: Create custom log files with random IP addresses, endpoints, and status codes.
- **Log Analysis**: Analyze the log files to:
  - Count requests per IP.
  - Identify the most accessed endpoint.
  - Detect suspicious activity (e.g., failed login attempts with "Invalid credentials").
- **Web Interface**: An intuitive interface to upload logs, preview them, and view analysis results.
- **CSV Export**: Export analysis results to a CSV file for further examination.

## Project Structure
The project is organized into the following files:

- **app.py**: The main Flask application file that handles routing and logic.
- **generate.py**: A script to generate a random log file with unique IPs, endpoints, and status codes.
- **index.html**: The homepage for uploading or generating logs.
- **preview.html**: Displays the content of a generated log file before analysis.
- **results.html**: Shows the results of log analysis, including suspicious IPs, total requests, and endpoint statistics.
- **style.css**: Custom styles for the web application.
- **log_analysis.py**: A script to analyze log files and generate output like request counts, most accessed endpoints, and suspicious activity. Results are displayed in the terminal and saved to `log_analysis_results.csv`.

## Requirements
- **Python 3.x**
- **Flask**: Web framework used for the application.
- **CSV module**: For CSV file operations (built-in).
- **collections module**: Used for handling data structures efficiently.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/log-analysis-web-app.git
   cd log-analysis-web-app
