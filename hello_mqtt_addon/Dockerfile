FROM python:3.9-alpine

# Install necessary dependencies
RUN apk add --no-cache bash

# Install required Python packages
RUN pip install paho-mqtt pyserial

# Copy application files
WORKDIR /app
COPY . /app

# Set permissions for run.sh
RUN chmod +x /app/run.sh

# Set the entrypoint
ENTRYPOINT ["/app/run.sh"]
