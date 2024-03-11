import collections
import json
import os
from typing import Any, DefaultDict, Generator, List, NamedTuple, Set

import colorama
import networkx
from _pytest.nodes import Item

from .constants import MARKER_KWARG_DEPENDENCIES, MARKER_NAME
from .graphs import graph_interactive_network
from .util import clean_nodeid, get_absolute_nodeid, get_markers, get_name

