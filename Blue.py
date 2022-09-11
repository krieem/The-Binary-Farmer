#!/usr/bin/python
import serial
import time
import string
# reading and writing data from and to arduino serially. # rfcomm0 -> this could be different
ser = serial.Serial("/dev/rfcomm1", 9600)
ser.write(str.encode('Start\r\n'))

rawserial = ser.readline()
cookedserial = rawserial.decode('utf-8').strip('\r\n')
print(cookedserial)
