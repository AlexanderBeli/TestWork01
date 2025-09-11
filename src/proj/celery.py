"""Celery Entrypoint."""

from celery import Celery

app = Celery(
    "parse_quotes",
)
app.config_from_object("proj.celeryconfig")

app.autodiscover_tasks(["src.proj"])
