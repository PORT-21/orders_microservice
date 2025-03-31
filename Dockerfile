FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /application/src/

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev gettext libmagic-dev libjpeg-dev zlib1g-dev git && \
    apt-get purge -y --auto-remove -o APT:AutoRemove:RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/* && \
    apt install vim

COPY ./ requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "cd", "/application/src/", "&&", "python", "./entrypoints/run.py"]
