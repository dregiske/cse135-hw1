#!/usr/bin/python3

import os
import sys
import http.cookies
import json
import uuid
import tempfile
from datetime import datetime

# Session handling
session_dir = "/tmp/python_sessions"
os.makedirs(session_dir, exist_ok=True)

cookie = http.cookies.SimpleCookie()
cookie_header = os.environ.get("HTTP_COOKIE", "")
cookie.load(cookie_header)

# Get or create session ID
if "PYTHON_SID" in cookie:
    session_id = cookie["PYTHON_SID"].value
else:
    session_id = str(uuid.uuid4())

session_file = os.path.join(session_dir, session_id + ".json")

# Read existing session data
session_data = {}
if os.path.exists(session_file):
    with open(session_file, "r") as f:
        session_data = json.load(f)

# Check if form was submitted (POST)
method = os.environ.get("REQUEST_METHOD", "GET")
if method == "POST":
    content_length = int(os.environ.get("CONTENT_LENGTH", 0) or 0)
    body = sys.stdin.read(content_length)
    from urllib.parse import parse_qs
    form_data = parse_qs(body)
    if "name" in form_data:
        session_data["name"] = form_data["name"][0]
    if "message" in form_data:
        session_data["message"] = form_data["message"][0]
    session_data["saved_at"] = str(datetime.now())
    with open(session_file, "w") as f:
        json.dump(session_data, f)

# Set cookie and print headers
print(f"Set-Cookie: PYTHON_SID={session_id}; path=/")
print("Cache-Control: no-cache")
print("Content-Type: text/html\n")

print(f"""<!DOCTYPE html>
<html><head><title>State - Save Data</title></head>
<body>
<h1 align="center">State Demo - Save Data</h1><hr>
<form method="POST" action="/cgi-bin/python/state-python-save.py">
    <label>Name: </label><input type="text" name="name" value="{session_data.get('name', '')}"  /><br /><br />
    <label>Message: </label><input type="text" name="message" value="{session_data.get('message', '')}" /><br /><br />
    <input type="submit" value="Save" />
</form>
<hr>
<p><a href="/cgi-bin/python/state-python-view.py">View saved data</a></p>
<p><a href="/cgi-bin/python/state-python-destroy.py">Clear session</a></p>
</body></html>""")
