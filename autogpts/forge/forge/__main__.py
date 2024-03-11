import os  # Importing the os module for interacting with the operating system

import uvicorn  # FastHTTP server implementation for ASGI applications
from dotenv import load_dotenv  # Load environment variables from .env file

import forge.sdk.forge_log  # Importing custom logging module

# Initialize the logger
LOG = forge.sdk.forge_log.ForgeLogger(__name__)

# The ASCII art logo for the application
logo = """
...
"""

if __name__ == "__main__":  # Check if the script is run directly
    print(logo)  # Print the ASCII art logo

    # Get the environment variable 'PORT' with a default value of 8000
    port = os.getenv("PORT", 8000)
    LOG.info(f"Agent server starting on http://localhost:{port}")

    # Load environment variables from .env file
    load_dotenv()

    # Configure the custom logger
    forge.sdk.forge_log.setup_logger()

    uvicorn.run(
        "forge.app:app",  # The ASGI application (wsgi.py:app)
        host="localhost",  # The host to bind the server to
        port=int(port),  # The port to bind the server to
        log_level="error",  # The log level for the server

        # Reload the server on code or .env file changes
        reload=True,
        reload_dirs=os.path.dirname(os.path.dirname(__file__)),  # Directory to watch for changes
        reload_excludes="*.py",  # File pattern to exclude from watching
        reload_includes=[
            f"{os.path.basename(os.path.dirname(__file__))}/**/*.py",  # Include pattern for .py files
            ".*",  # Include pattern for .env files
            ".env",  # Include pattern for .env files
        ],
    )
