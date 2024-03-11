import json
import logging
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pyvis.network import Network

from agbenchmark.generate_test import DATA_CATEGORY
from agbenchmark.utils.utils import write_pretty_json  # Importing the write_pretty_json utility function

# Initialize the logger with the name of the current module
logger = logging.getLogger(__name__)


