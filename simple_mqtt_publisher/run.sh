#!/bin/bash

# Load configuration from options
MQTT_BROKER=${MQTT_BROKER:-"mqtt_broker_address"}
MQTT_PORT=${MQTT_PORT:-1883}
MQTT_TOPIC=${MQTT_TOPIC:-"homeassistant/test"}
MESSAGE=${MESSAGE:-"Hello from Home Assistant add-on"}

# Start the Python script and log output
python /app/mqtt_publisher.py

