ARG BUILD_FROM
FROM $BUILD_FROM

# Set environment variables
ENV LANG C.UTF-8

# Install required packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    linux-headers

# Install Python packages
RUN pip3 install --no-cache-dir paho-mqtt pyserial

# Copy data
COPY run.sh /
COPY mqtt_state_monitor.py /usr/src/app/

# Set permissions
RUN chmod a+x /run.sh

# Set the entrypoint
CMD [ "/run.sh" ]

