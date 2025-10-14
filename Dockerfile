# Stage 1: Builder
FROM python:3.13.7-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONPATH="/app:/app/src:${PYTHONPATH}"

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.13.7-slim
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/app:/app/src:${PYTHONPATH}"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libpq5 \
    gettext \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# This is the key optimisation
COPY --from=builder /root/.local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /root/.local/bin /usr/local/bin

COPY ./src /app

RUN ln -s /app /app/src

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/healthcheck || exit 1 

CMD ["gunicorn", "-c", "gunicorn_conf.py", "main:app"]