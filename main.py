"""
Feed generator for icelandreview.com

All arguments found here https://www.icelandreview.com/wp-json/
"""

import os
import datetime

from apscheduler.events import EVENT_JOB_EXECUTED
from flask import Flask, request, url_for
from flask_apscheduler import APScheduler
from werkzeug.contrib.atom import AtomFeed, FeedEntry

from utils import get_posts, get_age, parse_datetime, remove_macro_tags


app = Flask(__name__)
url = 'https://www.icelandreview.com/wp-json/wp/v2/posts'
posts = {}


def update_posts():
    global posts
    posts = get_posts(url)


def update_posts_from_event(event):
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
        id=post['guid']['rendered'],
        title=post['title']['rendered'],
        content=remove_macro_tags(post['content']['rendered']),
        summary=remove_macro_tags(post['excerpt']['rendered']),
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
    atom = AtomFeed('Iceland Review', feed_url=feed_url, author='Iceland Review',
        icon='https://www.icelandreview.com/wp-content/uploads/2018/06/ir-32x32.png')
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
    return '''<html><a href="{}">Atom Feed</a><br />{}</html>'''.format(url_for('recent_feed'), content)


@app.route('/atom.xml')
def recent_feed():  # pragma: no cover
    atom = get_feed(feed_url=request.url)
    return atom.get_response()


if __name__ == '__main__':  # pragma: no cover
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

    app.config.from_object(Config())

    flask_scheduler = APScheduler()
    flask_scheduler.init_app(app)
    flask_scheduler.start()

    flask_scheduler.add_listener(update_posts_from_event, EVENT_JOB_EXECUTED)

    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
