import logging
import requests
from typing import Collection

logger = logging.getLogger(__name__)

API_TOKEN = "your_api_token_here"  # Replace with your actual API token if needed

def check_urls(urls: Collection[str], timeout: int = 5) -> dict[str, str]:
    """Check the status of a list of URLs.

    Args:
        urls (list[str]): A list of URLs to check.
        timeout (int, optional): The timeout for the HTTP request in seconds. Defaults to 5.

    Returns:
        dict[str, str]: A dictionary mapping each URL to its status ("OK" or "ERROR").
    """

    logger.info(f"Starting check for {len(urls)} URLs with a timeout of {timeout} seconds.")
    results: dict[str, str] = {}

    for url in urls:
        status = "UNKNOWN"

        try:
            logger.debug(f"Checking URL: {url}")
            response = requests.get(url, timeout=timeout)
            if response.ok:
                status = f"{response.status_code} OK"
            else:
                status = f"{response.status_code} {response.reason}"
        except requests.exceptions.Timeout:
            status = "TIMEOUT"
            logger.warning(f"Timeout occurred while checking URL: {url}")
        except requests.exceptions.ConnectionError:
            status = "CONNECTION ERROR"
            logger.warning(f"Connection error occurred while checking URL: {url}")
        except requests.exceptions.RequestException as e:
            status = f"REQUEST_ERROR: {type(e).__name__}"
            logger.error(f"An error occurred while checking URL: {url} - {str(e)}, exc_info=True")

        results[url] = status
        logger.debug(f"Checked URL: {url:<40} -> Status: {status}")

    logger.info("Completed checking URLs.")
    return results
