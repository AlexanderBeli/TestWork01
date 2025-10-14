# It is a little bit overhead for this project but I did it just for showing some skills
"""Celery Application Configuration."""

from src.config import settings

# broker and backend settings
broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_RESULT_BACKEND

# serialization settings
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

# timezone and utc settings
timezone = "UTC"
enable_utc = True

# result backend settings
result_expires = 3600
result_backend_transport_options = {"max_connections": 400}

# worker perfomance settings
worker_prefetch_multiplier = 1
task_acks_late = True
worker_max_tasks_per_child = 1000

# task retry settings
task_default_retry_delay = 60
task_max_retries = 3

# logging settings
worker_hijack_root_logger = False
worker_log_color = False
worker_log_format = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"

# monitoring and health check settings
worker_send_task_events = True
task_send_sent_event = True
task_track_started = True
task_reject_on_worker_lost = True

# queue configuration
task_default_queue = "default"
task_create_missing_queues = True

task_routes = {
    "proj.celery.start_parsing_task": {"queue": "default"},
}

# environment specific settings
if settings.ENVIRONMENT == "development":
    task_always_eager = False
    task_eager_propagates = True

elif settings.ENVIRONMENT == "production":
    worker_pool_restarts = True
    worker_max_memory_per_child = 200000
