#!/usr/bin/env python


import serial, time, signal, sys
import wiringpi2 as wiringpi

wiringpi.wiringPiSetup()
wiringpi.pinMode(0,0)

s = serial.Serial()
s.baudrate = 9600
s.timeout = 0
s.port = "/dev/ttyAMA0"

try:
    s.open()
except serial.SerialException, e:
    sys.stderr.write("could not open port %r: %s\n" % (port, e))
    sys.exit(1)
    
def sigint_handler(signum, frame):
    print ("User interrupted, exiting \r")
    s.write("$$$ALL,OFF\r")
    sys.exit()
    
signal.signal(signal.SIGINT, sigint_handler)

def prikaz_opozorila():
    print ("SENZOR !!!")
    
    s.write("$$$P7,4,ON\r")
    s.write("$$$P7,5,ON\r")
    s.write("$$$P7,6,ON\r")
    s.write("$$$P8,4,ON\r")
    s.write("$$$P8,5,ON\r")
    s.write("$$$P8,6,ON\r")
    time.sleep(0.15)

    s.write("$$$P6,4,ON\r")
    s.write("$$$P6,5,ON\r")
    s.write("$$$P6,6,ON\r")
    s.write("$$$P9,4,ON\r")
    s.write("$$$P9,5,ON\r")
    s.write("$$$P9,6,ON\r")
    time.sleep(0.15)

    s.write("$$$P5,1,ON\r")
    s.write("$$$P5,2,ON\r")
    s.write("$$$P5,3,ON\r")
    s.write("$$$P5,4,ON\r")
    s.write("$$$P5,5,ON\r")
    s.write("$$$P5,6,ON\r")
    s.write("$$$P5,7,ON\r")
    s.write("$$$P5,8,ON\r")
    s.write("$$$P5,9,ON\r")
    s.write("$$$P10,1,ON\r")
    s.write("$$$P10,2,ON\r")
    s.write("$$$P10,3,ON\r")
    s.write("$$$P10,4,ON\r")
    s.write("$$$P10,5,ON\r")
    s.write("$$$P10,6,ON\r")
    s.write("$$$P10,7,ON\r")
    s.write("$$$P10,8,ON\r")
    s.write("$$$P10,9,ON\r")
    time.sleep(0.15)

    s.write("$$$P4,2,ON\r")
    s.write("$$$P4,3,ON\r")
    s.write("$$$P4,4,ON\r")
    s.write("$$$P4,5,ON\r")
    s.write("$$$P4,6,ON\r")
    s.write("$$$P4,7,ON\r")
    s.write("$$$P4,8,ON\r")
    s.write("$$$P11,2,ON\r")
    s.write("$$$P11,3,ON\r")
    s.write("$$$P11,4,ON\r")
    s.write("$$$P11,5,ON\r")
    s.write("$$$P11,6,ON\r")
    s.write("$$$P11,7,ON\r")
    s.write("$$$P11,8,ON\r")
    time.sleep(0.15)

    s.write("$$$P3,3,ON\r")
    s.write("$$$P3,4,ON\r")
    s.write("$$$P3,5,ON\r")
    s.write("$$$P3,6,ON\r")
    s.write("$$$P3,7,ON\r")
    s.write("$$$P12,3,ON\r")
    s.write("$$$P12,4,ON\r")
    s.write("$$$P12,5,ON\r")
    s.write("$$$P12,6,ON\r")
    s.write("$$$P12,7,ON\r")
    time.sleep(0.15)

    s.write("$$$P2,4,ON\r")
    s.write("$$$P2,5,ON\r")
    s.write("$$$P2,6,ON\r")
    s.write("$$$P13,4,ON\r")
    s.write("$$$P13,5,ON\r")
    s.write("$$$P13,6,ON\r")
    time.sleep(0.15)

    s.write("$$$P1,5,ON\r")
    s.write("$$$P14,5,ON\r")
    time.sleep(0.5)
    s.write("$$$ALL,OFF\r")
    
##    s.write("KEEP DISTANCE!      \r")
##    time.sleep(0.2)
##    s.write("$$$ALL,OFF\r")

    
while True:
    A=wiringpi.digitalRead(0)
    if A==1:
        prikaz_opozorila() 
 
    else:
        print ("NI GIBANJA")
        time.sleep(0.1)

