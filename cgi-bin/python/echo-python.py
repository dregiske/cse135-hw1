#!/usr/bin/python3
import os
import sys
from urllib.parse import parse_qs, unquote_plus
import json
from datetime import datetime
import socket

print("Cache-Control: no-cache")
print("Content-Type: text/html\n")

# Read request info from environment
method = os.environ.get("REQUEST_METHOD", "UNKNOWN")
query_string = os.environ.get("QUERY_STRING", "")
content_length = int(os.environ.get("CONTENT_LENGTH", 0) or 0)
content_type = os.environ.get("CONTENT_TYPE", "")
user_agent = os.environ.get("HTTP_USER_AGENT", "unknown")
remote_addr = os.environ.get("REMOTE_ADDR", "unknown")
hostname = socket.gethostname()

# Read the message body from stdin (for POST/PUT)
body = ""
if content_length > 0:
    body = sys.stdin.read(content_length)

# Parse the data depending on where it came from
parsed_data = {}
if method == "GET":
    parsed_data = parse_qs(query_string)
elif method in ("POST", "PUT", "DELETE"):
    if "application/json" in content_type:
        try:
            parsed_data = json.loads(body)
        except json.JSONDecodeError:
            parsed_data = {"error": "Invalid JSON"}
    else:
        parsed_data = parse_qs(body)

# Print HTML
print("""<!DOCTYPE html>
<html><head><title>Echo Request</title>
</head><body><h1 align="center">Echo Request</h1>
<hr>""")

# Metadata
print(f"<p><b>Hostname:</b> {hostname}</p>")
print(f"<p><b>Date/Time:</b> {datetime.now()}</p>")
print(f"<p><b>User Agent:</b> {user_agent}</p>")
print(f"<p><b>IP Address:</b> {remote_addr}</p>")
print("<hr>")

# Request details
print(f"<p><b>HTTP Method:</b> {method}</p>")
print(f"<p><b>Content-Type:</b> {content_type}</p>")
print(f"<p><b>Query String:</b> {query_string}</p>")
print(f"<p><b>Message Body:</b> {body}</p>")

# Parsed fields
print("<hr>")
print("<h2>Parsed Data</h2>")
if parsed_data:
    print("<ul>")
    for key, value in parsed_data.items():
        print(f"<li><b>{key}:</b> {value}</li>")
    print("</ul>")
else:
    print("<p>No data to parse.</p>")

print("</body></html>")
