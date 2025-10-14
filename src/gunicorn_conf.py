"""Gunicorn configuration for production FastAPI deployment."""

import multiprocessing
from typing import Any

from logger import setup_logging

# Configure logging before Gunicorn starts
setup_logging()

import logging

logger = logging.getLogger(__name__)

# Worker processes
workers: int = multiprocessing.cpu_count() * 2 + 1

# Worker class for async FastAPI
worker_class: str = "uvicorn.workers.UvicornWorker"

# Server socket
bind: str = "0.0.0.0:8000"

# Timeout settings
timeout: int = 120
graceful_timeout: int = 30  # Time to finish requests during restart
keepalive: int = 5

# Logging
accesslog: str = "-"
errorlog: str = "-"
loglevel: str = "info"

# Worker lifecycle management
max_requests: int = 1000
max_requests_jitter: int = 50

# Performance optimization
preload_app: bool = True  # Load app before forking (saves memory)


# Lifecycle hooks
def on_starting(_server: Any) -> None:
    """Called just before the master process is initialized."""
    logger.info("🚀 Gunicorn master process starting...")


def when_ready(_server: Any) -> None:
    """Called just after the server is started."""
    logger.info(f"✅ Gunicorn ready with {workers} workers on {bind}")


def on_reload(_server: Any) -> None:
    """Called to recycle workers during a reload via SIGHUP."""
    logger.info("🔄 Gunicorn reloading workers...")


def worker_int(worker: Any) -> None:
    """Called when a worker receives the SIGINT or SIGQUIT signal."""
    logger.info(f"⚠️  Worker {worker.pid} received interrupt signal")


def on_exit(_server: Any) -> None:
    """Called just before the master process exits."""
    logger.info("🔴 Gunicorn shutting down gracefully...")
