import base64
import json

# Open the "secrets.json" file in read mode
with open("secrets.json", "r") as f:
    # Load the JSON data from the file into a Python object
    data = json.load(f)

# Convert the Python object directly to a JSON string and then encode it as a base64 string
base64_string = base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")

# Print the base64-encoded string
print(base64_string)
