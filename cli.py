"""
This is a minimal file intended to be run by users to help them manage the autogpt projects.

If you want to contribute, please use only libraries that come as part of Python.
To ensure efficiency, add the imports to the functions so only what is needed is imported.
"""

import os  # This module provides a way of using operating system dependent functionality
import subprocess  # This module allows the running of operating system commands
import click  # This module provides a simple way to write command line interfaces
import socket  # This module provides low-level networking interface
from datetime import datetime  # This module supplies classes for manipulating dates and times
import requests  # This module allows you to send HTTP/1.1 requests

try:
    # Importing PyGithub module, which is used for interacting with GitHub's API
    import github
except ImportError:
    # Display an error message if PyGithub module is not found
    click.echo(
        click.style(
            "😞 Missing dependency: PyGithub. Please install it by running 'pip3 install PyGithub'.",
            fg="red",
        )
    )
    # Exit the program with a status code of 1
    exit(1)

def wait_until_conn_ready(port: int = 8000):
    """
    Wait until a connection can be established on the specified port.

    :param port: The port number to wait for a connection on. Defaults to 8000.
    """
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a specific address and port
    sock.bind(('', port))
    # Start listening for connections
    sock.listen(1)
    # Continuously try to accept a connection
    while True:
        try:
            # Attempt to accept a connection
            connection, client_address = sock.accept()
            # If successful, close the socket and exit the function
            connection.close()
            sock.close()
            break
        except socket.
