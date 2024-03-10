"""Model definitions for use in the API"""

from datetime import datetime
from pydantic import BaseModel, constr, Field
from typing import List, Dict, Optional

datetime_format = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:0
