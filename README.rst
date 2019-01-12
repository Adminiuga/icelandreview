|Updates|

icelandreview
=============

This is a Docker container that scrapes the JSON endpoint on icelandreview.com to generate an Atom feed to allow you to read it in the RSS/Atom reader of your choice.

Running
-------

The application is builton Flask, and can simply be run using ``python main.py``. 
The application uses Python 3.7.

Deploying
---------

Docker 
^^^^^^

Build the Docker image using ``docker build -t icelandreview .``

Heroku
^^^^^^

The Docker image can be run on Herkou using the following commands:

.. code-block:: bash

    $ heroku login
    $ heroku container:login
    $ heroku container:push web
    $ heroku container:release web

.. |Updates| image:: https://pyup.io/repos/github/aodj/icelandreview/shield.svg
    :target: https://pyup.io/repos/github/aodj/icelandreview/
    :alt: Updates