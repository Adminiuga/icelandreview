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

    Args:
        url (str): the url to request

    Returns:
        dict: the parsed json response from the url

    """
    response = requests.get(url, params={'after': get_date_range(), 'per_page': get_page_range()})
    return response.json()


def get_age(now: datetime.date, then: datetime.datetime):
    """
    Returns the number of days between "now" and "then"

    Args:
        now (datetim.date): today's date
        then: (datetime.datetime): posted datetime for the post

    Returns:
        int: number of days between the two dates

    """
    return (now-then.date()).days
