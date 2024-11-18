import paho.mqtt.client as mqtt
import ssl

# Define callback for successful connection
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with code:", rc)
    if rc == 0:
        # Subscribe to the topic after connecting
        client.subscribe("ATN/led", qos=1)
    else:
        print("Failed to connect, return code:", rc)

# Define callback for receiving messages
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

# Create MQTT client
client = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)

# Set up callbacks
client.on_connect = on_connect
client.on_message = on_message


client.username_pw_set("ATN_IOT_SYSTEM", "Wasd1234")


# Enable TLS if needed (comment out if not using secure connection)
# client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.tls_set(tls_version=ssl.PROTOCOL_TLS)

# Connect to the broker
client.connect("298321207d58431bb997da06e6cd2ca4.s1.eu.hivemq.cloud", 8883)

# Start the loop to process network traffic and callbacks
client.loop_forever()
