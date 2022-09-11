import paho.mqtt.client as mqtt
from time import sleep
import serial
import paho.mqtt.client as mqtt
import os
import threading

hostname="3.11.79.48"
port=1883
mqttUser="ifn649"
mqttPass="ifn649"
topics = ["Humidity", "Temperature", "Soil", "Heat" ]
actor = serial.Serial("/dev/rfcomm0", 9600)

def init():
    blue0 = os.path.exists("/dev/rfcomm0")
    if blue0 == False:
        os.system("sudo rfcomm bind rfcomm0 {}", com0)
        print("Teensy 1 Initialized")
        print()
    actor

def on_connect(client, userdata, flags, rc): # func for making connection print("Connected to MQTT")
    print("Connected to MQTT")
    print("Connection returned result: " + str(rc) )
    print()
    for topic in topics:
        client.subscribe(topic)
        print("subscribed to : " + topic)
    print()
    

def on_message(client, userdata, msg):
    print("Receving Data From AWS")
    led('1')
    print()
    print(msg.topic+" "+str(msg.payload))
    led('0')

def led(soil):
    try:
        if (soil == '1'):
            actor.write("0".encode())
            sleep(2)
        elif (soil == '0'):
            actor.write("1".encode())
    except:
        print("Connection Error")
        print("Retring in 1 second")
        print()
        
init()

client = mqtt.Client() 
client.on_connect = on_connect

client.on_message = on_message
client.username_pw_set(mqttUser, mqttPass)
client.connect(hostname , port, 60)
client.loop_forever()