import logging
import os
import paho.mqtt.client as mqtt
import serial
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# MQTT Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER')
MQTT_PORT = int(os.getenv('MQTT_PORT'))
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
MQTT_TOPIC_PREFIX = os.getenv('MQTT_TOPIC_PREFIX')

# Serial Configuration
SERIAL_PORT = os.getenv('SERIAL_PORT')
BAUDRATE = int(os.getenv('BAUDRATE'))

# Connect to the serial port
def connect_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
        logger.info(f"Connected to serial port: {SERIAL_PORT} at {BAUDRATE} baud")
        return ser
    except serial.SerialException as e:
        logger.error(f"Failed to connect to serial port: {e}")
        return None

# Connect to the MQTT broker
def connect_mqtt():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client

# Send command to the matrix switch
def send_command(ser, command):
    try:
        ser.write(command.encode() + b'\r')
        response = ser.read_until(b'\r')
        return response.decode().strip()
    except serial.SerialException as e:
        logger.error(f"Failed to send command: {e}")
        return None

# Publish state to MQTT
def publish_state(client, topic, state):
    client.publish(MQTT_TOPIC_PREFIX + topic, state)
    logger.info(f"Published to {MQTT_TOPIC_PREFIX + topic}: {state}")

def main():
    ser = connect_serial()
    if not ser:
        return

    client = connect_mqtt()

    while True:
        # Example command: Get the status of the matrix switch
        command = 'GET_STATUS'
        response = send_command(ser, command)
        
        if response:
            publish_state(client, 'status', response)
        
        time.sleep(10)  # Wait for 10 seconds before the next poll

if __name__ == "__main__":
    main()
