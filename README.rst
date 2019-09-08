|Actions Status| |Coveralls| |Updates|

icelandreview
=============

This is a Docker container that scrapes the JSON endpoint on icelandreview.com to generate an Atom feed to allow you to read it in the RSS/Atom reader of your choice.

Running
-------

The application is builton Flask, and can simply be run using ``python main.py``. 
The application uses Python 3.6. This version of Python is used since the Zappa_ library doesn't support 3.7.

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

AWS Lambda
^^^^^^^^^^

We use Zappa_ to deploy and manage the application on AWS Lambda.

Tocreate the application and deploy just run the following:

.. code-block:: bash

    # to initialise the first time
    $ zappa init
    # to deploy the first time
    $ zappa deploy dev
    # to update subsequently
    $ zappa update dev

The settings for the application on AWS Lambda are stored in ``zappa_settings.json``

.. |Actions Status| image:: https://github.com/aodj/icelandreview/workflows/pytest/badge.svg
.. |Updates| image:: https://pyup.io/repos/github/aodj/icelandreview/shield.svg
    :target: https://pyup.io/repos/github/aodj/icelandreview/
    :alt: Updates
.. |Coveralls| image:: https://coveralls.io/repos/github/aodj/icelandreview/badge.svg?branch=HEAD
    :target: https://coveralls.io/github/aodj/icelandreview?branch=HEAD
.. _Zappa: https://github.com/Miserlou/Zappa