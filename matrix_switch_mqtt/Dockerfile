FROM homeassistant/amd64-base:latest

# Set environment variables
ENV LANG C.UTF-8
ENV S6_OVERLAY_VERSION v2.2.0.3
ENV PATH="/srv/venv/bin:$PATH"

# Install s6-overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-amd64.tar.gz /tmp/
RUN tar -xzf /tmp/s6-overlay-amd64.tar.gz -C /

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

# s6 overlay service directory
COPY ./services.d /etc/services.d

ENTRYPOINT [ "/init" ]
