from copyreg import constructor
from time import sleep
import paho.mqtt.publish as publish
import serial
import os
import concurrent.futures
from rpi_lcd import LCD

hostname="3.11.79.48"
port="1883"
mqttUser="ifn649"
mqttPass="ifn649"

def init():
    blue1 = os.path.exists("/dev/rfcomm1")
    blue2 = os.path.exists("/dev/rfcomm2")
    blue3 = os.path.exists("/dev/rfcomm3")
    if blue1 == False:
        os.system("sudo rfcomm bind rfcomm1 98:D3:B1:FD:C0:5B")
        print("Teensy Soil Initialized")
        print()
    if blue2 == False:
        os.system("sudo rfcomm bind rfcomm2 98:D3:91:FD:D9:E5")
        print("Teensy Temp Initialized")
        print()
    if blue3 == False:
        os.system("sudo rfcomm bind rfcomm2 98:D3:C1:FD:BD:C3")
        print("Teensy Water level Initialized")
        print()

def soil():
    sleep(2)
    try:
        while True:
            soil = serial.Serial("/dev/rfcomm3", 9600)
            rawserial = soil.readline()
            cookedserial = rawserial.decode('utf-8').strip('\r\n')
            strserial = str(cookedserial)
            return strserial
    except:
        soil()

def wlevel():
    sleep(2)
    try:
        while True:
            soil = serial.Serial("/dev/rfcomm2", 9600)
            rawserial = soil.readline()
            cookedserial = rawserial.decode('utf-8').strip('\r\n')
            strserial = str(cookedserial)
            return strserial
    except:
        soil()

def temp():
    sleep(2)
    try:
        while True:
            soil = serial.Serial("/dev/rfcomm1", 9600)
            rawserial = soil.readline()
            cookedserial = rawserial.decode('utf-8').strip('\r\n')
            strserial = str(cookedserial)
            humi = (strserial[10:15])
            temp = (strserial[31:36])
            heat = (strserial[60:65])
            return humi, temp, heat
    except:
        temp()

def lcdInfo(soil, temp, humi, heat, water):
    lcd = LCD()
    lcd.clear()
    lcd.text("Soil Moisture",1)
    lcd.text(soil,2)
    sleep(5)
    lcd.clear()
    lcd.text("Temperature",1)
    lcd.text(temp + "C",2)
    sleep(5)
    lcd.clear()
    lcd.text("Humidity",1)
    lcd.text(humi + "%",2)
    sleep(5)
    lcd.clear()
    lcd.text("Heat index",1)
    lcd.text(heat + "C",2)
    sleep(5)
    lcd.clear()
    lcd.text("Water level",1)
    lcd.text(water ,2)
    sleep(5)
    lcd.clear()

def mqTT(Soil, Temperature, Humidity, Heat , water):
    mqtt_auth = { 'username': mqttUser, 'password': mqttPass } 
    publish.single("Humidity", Humidity , hostname = hostname, auth = mqtt_auth)
    publish.single("Temperature", Temperature , hostname = hostname, auth = mqtt_auth)
    publish.single("Heat", Heat , hostname = hostname, auth = mqtt_auth)
    publish.single("Soil", Soil , hostname = hostname, auth = mqtt_auth)
    publish.single("WaterLevel", water , hostname = hostname, auth = mqtt_auth)

with concurrent.futures.ThreadPoolExecutor() as executor:
    while True:
        f1 = executor.submit(soil)
        f2 = executor.submit(temp)
        f3 = executor.submit(wlevel)
        Soil= 0
        Soil = (f1.result())
        Humidity = 0
        Humidity = (f2.result())[0]
        Temperature = 0
        Temperature = (f2.result())[1]
        Heat = 0
        Heat = (f2.result())[2]
        level = 0
        level = (f3.result())
        print(Soil ,Temperature, Humidity, Heat, level )
        f3 = executor.submit(lcdInfo,Soil ,Temperature, Humidity, Heat, level )
        f4 = executor.submit(mqTT,Soil ,Temperature, Humidity, Heat, level)
        sleep(20)




