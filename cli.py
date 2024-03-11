"""
This is a minimal file intended to be run by users to help them manage the autogpt projects.

If you want to contribute, please use only libraries that come as part of Python.
To ensure efficiency, add the imports to the functions so only what is needed is imported.
"""
import os
import subprocess
import click
import socket
from datetime import datetime
import requests

try:
    import github
except ImportError:
    click.echo(
        click.style(
            "😞 Missing dependency: PyGithub. Please install it by running 'pip3 install PyGithub'.",
            fg="red",
        )
    )
    exit(1)


def wait_until_conn_ready(port: int = 800
