# Hello MQTT Add-on

This is a Hello World add-on for Home Assistant with MQTT functionality. It publishes a message to a specified MQTT topic periodically and logs any received messages.

## Configuration

Add-on configuration options:

- `mqtt_broker`: The address of the MQTT broker.
- `mqtt_port`: The port of the MQTT broker.
- `mqtt_username`: The username for the MQTT broker (if required).
- `mqtt_password`: The password for the MQTT broker (if required).
- `mqtt_topic`: The MQTT topic to publish to and subscribe to.
- `message`: The message to publish to the MQTT topic.

## Usage

1. Add the add-on repository to Home Assistant.
2. Install the Hello MQTT Add-on.
3. Configure the add-on options as required.
4. Start the add-on.
