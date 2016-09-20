import serial, time, signal, sys
import wiringpi2 as wiringpi

wiringpi.wiringPiSetup()
wiringpi.pinMode(0,0)

s = serial.Serial()
s.baudrate = 115200
s.timeout = 0
s.port = "/dev/ttyAMA0"

try:
    s.open()
except serial.SerialException, e:
    sys.stderr.write("could not open port %r: %s\n" % (port, e))
    sys.exit(1)
    
def sigint_handler(signum, frame):
    print ("User interrupted, exiting \r")
    sys.exit()
    
signal.signal(signal.SIGINT, sigint_handler)

time.sleep(0.25)
s.write("t")
time.sleep(0.25)
s.write("5")

time.sleep(0.25)
s.write("s")
time.sleep(0.25)

while True:
    A=s.readline()
    print(A)
    s.flush()
    time.sleep(0.1)
#s.write("t")
#time.sleep(0.22)
#s.write("5")
#time.sleep(2)
s.close()
    
