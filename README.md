Here's the updated README:

---

# Log Analysis Web Application

## Project Overview

This project is a web application built with Flask to generate and analyze log files. The logs simulate user requests to a web server, containing IP addresses, endpoints, status codes, and messages. The primary goal is to provide insights into web traffic, detect suspicious activity, and present statistics in a user-friendly format.

## Features

- **Log Generation**: Create custom log files with random IP addresses, endpoints, and status codes.
- **Log Analysis**:
  - Count requests per IP address.
  - Identify the most accessed endpoint.
  - Detect suspicious activity, such as failed login attempts (e.g., "Invalid credentials").
- **Web Interface**: Intuitive interface to upload, preview, and analyze logs.
- **CSV Export**: Export analysis results into a downloadable CSV file.

---

## Project Structure

- **`app.py`**: Handles routing, log generation, and integration with the analysis module.
- **`log_analysis.py`**: Script to analyze logs and generate detailed outputs:
  - Requests per IP.
  - Most accessed endpoint.
  - Suspicious activity (failed login attempts).  
  Results are displayed in the terminal and saved as `log_analysis_results.csv`.
- **`index.html`**: Homepage for uploading or generating logs.
- **`preview.html`**: Displays the content of a generated log file before analysis.
- **`results.html`**: Displays the results of log analysis, including suspicious IPs, total requests, and endpoint statistics.
- **`style.css`**: Custom styles for the web application.

---

## Requirements

- **Python 3.x**
- **Flask**: Web framework.
- **CSV module**: For handling CSV operations (built-in).
- **Collections module**: Efficient data structures.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/log-analysis-web-app.git
   cd log-analysis-web-app
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: `env\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install flask
   ```

4. Run the application:

   ```bash
   python app.py
   ```

---

## Usage

1. Access the web application at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).
2. Choose to either:
   - Upload an existing log file using the "Upload Log" option.
   - Generate a new log file using the "Generate Log" option.
3. Preview the log to ensure correctness.
4. Analyze the log to view:
   - Requests per IP address.
   - Most accessed endpoint.
   - Suspicious activity (e.g., IPs with failed login attempts).
5. Download the analysis results as a CSV file for further review.

---

## Example Log Format

Each log entry is structured as follows:

```plaintext
<IP> - - [<Date>] "GET /<Endpoint> HTTP/1.1" <Status Code> "<Message>"
```

### Example Log:

```plaintext
192.168.1.1 - - [08/Dec/2024:12:34:56 +0000] "GET /login HTTP/1.1" 401 "Invalid credentials"
```

---

## Output Details

- **Requests per IP**:
  - Displays the number of requests made by each IP in descending order.
- **Most Accessed Endpoint**:
  - Shows the endpoint with the highest access count.
- **Suspicious Activity**:
  - Lists IPs with failed login attempts exceeding a threshold (default: 10 attempts).

---
