import base64
import json
import os
import re
from datetime import datetime, timedelta

import gspread
import pandas as pd
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# Load the base64-encoded service account credentials from the environment variable
load_dotenv()
base64_creds = os.getenv("GDRIVE_BASE64")
if not base6
