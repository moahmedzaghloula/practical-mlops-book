FROM registry.fedoraproject.org/fedora:42

ARG APP_VERSION=1.0.0

LABEL org.opencontainers.image.title="Chapter 3 Container Basics" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.description="Fedora container fundamentals lab"

RUN dnf install -y \
        --setopt=install_weak_deps=False \
        python3 \
    && dnf clean all \
    && rm -rf /var/cache/dnf

ENTRYPOINT ["/usr/bin/python3"]

CMD ["--version"]
