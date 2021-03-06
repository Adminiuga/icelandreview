import datetime
import re
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
    response = requests.get(url, params={"after": get_date_range(), "per_page": get_page_range()})
    return response.json()


def get_age(now: datetime.date, then: datetime.datetime):
    """
    Returns the number of days between "now" and "then"

    Args:
        now (datetime.date): today's date
        then: (datetime.datetime): posted datetime for the post

    Returns:
        int: number of days between the two dates

    """
    return (now - then.date()).days


def parse_datetime(input: str) -> datetime.datetime:
    """
    Replaces cis8601.parse_datetime that was in use before.
    Returns a datetime.datetime object parsed from the input string.

    Args:
        input (str): timestamp

    Returns:
        datetime.datetime: parsed datetime object

    """
    return datetime.datetime.strptime(input, "%Y-%m-%dT%H:%M:%S")


def remove_macro_tags(text: str) -> str:
    """
    Removes the WordPress macros that sometimes appear in the rendered output
    such as `[vc_row]`. Also replaces the `mk_image` macro with an img tag to
    show the images in the output.

    Args:
        text (str): the text to strip
    
    Returns:
        str: stripped text
    
    """
    fix_images = re.sub(r"\[mk_image[^\;]+\;([^\&]+)[^\]]+\]", r'\n<img src="\1">\n', text)
    return re.sub(r"\[\/?(vc|mk)[^\]]+\]", "", fix_images)
