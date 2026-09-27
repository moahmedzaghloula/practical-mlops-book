FROM docker.io/library/python:3.13-slim

ARG APP_VERSION=0.1.0

LABEL org.opencontainers.image.title="Chapter 3 Hardened Image" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.description="Non-root Python container"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --gid 10001 appuser \
    && useradd \
        --uid 10001 \
        --gid 10001 \
        --create-home \
        --shell /usr/sbin/nologin \
        appuser

USER 10001:10001

ENTRYPOINT ["python"]

CMD ["--version"]
