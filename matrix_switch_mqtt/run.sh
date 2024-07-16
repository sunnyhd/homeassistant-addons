#!/usr/bin/with-contenv bashio

# Load configuration from options
export MQTT_BROKER=$(bashio::config 'mqtt_broker')
export MQTT_PORT=$(bashio::config 'mqtt_port')
export MQTT_USERNAME=$(bashio::config 'mqtt_username')
export MQTT_PASSWORD=$(bashio::config 'mqtt_password')
export MQTT_USE_SSL=$(bashio::config 'mqtt_use_ssl')
export MQTT_CA_CERT=$(bashio::config 'mqtt_ca_cert')
export MQTT_CLIENT_CERT=$(bashio::config 'mqtt_client_cert')
export MQTT_CLIENT_KEY=$(bashio::config 'mqtt_client_key')
export SERIAL_PORT=$(bashio::config 'serial_port')
export BAUDRATE=$(bashio::config 'baudrate')
export MQTT_TOPIC_PREFIX=$(bashio::config 'mqtt_topic_prefix')
export MQTT_DISCOVERY_PREFIX=$(bashio::config 'mqtt_discovery_prefix')
export LOG_LEVEL=$(bashio::config 'log_level')

# Start the Python script
python3 /usr/src/app/mqtt_state_monitor.py
