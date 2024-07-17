ARG BUILD_FROM=ghcr.io/hassio-addons/base:15.0.9
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install necessary dependencies
RUN apk add --no-cache python3 py3-pip build-base git libffi-dev python3-dev

# Copy Python requirements file
COPY requirements.txt /tmp/

# Install Python packages
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Copy application files
WORKDIR /app
COPY . /app

# Set permissions for run.sh
RUN chmod +x /app/run.sh

# Set the entrypoint
ENTRYPOINT ["/app/run.sh"]


