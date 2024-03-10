import contextlib
import json
import os
import re
from io import BytesIO
from typing import Any, Dict, List, Union
from urllib.parse import urlparse, urlunparse

import vcr
from vcr.request import Request
from vcr.response import Response

