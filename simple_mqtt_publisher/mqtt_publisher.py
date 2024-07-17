import os
import time
import paho.mqtt.client as mqtt

# Load environment variables and set default values if not provided
MQTT_BROKER = os.getenv('MQTT_BROKER', 'mqtt_broker_address')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'homeassistant/test')
MESSAGE = os.getenv('MESSAGE', 'Hello from Home Assistant add-on')

# Connect to the MQTT broker
def connect_mqtt():
    client = mqtt.Client()
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