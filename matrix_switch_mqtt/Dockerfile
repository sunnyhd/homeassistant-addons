ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install packages
RUN apk add --no-cache \
    python3 \
    py3-pip

# Install Python packages
RUN pip3 install paho-mqtt pyserial

# Copy data
COPY run.sh /
COPY mqtt_state_monitor.py /usr/src/app/

# Set permissions
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
