import paho.mqtt.client as mqtt
import serial
import time
import json
import os
import logging

# Constants for commands
COMMANDS = {
    "SET_VIDEO_INPUT_HDMI": "SPI{input_number}V1",
    "SET_VIDEO_INPUT_CAT5": "SPI{input_number}V2",
    "MUTE_VIDEO_OUTPUT_ENABLED": "SPO{output_number}VME",
    "MUTE_VIDEO_OUTPUT_DISABLED": "SPO{output_number}VMD",
    "SET_AUDIO_OUTPUT_VOLUME": "SPO{output_number}AV{volume_level}",
    "SET_AUDIO_OUTPUT_BALANCE": "SPO{output_number}AB{balance_value}",
    "SET_AUDIO_BASS_FREQUENCY_OUTPUT": "SPO{output_number}AL{bass_value}",
    "SET_AUDIO_MIDDLE_FREQUENCY_OUTPUT": "SPO{output_number}AM{middle_value}",
    "SET_AUDIO_TREBLE_FREQUENCY_OUTPUT": "SPO{output_number}AH{treble_value}",
    "SET_AUDIO_DELAY_OUTPUT": "SPO{output_number}AD{delay_value}",
    "MUTE_AUDIO_OUTPUT_ENABLED": "SPO{output_number}AME",
    "MUTE_AUDIO_OUTPUT_DISABLED": "SPO{output_number}AMD",
    "STEP_VOLUME_UP": "SPO{output_number}VU",
    "STEP_VOLUME_DOWN": "SPO{output_number}VD",
    "POWER_ON": "PON",
    "POWER_OFF": "POF",
    "SET_FACTORY_DEFAULTS": "SFD",
    "SAVE_CURRENT_SETTINGS": "SCS",
    "LOAD_SAVED_SETTINGS": "LSS"
}

# State commands to initialize the state of the matrix
STATE_COMMANDS = [
    "GET_INPUT_STATUS",
    "GET_OUTPUT_STATUS",
    "GET_VOLUME_LEVEL",
    "GET_MUTE_STATUS",
    "GET_GENERAL_STATUS"
]

# Configuration and Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

# Load configuration from environment variables
def load_config():
    config = {
        "MQTT_BROKER": os.getenv("MQTT_BROKER"),
        "MQTT_PORT": int(os.getenv("MQTT_PORT", 1883)),
        "MQTT_USERNAME": os.getenv("MQTT_USERNAME"),
        "MQTT_PASSWORD": os.getenv("MQTT_PASSWORD"),
        "MQTT_USE_SSL": os.getenv("MQTT_USE_SSL") == "true",
        "MQTT_CA_CERT": os.getenv("MQTT_CA_CERT"),
        "MQTT_CLIENT_CERT": os.getenv("MQTT_CLIENT_CERT"),
        "MQTT_CLIENT_KEY": os.getenv("MQTT_CLIENT_KEY"),
        "SERIAL_PORT": os.getenv("SERIAL_PORT"),
        "BAUDRATE": int(os.getenv("BAUDRATE")),
        "MQTT_TOPIC_PREFIX": os.getenv("MQTT_TOPIC_PREFIX"),
        "MQTT_DISCOVERY_PREFIX": os.getenv("MQTT_DISCOVERY_PREFIX")
    }
    
    if not all(config.values()):
        logger.error("One or more required environment variables are missing.")
        exit(1)
    
    return config

config = load_config()

# MQTT Initialization
def init_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    
    if config["MQTT_USERNAME"] and config["MQTT_PASSWORD"]:
        client.username_pw_set(config["MQTT_USERNAME"], config["MQTT_PASSWORD"])
    
    if config["MQTT_USE_SSL"]:
        if config["MQTT_CA_CERT"] or config["MQTT_CLIENT_CERT"] or config["MQTT_CLIENT_KEY"]:
            client.tls_set(ca_certs=config["MQTT_CA_CERT"], certfile=config["MQTT_CLIENT_CERT"], keyfile=config["MQTT_CLIENT_KEY"])
        else:
            client.tls_set()
    
    try:
        client.connect(config["MQTT_BROKER"], config["MQTT_PORT"], 60)
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
        exit(1)
    
    return client

# Serial Initialization
def init_serial_connection():
    try:
        ser = serial.Serial(config["SERIAL_PORT"], config["BAUDRATE"], timeout=1)
        logger.info(f"Listening on {config['SERIAL_PORT']} at {config['BAUDRATE']} baud.")
    except Exception as e:
        logger.error(f"Failed to open serial port: {e}")
        client.loop_stop()
        client.disconnect()
        exit(1)
    
    return ser

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        publish_discovery_config(client)
        publish_available_commands(client)
        initialize_state(ser)
    else:
        logger.error(f"Failed to connect to MQTT broker, return code {rc}")

def publish_discovery_config(client):
    discovery_configs = {
        "input_setup": {
            "topic": f"{config['MQTT_DISCOVERY_PREFIX']}/sensor/matrix_switch_input_setup/config",
            "payload": {
                "name": "Matrix Switch Input Setup",
                "state_topic": f"{config['MQTT_TOPIC_PREFIX']}input/setup",
                "unique_id": "matrix_switch_input_setup",
                "value_template": "{{ value_json.state }}"
            }
        },
        "output_setup": {
            "topic": f"{config['MQTT_DISCOVERY_PREFIX']}/sensor/matrix_switch_output_setup/config",
            "payload": {
                "name": "Matrix Switch Output Setup",
                "state_topic": f"{config['MQTT_TOPIC_PREFIX']}output/setup",
                "unique_id": "matrix_switch_output_setup",
                "value_template": "{{ value_json.state }}"
            }
        },
        "control_setup": {
            "topic": f"{config['MQTT_DISCOVERY_PREFIX']}/sensor/matrix_switch_control_setup/config",
            "payload": {
                "name": "Matrix Switch Control Setup",
                "state_topic": f"{config['MQTT_TOPIC_PREFIX']}control/setup",
                "unique_id": "matrix_switch_control_setup",
                "value_template": "{{ value_json.state }}"
            }
        },
        "status": {
            "topic": f"{config['MQTT_DISCOVERY_PREFIX']}/sensor/matrix_switch_status/config",
            "payload": {
                "name": "Matrix Switch Status",
                "state_topic": f"{config['MQTT_TOPIC_PREFIX']}status",
                "unique_id": "matrix_switch_status",
                "value_template": "{{ value_json.state }}"
            }
        },
        "general": {
            "topic": f"{config['MQTT_DISCOVERY_PREFIX']}/sensor/matrix_switch_general/config",
            "payload": {
                "name": "Matrix Switch General",
                "state_topic": f"{config['MQTT_TOPIC_PREFIX']}general",
                "unique_id": "matrix_switch_general",
                "value_template": "{{ value_json.state }}"
            }
        }
    }
    
    for key, config in discovery_configs.items():
        try:
            client.publish(config["topic"], json.dumps(config["payload"]), retain=True)
            logger.info(f"Published discovery config for {key}")
        except Exception as e:
            logger.error(f"Failed to publish discovery config for {key}: {e}")

def publish_available_commands(client):
    commands_topic = f"{config['MQTT_TOPIC_PREFIX']}available_commands"
    try:
        client.publish(commands_topic, json.dumps(COMMANDS), retain=True)
        logger.info(f"Published available commands to {commands_topic}")
    except Exception as e:
        logger.error(f"Failed to publish available commands: {e}")

def publish_state_change(client, topic_suffix, state):
    topic = f"{config['MQTT_TOPIC_PREFIX']}{topic_suffix}"
    payload = json.dumps({"state": state.strip()})
    try:
        client.publish(topic, payload)
        logger.info(f"Published state change: {topic} -> {payload}")
    except Exception as e:
        logger.error(f"Failed to publish state change: {e}")

def initialize_state(ser):
    for command in STATE_COMMANDS:
        try:
            ser.write(f"{command}\r".encode())
            time.sleep(0.5)  # Allow some time for the command to be processed
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').strip()
                publish_state_change(client, f"state/{command.lower()}", response)
                logger.info(f"Initialized state for {command}: {response}")
        except Exception as e:
            logger.error(f"Failed to initialize state for {command}: {e}")

def check_serial_connection(ser):
    try:
        ser.write(b'\r')  # Send a simple command to check the connection
        ser.read(1)       # Read the response to verify connection
        return True
    except serial.SerialException as e:
        logger.error(f"Serial connection lost: {e}")
        return False

def reconnect_serial():
    global ser
    while True:
        ser = init_serial_connection()
        if ser:
            logger.info("Serial connection reestablished")
            initialize_state(ser)
            break
        time.sleep(5)

if __name__ == "__main__":
    client = init_mqtt_client()
    ser = init_serial_connection()

    client.loop_start()

    try:
        while True:
            try:
                if not check_serial_connection(ser):
                    reconnect_serial()

                if ser.in_waiting > 0:
                    state = ser.readline().decode('utf-8')
                    if state:
                        # Example topic structure based on the command or state content
                        if "SPI" in state:
                            publish_state_change(client, "input/setup", state)
                        elif "SPO" in state:
                            publish_state_change(client, "output/setup", state)
                        elif "SPC" in state:
                            publish_state_change(client, "control/setup", state)
                        elif "ST" in state:
                            publish_state_change(client, "status", state)
                        else:
                            publish_state_change(client, "general", state)
            except Exception as e:
                logger.error(f"Failed to read from serial port: {e}")
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt, shutting down")
    finally:
        ser.close()
        client.loop_stop()
        client.disconnect()
        logger.info("Disconnected from MQTT broker and closed serial port")

