import paho.mqtt.client as mqtt
import threading
from cpm_log import Cpmlog
class MessageCom:
    def __init__(self, broker, port, topic):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker = broker
        self.port = port
        self.topic = topic
        self.messages = []
        self.logger = Cpmlog().get_logger()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.logger.info("Connected with result code "+str(rc))
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.payload.decode()}")
        self.logger.info(msg.topic+" "+str(msg.payload))
        self.messages.append(msg.payload.decode())

    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        self.thread = threading.Thread(target=self.client.loop_forever)
        self.thread.start()

    def send_message(self, message):
        self.client.publish(self.topic, message)
        self.logger.info("send the bsm message:{msg}".format(msg=message))

    def disconnect(self):
        self.client.disconnect()