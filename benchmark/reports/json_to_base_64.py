import base64
import json

with open("secrets.json", "r") as f:
    data = json.load(f)

# Convert the JSON object directly to a base64 string in one line
base64_string = base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")

print(base64_string)
