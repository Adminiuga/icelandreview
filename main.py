"""
Feed generator for icelandreview.com

All arguments found here https://www.icelandreview.com/wp-json/
"""

import os
from apscheduler.events import EVENT_JOB_EXECUTED
from flask import Flask, request, url_for, jsonify
from flask_apscheduler import APScheduler

import werkzeug
from utils import get_posts

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
    global posts
    posts = event.retval


@app.route('/')
def root():
    return jsonify(posts)


if __name__ == '__main__':  # pragma: no cover
    flask_scheduler = APScheduler()
    flask_scheduler.init_app(app)
    flask_scheduler.start()

    flask_scheduler.add_listener(update_posts, EVENT_JOB_EXECUTED)

    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
