FROM docker.io/library/debian:11-slim

RUN apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
    && mkdir -p /usr/share/keyrings \
    && curl \
        --fail \
        --silent \
        --show-error \
        https://packages.cloud.google.com/apt/doc/apt-key.gpg \
        | gpg --dearmor \
        > /usr/share/keyrings/coral-edgetpu.gpg \
    && echo \
        "deb [signed-by=/usr/share/keyrings/coral-edgetpu.gpg] https://packages.cloud.google.com/apt coral-edgetpu-stable main" \
        > /etc/apt/sources.list.d/coral-edgetpu.list \
    && apt-get update \
    && apt-get install -y \
        --no-install-recommends \
        edgetpu-compiler \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["edgetpu_compiler"]

CMD ["--help"]
