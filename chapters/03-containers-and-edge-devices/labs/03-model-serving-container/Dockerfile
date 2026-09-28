FROM docker.io/library/python:3.13-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

COPY requirements.lock.txt .

RUN python -m pip wheel \
    --no-cache-dir \
    --wheel-dir /wheels \
    --requirement requirements.lock.txt


FROM docker.io/library/python:3.13-slim AS runtime

ARG MODEL_VERSION=1.0.0

LABEL org.opencontainers.image.title="Chapter 3 Model API" \
      org.opencontainers.image.version="${MODEL_VERSION}" \
      org.opencontainers.image.description="Containerized regression inference API"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/model/model.joblib

RUN groupadd --gid 10001 appuser \
    && useradd \
        --uid 10001 \
        --gid 10001 \
        --create-home \
        --shell /usr/sbin/nologin \
        appuser

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY requirements.lock.txt .

RUN python -m pip install \
        --no-cache-dir \
        --no-index \
        --find-links=/wheels \
        --requirement requirements.lock.txt \
    && rm -rf /wheels

COPY train.py app.py ./

RUN mkdir -p /app/model \
    && MODEL_VERSION="${MODEL_VERSION}" python train.py \
    && chown -R 10001:10001 /app

USER 10001:10001

EXPOSE 8000

HEALTHCHECK \
    --interval=30s \
    --timeout=3s \
    --start-period=10s \
    --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "--timeout", "60", "app:app"]
