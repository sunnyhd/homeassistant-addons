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

# Activate the virtual environment
source /srv/venv/bin/activate

# Debugging information
echo "MQTT_BROKER=${MQTT_BROKER}"
echo "MQTT_PORT=${MQTT_PORT}"
echo "MQTT_USERNAME=${MQTT_USERNAME}"
echo "MQTT_PASSWORD=${MQTT_PASSWORD}"
echo "MQTT_USE_SSL=${MQTT_USE_SSL}"
echo "MQTT_CA_CERT=${MQTT_CA_CERT}"
echo "MQTT_CLIENT_CERT=${MQTT_CLIENT_CERT}"
echo "MQTT_CLIENT_KEY=${MQTT_CLIENT_KEY}"
echo "SERIAL_PORT=${SERIAL_PORT}"
echo "BAUDRATE=${BAUDRATE}"
echo "MQTT_TOPIC_PREFIX=${MQTT_TOPIC_PREFIX}"
echo "MQTT_DISCOVERY_PREFIX=${MQTT_DISCOVERY_PREFIX}"
echo "LOG_LEVEL=${LOG_LEVEL}"

# Start the Python script and log output
python /app/mqtt_state_monitor.py > /config/matrix_switch_mqtt.log 2>&1
