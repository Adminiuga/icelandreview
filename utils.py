import datetime
import requests


def get_date_range() -> str:
    """
    Returns the date for the query to the wordpress server in ISO8601 format
    """
    return (datetime.datetime.now() - datetime.timedelta(days=30)).isoformat()


def get_page_range() -> int:
    """
    Returns the number of pages
    """
    return 100


def get_posts(url: str) -> dict:
    """
    Does the actual querying
    """
    response = requests.get(url, params={'after': get_date_range(), 'per_page': get_page_range()})
    return response.json()
