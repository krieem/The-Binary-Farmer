import paho.mqtt.client as mqtt
import keys
import requests

hostname="localhost"
port=1883
mqttUser="ifn649"
mqttPass="ifn649"
topics = ["Humidity", "Temperature", "Soil", "Heat", "WaterLevel" ]

print('Starting up bot...')


def send_msg(msg):
	token = "5697769562:AAEL6MyZ4V6wy006yV3D-6o48nKscKIXmX4"
	chat_id = "717510350"
	url_req = "https://api.telegram.org/bot"+ token +"/sendMessage" + "?chat_id=" + chat_id + "&text=" + msg
	results = requests.get(url_req)


def on_connect(client, userdata, flags, rc): # func for making connection print("Connected to MQTT")
	print("Connected to MQTT")
	print("Connection returned result: " + str(rc) )
	print()
	client.subscribe("WaterLevel")
	print("subscribed to : " +  "WaterLevel")    

def on_message(client, userdata, msg):
	print("Receving Data From AWS")
	print()
	print(msg.topic+" "+str(msg.payload))
	note = int(msg.payload[-2:-1])
	print(note)
	if note < 3:
		send_msg("Water level is critical please refill the tank")


client = mqtt.Client() 
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqttUser, mqttPass)
client.connect(hostname , port, 60)
client.loop_forever()
