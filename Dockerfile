FROM python:3.13.7-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/app:/app/src:${PYTHONPATH}"

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev \
    gcc \
    gettext \
    make \
    wget

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src /app

RUN ln -s /app /app/src

CMD ["gunicorn", "-c", "gunicorn_conf.py", "main:app"]