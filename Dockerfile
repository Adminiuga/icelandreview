FROM python:3.7-alpine

ENV \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PORT=5000

EXPOSE $PORT

# -- Install Application into container:
RUN set -ex && mkdir /app

WORKDIR /app

# -- Add requirements.txt
COPY requirements.txt requirements.txt

# -- Install dependencies:
RUN set -ex && pip install -r requirements.txt

COPY . /app

CMD [ "python3", "main.py", "$PORT" ]
