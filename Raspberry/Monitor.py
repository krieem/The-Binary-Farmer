from time import sleep
import paho.mqtt.publish as publish
import serial
import os

hostname="3.11.79.48"
port="1883"
mqttUser="ifn649"
mqttPass="ifn649"
com1 = "98:D3:B1:FD:C0:5B"
com2 = "98:D3:91:FD:D9:E5"

def init():
    blue1 = os.path.exists("/dev/rfcomm1")
    blue2 = os.path.exists("/dev/rfcomm2")
    if blue1 == False:
        os.system("sudo rfcomm bind rfcomm1 {}", com1)
        print("Teensy 2 Initialized")
        print()
    if blue2 == False:
        os.system("sudo rfcomm bind rfcomm2 {}", com2)
        print("Teensy 3 Initialized")
        print()

def collectData():
    print()
    data = []
    for n in range(3):
        if n == 0:
            n = 1
        nstr = str(n)
        sensor = serial.Serial("/dev/rfcomm" + nstr, 9600)
        sleep(2)
        while True:
            try:
                if sensor.in_waiting > 0:
                    rawserial = sensor.readline()
                    cookedserial = rawserial.decode('utf-8').strip('\r\n')
                    strserial = str(cookedserial)
                    data.append(strserial)
                    break
                else:
                    print("Witting for connection")
                    print("Retring in 1 second")
                    print()
                    sleep(1)
            except:
                print("An exception occurred")
                sleep(1)
                print()

    soil = data[0]
    temp = data[2]
    soil = soil[7:10]
    data = []
    return temp, soil
    
def  demo():
    for i in range(5):
        print()
        print(f"This demo will be repeated {i + 1} time out of 5")
        sensors = collectData()

        print( "Temp : " + sensors[0])
        print( "Soil : " + sensors[1])

        DHT = sensors[0]
        humi = DHT[9:16]
        temp = (DHT[30:36]+ "C")
        heat = (DHT[59:65]+ "C")
        soil = sensors[1]

        mqtt_auth = { 'username': mqttUser, 'password': mqttPass } 
        publish.single("Humidity", humi , hostname = hostname, auth = mqtt_auth)
        publish.single("Temperature", temp , hostname = hostname, auth = mqtt_auth)
        publish.single("Heat", heat , hostname = hostname, auth = mqtt_auth)
        publish.single("Soil", soil , hostname = hostname, auth = mqtt_auth)

        #i+=1


while True:
    print()
    print("Connections initializing")
    init()
    print("Full Demo for assessment One")
    print("Initializing connctions completed")
    print()
    print("1) Start the Demo")
    print("2) Exit")
    menuInput = input("Enter item number > ")
    print()
    if (menuInput == "1"):
        demo()
    elif (menuInput== "2"):
        print("Exiting")
        break
    else:
        print("Worng item")
