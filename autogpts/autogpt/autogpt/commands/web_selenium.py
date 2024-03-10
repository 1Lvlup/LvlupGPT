"""Commands for browsing a website"""

import asyncio
import logging
import re
from pathlib import Path
from sys import platform
from typing import Optional
from urllib.request import urlretrieve

import bs4
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeDriverService
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import ArgOptions as BrowserOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeDriverService
from selenium.webdriver.edge.webdriver import WebDriver as EdgeDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as GeckoDriverService
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.safari.webdriver import WebDriver as SafariDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager as EdgeDriverManager

from autogpt.agents.utils.exceptions import CommandExecutionError, TooMuchOutputError
from autogpt.command_decorator import command
from autogpt.core.utils.json_schema import JSONSchema
from autogpt.processing.html import extract_hyperlinks, format_hyperlinks
from autogpt.processing.text import extract_information, summarize_text
from autogpt.url_utils.validators import validate_url

COMMAND_CATEGORY = "web_browse"
COMMAND_CATEGORY_TITLE = "Web Browsing"

logger = logging.getLogger(__name__)
FILE_DIR = Path(__file__).parent.parent
MAX_RAW_CONTENT_LENGTH = 500
LINKS_TO_RETURN = 20

BROWSER_OPTIONS = {
    "chrome": ChromeOptions,
    "edge": EdgeOptions,
    "firefox": FirefoxOptions,
    "safari": SafariOptions,
}


async def open_page_in_browser(url: str, config: dict) -> WebDriver:
    options: BrowserOptions = BROWSER_OPTIONS[config["browser"]]()
    options.add_argument(f"user-agent={config['user_agent']}")

    if options.__class__ is FirefoxOptions:
        if config["headless"]:
            options.headless = True
            options.add_argument("--disable-gpu")
        driver = FirefoxDriver(
            service=GeckoDriverService(GeckoDriverManager().install()), options=options
        )
    elif options.__class__ is EdgeOptions:
        driver = EdgeDriver(
            service=EdgeDriverService(EdgeDriverManager().install()), options=options
        )
    elif options.__class__ is SafariOptions:
        driver = SafariDriver(options=options)
    elif options.__class__ is ChromeOptions:
        if platform == "linux" or platform == "linux2":
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--remote-debugging-port=9222")

        options.add_argument("--no-sandbox")
        if config["headless"]:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

        _sideload_chrome_extensions(options, Path(config["app_data_dir"]) / "assets" / "crx")

        if (chromium_driver_path := Path("/usr/bin/chromedriver")).exists():
            chrome_service = ChromeDriverService(str(chromium_driver_path))
        else:
            try:
                chrome_driver = ChromeDriverManager().install()
            except AttributeError as e:
                if "'NoneType' object has no attribute 'split'" in str(e):
                    logger.critical(
                        "Connecting to browser failed: is Chrome or Chromium installed?"
                    )
                raise
            chrome_service = ChromeDriverService(chrome_driver)
        driver = ChromeDriver(service=chrome_service, options=options)

    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    await asyncio.sleep(2)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    return driver


@command(
    "read_webpage",
    (
        "Read a webpage, and extract specific information from it."
        " You must specify either topics_of_interest, a question, or get_raw_content."
