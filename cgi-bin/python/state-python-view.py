#!/usr/bin/python3

import os
import http.cookies
import json

# Session handling
session_dir = "/tmp/python_sessions"
cookie = http.cookies.SimpleCookie()
cookie_header = os.environ.get("HTTP_COOKIE", "")
cookie.load(cookie_header)

session_data = {}
if "PYTHON_SID" in cookie:
    session_id = cookie["PYTHON_SID"].value
    session_file = os.path.join(session_dir, session_id + ".json")
    if os.path.exists(session_file):
        with open(session_file, "r") as f:
            session_data = json.load(f)

print("Cache-Control: no-cache")
print("Content-Type: text/html\n")

print("""<!DOCTYPE html>
<html><head><title>State - View Data</title></head>
<body>
<h1 align="center">State Demo - View Data</h1><hr>""")

if session_data:
    print(f"<p><b>Name:</b> {session_data.get('name', 'N/A')}</p>")
    print(f"<p><b>Message:</b> {session_data.get('message', 'N/A')}</p>")
    print(f"<p><b>Saved at:</b> {session_data.get('saved_at', 'N/A')}</p>")
else:
    print("<p>No data saved yet. Go save some!</p>")

print("""<hr>
<p><a href="/cgi-bin/python/state-python-save.py">Go back and edit</a></p>
<p><a href="/cgi-bin/python/state-python-destroy.py">Clear session</a></p>
</body></html>""")
