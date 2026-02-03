#!/usr/bin/python3
import json
import os
from datetime import datetime

print("Cache-Control: no-cache\n")
print("Content-type: application/json\n\n")

date = datetime.now()
address = os.environ.get('REMOTE_ADDR', 'Unknown')

message = {
    "title": "Hello, Python!",
    "heading": "Hello, Python!",
    "message": "This page was generated with the Python programming language",
    "time": str(date),
    "IP": address
}

json_string = json.dumps(message)
print(json_string)
