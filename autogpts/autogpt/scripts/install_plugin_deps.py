import logging
import os
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)

def initialize_logger():
    """Initialize the logger with a custom format and a file handler."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler("install_deps.log"), logging.StreamHandler()],
    )

def file_exists(path):
    """Check if a file exists."""
    return path.exists() and not path.is_dir()

def install_plugin_dependencies():
    """
    Installs dependencies for all plugins in the plugins dir.

    Args:
        None

    Returns:
        None
    """
    plugins_dir = Path(os.getenv("PLUGINS_DIR", "plugins"))

    if not plugins_dir.exists():
        logger.error(f"The plugins directory '{plugins_dir}' does not exist.")
        return

    initialize_logger()

    logger.debug("Checking for dependencies in zipped plugins...")

    # Install zip-based plugins
    for plugin_archive in plugins_dir.glob("*.zip"):
        if not file_exists(plugin_archive):
            continue

        logger.debug(f"Checking for requirements in '{plugin_archive}'...")
        with zipfile.ZipFile(plugin_archive, "r") as zfile:
            if not zfile.namelist():
                continue

            # Assume the first entry in the list will be (in) the lowest common dir
            first_entry = zfile.namelist()[0]
            basedir = first_entry.rsplit("/", 1)[0] if "/" in first_entry else ""
            logger.debug(f"Looking for requirements.txt in '{basedir}'")

            basereqs = os.path.join(basedir, "requirements.txt")
            try:
                extracted = zfile.extract(basereqs, path=plugins_dir)
            except KeyError as e:
                logger.debug(e.args[0])
                continue

            if not file_exists(extracted):
                logger.warning(f"Requirements file '{basereqs}' not found in the zip file.")
                continue

            logger.debug(f"Installing dependencies from '{basereqs}'...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", extracted]
            )
            os.remove(extracted)
            os.rmdir(os.path.join(plugins_dir, basedir))

    logger.debug("Checking for dependencies in other plugin folders...")

    # Install directory-based plugins
    for requirements_file in plugins_dir.glob("*/requirements.txt"):
        if not file_exists(requirements_file):
            continue

        logger.debug(f"Installing dependencies from '{requirements_file}'..."
