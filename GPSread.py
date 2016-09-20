import serial, signal
import pynmea2
ser=serial.Serial("/dev/ttyACM0",9600)

def sigint_handler(signum, frame):
    print ("User interrupted, exiting \r")
    sys.exit()

signal.signal(signal.SIGINT, sigint_handler)

while True:
    a=ser.readline()
    b=a.split(',')

    if b[0]=="$GPGGA":
        msg=pynmea2.parse(a)
        print msg.timestamp
        print msg.lat,msg.lat_dir
        print msg.lon,msg.lon_dir
        
    elif b[0]=="$GPVTG":
        msg=pynmea2.parse(a)
        print msg.spd_over_grnd_kmph,"km/h"
        print "\n"

##    elif b[0]=="$GPGSV":
##        msg=pynmea2.parse(a)
##        print msg.elevation_deg_1
##        print msg.elevation_deg_2
##        print "\n"        


