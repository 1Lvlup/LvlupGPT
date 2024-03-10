import os
import pathlib

import pytest


@pytest.fixture
def workspace():
    return pathlib.Path().absolute()

