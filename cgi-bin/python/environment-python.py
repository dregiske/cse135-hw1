#!/usr/bin/python3
import os

print("Cache-Control: no-cache")
print("Content-Type: text/html\n")

# print HTML file top
print("""<!DOCTYPE html>
<html><head><title>Environment Variables</title>
</head><body><h1 align="center">Environment Variables</h1>
<hr>""")

# Loop over the environment variables and print each variable and its value
for key in sorted(os.environ.keys()):
  print(f"<b>{key}:</b> {os.environ[key]}<br />")

# Print the HTML file bottom
print("</body></html>")
