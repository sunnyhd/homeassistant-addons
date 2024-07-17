ARG BUILD_FROM=ghcr.io/hassio-addons/base:15.0.9
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Copy Python requirements file
COPY requirements.txt /tmp/

# Setup base
RUN \
    apk add --no-cache --virtual .build-dependencies \
        build-base \
        git \
        libffi-dev \
        py3-wheel \
        python3-dev \
    && apk add --no-cache \
        py3-bcrypt \
        py3-cryptography \
        py3-pip \
        python3 \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && find /usr \
        \( -type d -a -name test -o -name tests -o -name '__pycache__' \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && apk del --no-cache --purge .build-dependencies

# Copy application files
WORKDIR /app
COPY . /app

# Set permissions for run.sh
RUN chmod +x /app/run.sh

# Set the entrypoint
ENTRYPOINT ["/app/run.sh"]
