import paho.mqtt.client as mqttClient
import time


def on_connect(client, userdata, flags, rc):
     if rc == 0:
        print("Connected to broker")
        global Connected #Use global variabl
        Connected = True
     else:
        print("Connection failed")

Connected = False #global variable for the state of the connection

broker_address= "192.168.18.173"
port = 1883
user = "mbkm"
password = "mbkm"

client = mqttClient.Client("Publish : Gamzv (Python)") #create new instance
client.username_pw_set(user, password=password) #set usernameand password
client.on_connect = on_connect #attach function to callback
client.connect(broker_address, port=port) #connect to broker
client.loop_start()

while Connected != True: #Wait for connection
    time.sleep(0.1)

try:
    i = 1
    while True:
        val = f"{i.__str__()}:{(i*2).__str__()}"
        client.publish("device/room/kitchen/", val)
        i += 1
        time.sleep(1)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()