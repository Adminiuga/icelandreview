"""
Feed generator for icelandreview.com

All arguments found here https://www.icelandreview.com/wp-json/
"""

import os
import datetime

from apscheduler.events import EVENT_JOB_EXECUTED
from flask import Flask, request, url_for, jsonify
from flask_apscheduler import APScheduler
import werkzeug
from werkzeug.contrib.atom import AtomFeed, FeedEntry

from utils import get_posts, get_age, parse_datetime

url = 'https://www.icelandreview.com/wp-json/wp/v2/posts'


class Config(object):
    SCHEDULER_JOBS = [
        # trigger for hourly updates
        {
            'id': 'hourly',
            'func': get_posts,
            'kwargs': {'url': url},
            'trigger': 'interval',
            'hours': 1
        },
        # trigger to run immediately for initial state
        {
            'id': 'immediate',
            'func': get_posts,
            'kwargs': {'url': url}
        }
    ]
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config())
posts = {}


def update_posts(event):
    """
    Updates the global posts dict with the latest scraped values from the website
    """
    global posts
    posts = event.retval


def get_feed_item(post: dict) -> FeedEntry:
    """
    Returns a FeedEntry object for adding to an AtomFeed item from the werkzeug.contrib.atom
    module

    Args:
        post (dict): post dict from the parser

    Returns:
        FeedEntry: item for the atom feed

    """
    return FeedEntry(
        title=post['title']['rendered'],
        content=post['excerpt']['rendered'],
        content_type='html',
        url=post['link'],
        updated=parse_datetime(post['modified_gmt']),
        published=parse_datetime(post['date_gmt'])
    )


def get_feed(feed_url: str) -> AtomFeed:
    """
    Creates an AtomFeed, appending the given posts to it, and then returns the instance

    Args:
        feed_url (str): url for the feed

    Returns:
        AtomFeed: Atom rss feed instance

    """
    atom = AtomFeed('Iceland Review', feed_url=feed_url)
    for post in posts:
        atom.add(get_feed_item(post))

    return atom


@app.route('/')
def root():  # pragma: no cover
    today = datetime.date.today()
    content = '<div>'
    for post in posts:
        content += '<br />{age}<a href="{url}">{title}</a>'.format(
            age=get_age(today, parse_datetime(post['date_gmt'])),
            url=post['link'],
            title=post['title']['rendered']
        )
    content += '</div>'
    return '''<html><a href="atom.xml">Atom Feed</a><br />{}</html>'''.format(content)


@app.route('/atom.xml')
def recent_feed():  # pragma: no cover
    atom = get_feed(feed_url=request.url)
    return atom.get_response()


if __name__ == '__main__':  # pragma: no cover
    flask_scheduler = APScheduler()
    flask_scheduler.init_app(app)
    flask_scheduler.start()

    flask_scheduler.add_listener(update_posts, EVENT_JOB_EXECUTED)

    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
