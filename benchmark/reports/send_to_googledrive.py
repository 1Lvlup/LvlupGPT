import base64
import json
import os
import re
from datetime import datetime, timedelta

import gspread
import pandas as pd
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
base64_creds = os.getenv("GDRIVE_BASE64")
if not base64_creds:
    raise ValueError("The GDRIVE_BASE64 environment variable is not set")

creds_bytes = base64.b64decode(base64_creds)
creds_string = creds_bytes.decode("utf-8")
creds_info = json.loads(creds_string)

base_dir = "reports"
if os.path.abspath(os.getcwd()) == os.path.abspath(base_dir):
    base_dir = "/"

def process_test(test_name, test_info, agent_name, common_data):
    # ... (same as before)

def process_reports(base_dir):
    rows = []
    for agent_dir in os.listdir(base_dir):
        agent_dir_path = os.path.join(base_dir, agent_dir)
        if not os.path.isdir(agent_dir_path):
            continue

        for report_folder in os.listdir(agent_dir_path):
            report_folder_path = os.path.join(agent_dir_path, report_folder)
            if not os.path.isdir(report_folder_path):
                continue

            report_path = os.path.join(report_folder_path, "report.json")
            if not os.path.exists(report_path):
                continue

            with open(report_path, "r") as f:
                data = json.load(f)

            benchmark_start_time = data.get("benchmark_start_time", "")
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00", benchmark_start_time):
                continue

            benchmark_datetime = datetime.strptime(benchmark_start_time, "%Y-%m-%dT%H:%M:%S+00:00")
            current_datetime = datetime.utcnow()
            if current_datetime - benchmark_datetime > timedelta(days=3):
                continue

            for test_name, test_info in data["tests"].items():
                process_test(test_name, test_info, agent_dir, data)

    return rows

rows = process_reports(base_dir)
df = pd.DataFrame(rows)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_info, scope)
client = gspread.authorize(creds)

branch_name = os.getenv("GITHUB_REF_NAME")
sheet = client.open(f"benchmark-{branch_name}")
sheet_instance = sheet.get_worksheet(0)

values = df.values.tolist()
values.insert(0, df.columns.tolist())
sheet_instance.clear()
sheet_instance.append_rows(values)
