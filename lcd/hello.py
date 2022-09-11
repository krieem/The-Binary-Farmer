#!/usr/bin/python3

from signal import signal, SIGTERM, SIGHUP, pause
from time import sleep
from rpi_lcd import LCD
import socket
import netifaces as ni
import serial
import string

hostname = socket.gethostname()    
IPAddr = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr'] 

ser = serial.Serial("/dev/rfcomm0", 9600) 
ser.write(str.encode('Start\r\n'))
while True:
    if ser.in_waiting > 0:
        rawserial = ser.readline()
        cookedserial = rawserial.decode('utf-8').strip('\r\n')
        print(cookedserial)


"""      
lcd = LCD()

def safe_exit(signum, frame):
    exit(1)

while True:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    lcd.text(hostname + ":-)",1)    
    lcd.text(IPAddr,2) 
    sleep(5)
    lcd.clear()
    lcd.text("   Norah Project",2)
    sleep(5)
    lcd.clear()
    lcd.text(" Temp: 35c ",1)
    lcd.text(" Moist: 35 ",2)
    sleep(5)
    lcd.text(" Plant is happy",1)
    lcd.text(" :-) ",2)
    sleep(5)
""" 