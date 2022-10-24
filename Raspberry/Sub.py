import paho.mqtt.client as mqtt
from time import sleep
import serial
import os

hostname="3.11.79.48"
port=1883
mqttUser="ifn649"
mqttPass="ifn649"
topics = ["Humidity", "Temperature", "Soil", "Heat" ]
actor = serial.Serial("/dev/rfcomm4", 9600)


blue0 = os.path.exists("/dev/rfcomm3")
if blue0 == False:
    os.system("sudo rfcomm bind rfcomm4 00:20:10:08:2B:51")
    print("Motor arduino Initialized")
    print()
actor

def on_connect(client, userdata, flags, rc): # func for making connection print("Connected to MQTT")
    print("Connected to MQTT")
    print("Connection returned result: " + str(rc) )
    print()
    client.subscribe("Soil")
    print("subscribed to : " + "Soil")
    print()
    

def on_message(client, userdata, msg):
    print("Receving Data From AWS")
    print()
    print(msg.topic+" "+str(msg.payload))
    Soil = str(msg.payload)
    motor(Soil[-3:-1])
    print(Soil[-4:-1])


def motor(Soil):
    sleep(2)
    if (Soil < '600'):
        actor.write("0".encode())
        sleep(2)
    elif (Soil > '600'):
        actor.write("1".encode())
        sleep(20)
        actor.write("0".encode())

client = mqtt.Client() 
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqttUser, mqttPass)
client.connect(hostname , port, 60)
client.loop_forever()