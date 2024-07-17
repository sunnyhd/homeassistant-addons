import os
import time
import paho.mqtt.client as mqtt

# Load environment variables and set default values if not provided
MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
MQTT_USERNAME = os.getenv('MQTT_USERNAME', '')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', '')
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'homeassistant/test')
MESSAGE = os.getenv('MESSAGE', 'Hello from Home Assistant add-on')

# Callback function when a message is received
def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

# Connect to the MQTT broker
def connect_mqtt():
    client = mqtt.Client()
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client

def main():
    client = connect_mqtt()
    client.on_message = on_message
    client.loop_start()
    client.subscribe(MQTT_TOPIC)

    while True:
        client.publish(MQTT_TOPIC, MESSAGE)
        print(f"Published '{MESSAGE}' to topic '{MQTT_TOPIC}'")
        time.sleep(10)

if __name__ == "__main__":
    main()
