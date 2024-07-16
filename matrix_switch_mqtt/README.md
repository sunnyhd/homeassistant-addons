# Matrix Switch MQTT Add-on

This add-on publishes matrix switch state changes to MQTT for Home Assistant.

## Installation

1. Add this repository to your Home Assistant add-on store.
2. Install the "Matrix Switch MQTT" add-on from the add-on store.
3. Configure the add-on options as required.
4. Start the add-on.

## Configuration

Example configuration options:

```yaml
mqtt_broker: "mqtt_broker_address"
mqtt_port: 8883
mqtt_username: "your_username"
mqtt_password: "your_password"
mqtt_use_ssl: true
mqtt_ca_cert: "/path/to/ca.crt"
mqtt_client_cert: "/path/to/client.crt"
mqtt_client_key: "/path/to/client.key"
serial_port: "/dev/ttyUSB0"
baudrate: 57600
mqtt_topic_prefix: "homeassistant/matrix_switch/"
mqtt_discovery_prefix: "homeassistant"
log_level: "info"
