ARG BUILD_FROM=hassioaddons/base:8.0.6
FROM $BUILD_FROM

# Set environment variables
ENV LANG C.UTF-8

# Install required packages
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    build-base \
    linux-headers \
    libffi-dev \
    openssl-dev \
    gcc \
    musl-dev \
    python3-dev

# Log Python and pip versions
RUN python3 --version && pip3 --version

# Install Python packages with detailed logging
RUN pip3 install --no-cache-dir paho-mqtt pyserial --verbose

# Copy data
COPY run.sh /
COPY mqtt_state_monitor.py /usr/src/app/

# Set permissions
RUN chmod a+x /run.sh

# Set the entrypoint
CMD [ "/run.sh" ]

