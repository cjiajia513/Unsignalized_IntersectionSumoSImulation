import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker")
    else:
        print(f"Failed to connect, return code {rc}")

# The callback for when the client disconnects from the server.
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection. Return code {rc}")
    else:
        print("Disconnected successfully")

# Create an MQTT client instance
client = mqtt.Client()

# Assign event callbacks
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Set the address and port of the MQTT broker you want to connect to
broker_address = "test.mosquitto.org"  # Use a public broker for testing
broker_port = 1883  # Default unencrypted MQTT port

try:
    # Attempt to connect to the MQTT broker
    print(f"Connecting to MQTT broker at {broker_address}:{broker_port}...")
    client.connect(broker_address, broker_port, 60)

    # Start the network loop
    client.loop_start()

    # Wait for a while to allow connection to be established
    # and for any callbacks to be processed
    input("Press Enter to exit...\n")

finally:
    # Stop the network loop and disconnect cleanly
    client.loop_stop()
    client.disconnect()
    
    
    
    
    