ARG BUILD_FROM
FROM $BUILD_FROM

# Set environment variables
ENV LANG C.UTF-8
ENV PATH="/srv/venv/bin:$PATH"

# Install required packages
WORKDIR /srv
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-yaml \
    build-base \
    linux-headers \
    libffi-dev \
    openssl-dev \
    gcc \
    musl-dev \
    python3-dev

# Prepare virtual environment
RUN python3 -m venv /srv/venv

# Install required Python packages
RUN /srv/venv/bin/pip install --no-cache-dir paho-mqtt pyserial

# Copy data for add-on
WORKDIR /
COPY run.sh /
COPY mqtt_state_monitor.py /srv/

# Set permissions
RUN chmod a+x /run.sh

# Set the entrypoint
ENTRYPOINT [ "/run.sh" ]
