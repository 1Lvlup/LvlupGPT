import functools
import re
from typing import Any, Callable, ParamSpec, TypeVar, Union
from urllib.parse import urljoin, urlparse

P = ParamSpec("P")
T = TypeVar("T")
UrlType = Union[str, "Url"]

class Url:
    def __init__(self, url: str):
        self.url = url
        self._parsed_url = urlparse(url)

    def __str__(self):
        return self.url

    def __eq__(self, other):
        if isinstance(other, Url):
            return self.url == other.url
        return self.url == other

def validate_url(func: Callable[[UrlType], T]) -> Callable[[UrlType], T]:
    """
    The method decorator validate_url is used to validate urls for any command that
    requires a url as an argument.
    """

    @functools.wraps(func)
    def wrapper(url: UrlType) -> Any:
        url = _validate_and_sanitize_url(url)
        return func(url)

    return wrapper

def _validate_and_sanitize_url(url: UrlType) -> Url:
    """Check if the URL is valid and not a local file accessor, and sanitize it.

    Returns:
        Url: The validated and sanitized URL

    Raises:
        ValueError if the url fails any of the validation tests
    """
    if not isinstance(url, Url):
        url = Url(url)

    # Most basic check if the URL is valid:
    if not re.match(r"^https?://", url.url):
        raise ValueError("Invalid URL format")
    if not _is_valid_url(url.url):
        raise ValueError("Missing Scheme or Network location")
    # Restrict access to local files
    if _check_local_file_access(url.url):
        raise ValueError("Access to local files is restricted")
    # Check URL length
    if len(url.url) > 2000:
        raise ValueError("URL is too long")

    return url

def _is_valid_url(url: str) -> bool:
    """Check if the URL is valid

    Args:
        url (str): The URL to check

    Returns:
        bool: True if the URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def _sanitize_url(url: str) -> str:
    """Sanitize the URL

    Args:
        url (str): The URL to sanitize

    Returns:
        str: The sanitized URL
    """
    parsed_url = urlparse(url)
    reconstructed_url = f"{parsed_url.path}{parsed_url.params}?{parsed_url.query}"
    return urljoin(url, reconstructed_url)

def _check_local_file_access(url: str) -> bool:
    """Check if the URL is a local file

    Args:
        url (str): The URL to check

    Returns:
        bool: True if the URL is a local file, False otherwise
    """
    # List of local file prefixes
    local_file_prefixes = [
        "file:///",
        "file://localhost",
    ]

    return any(url.startswith(prefix) for prefix in local_file_prefixes)
