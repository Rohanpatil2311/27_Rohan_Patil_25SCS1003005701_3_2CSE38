# API Performance Monitor

**Student:** Rohan Patil
**Roll No.:** 25SCS1003005701
**Internship:** Python Developer Intern
**Organization:** Codec Technologies Pvt. Ltd.

## Project objective
Monitor API response times and HTTP status codes, record successful/failed requests in SQLite, and present performance metrics through a Flask dashboard.

## Technologies
- Python
- Flask
- Requests
- SQLite
- HTML/CSS/JavaScript

## Features
- Test any HTTP/HTTPS GET endpoint
- Measure response time in milliseconds
- Capture HTTP status code
- Mark requests as successful/failed
- Persist logs in SQLite
- Calculate average, fastest and slowest response time
- Calculate success rate
- View recent checks in a web dashboard

## Run on Windows
Open a terminal in this folder:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py

Then open:
http://127.0.0.1:5000

For a demo endpoint, use:
https://httpbin.org/get

Note: Internet access is required for live API testing.
