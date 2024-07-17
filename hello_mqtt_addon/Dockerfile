ARG BUILD_FROM
FROM $BUILD_FROM

# Install necessary dependencies
RUN apk add --no-cache python3 py3-pip

# Install required Python packages
RUN pip3 install paho-mqtt

# Copy application files
WORKDIR /app
COPY . /app

# Set permissions for run.sh
RUN chmod +x /app/run.sh

# Set the entrypoint
ENTRYPOINT ["/app/run.sh"]
