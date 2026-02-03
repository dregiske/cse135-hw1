#!/usr/bin/python3
print("Cache-Control: no-cache")
print("Content-Type: text/html\n")

print("<!DOCTYPE html>")
print("<html>")
print("<head>")
print("<title>Hello CGI World</title>")
print("</head>")
print("<body>")

print("<h1 align=center>Hello HTML World</h1><hr/>")
print("<p>Hello Andre!</p>")
print("<p>This page was generated with the Python programming language</p>")

import datetime
date = datetime.datetime.now()
print(f"<p>This program was generated at: {date}</p>")

# IP Address is an environment variable when using CGI
import os
address = os.environ.get("REMOTE_ADDR", "unknown")
print(f"<p>Your current IP Address is: {address}</p>")

print("</body>")
print("</html>")
