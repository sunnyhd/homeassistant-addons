ARG BUILD_FROM
FROM $BUILD_FROM

# Set environment variables
ENV LANG C.UTF-8
ENV S6_OVERLAY_VERSION=v2.2.0.3.0
ENV PATH="/srv/venv/bin:$PATH"

# Install s6-overlay
ADD https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-amd64.tar.gz /tmp/
RUN tar -xzf /tmp/s6-overlay-amd64.tar.gz -C /

# Install required packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
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

# Copy application files
WORKDIR /app
COPY . /app

# Copy run.sh and make it executable
COPY run.sh /app/
RUN chmod +x /app/run.sh

# s6 overlay service directory
COPY ./services.d /etc/services.d

# Expose necessary ports (adjust based on your application needs)
EXPOSE 1627
EXPOSE 8099

# Set the entrypoint to s6-svscan
ENTRYPOINT [ "/init" ]

