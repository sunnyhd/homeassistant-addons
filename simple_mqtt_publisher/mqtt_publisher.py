import os
import time
import paho.mqtt.client as mqtt

# Load environment variables and set default values if not provided
MQTT_BROKER = os.getenv('MQTT_BROKER', 'core-mosquitto')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))  # Ensure default is a string
MQTT_USERNAME = os.getenv('MQTT_USERNAME', '')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', '')
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'homeassistant/test')
MESSAGE = os.getenv('MESSAGE', 'Hello from Home Assistant add-on')

# Connect to the MQTT broker
def connect_mqtt():
    client = mqtt.Client()
    if MQTT_USERNAME and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client

def main():
    client = connect_mqtt()
    
    while True:
        client.publish(MQTT_TOPIC, MESSAGE)
        print(f"Published '{MESSAGE}' to topic '{MQTT_TOPIC}'")
        time.sleep(10)

if __name__ == "__main__":
    main()
