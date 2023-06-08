FROM python:3.11
LABEL version='1.0' maintainer='guyabihanna@gmail.com'

RUN apt-get update && apt-get install -y ca-certificates wget

RUN pip3 install --upgrade pip
RUN pip3 install poetry==1.4.1 && poetry config virtualenvs.create false

RUN mkdir -vp /srv/http/api
WORKDIR /srv/http/api
COPY pyproject.toml poetry.lock /srv/http/api/

RUN poetry install --no-root
ADD srcs ./srcs