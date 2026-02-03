#!/usr/bin/python3

import os
import http.cookies

# Session handling
session_dir = "/tmp/python_sessions"
cookie = http.cookies.SimpleCookie()
cookie_header = os.environ.get("HTTP_COOKIE", "")
cookie.load(cookie_header)

# Delete the session file if it exists
if "PYTHON_SID" in cookie:
    session_id = cookie["PYTHON_SID"].value
    session_file = os.path.join(session_dir, session_id + ".json")
    if os.path.exists(session_file):
        os.remove(session_file)

# Expire the cookie by setting max-age to 0
print("Set-Cookie: PYTHON_SID=; max-age=0; path=/")
print("Cache-Control: no-cache")
print("Content-Type: text/html\n")

print("""<!DOCTYPE html>
<html><head><title>State - Session Cleared</title></head>
<body>
<h1 align="center">Session Cleared</h1><hr>
<p>Your session data has been deleted.</p>
<p><a href="/cgi-bin/python/state-python-save.py">Back to Save Page</a></p>
<p><a href="/cgi-bin/python/state-python-view.py">Back to View Page</a></p>
</body></html>""")
