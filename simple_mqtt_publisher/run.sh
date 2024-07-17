#!/bin/bash

# Load configuration from options
MQTT_BROKER=${MQTT_BROKER:-"core-mosquitto"}
MQTT_PORT=${MQTT_PORT:-1883}
MQTT_USERNAME=${MQTT_USERNAME:-""}
MQTT_PASSWORD=${MQTT_PASSWORD:-""}
MQTT_TOPIC=${MQTT_TOPIC:-"homeassistant/test"}
MESSAGE=${MESSAGE:-"Hello from Home Assistant add-on"}

# Export the variables for use in the Python script
export MQTT_BROKER
export MQTT_PORT
export MQTT_USERNAME
export MQTT_PASSWORD
export MQTT_TOPIC
export MESSAGE

# Start the Python script
python /app/mqtt_publisher.py
