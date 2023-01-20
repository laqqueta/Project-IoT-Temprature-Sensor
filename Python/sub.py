import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to broker")

def on_message(client, userdata, message):
    print ("Message received: " + message.payload.decode('utf8'))

broker_address= "192.168.18.173"
port = 1883
user = "mbkm"
password = "mbkm"

client = mqtt.Client()
client.username_pw_set(user,password=password)
client.connect(broker_address, port)
client.on_connect = on_connect #attach function to callback
client.on_message = on_message #attach function to callback

client.subscribe("device/room/kitchen/")
client.loop_forever()