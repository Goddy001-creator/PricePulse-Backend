import requests

from app.config.settings import SCRAPER_TIMEOUT


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_page(url):
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=SCRAPER_TIMEOUT
    )

    response.raise_for_status()

    return response
