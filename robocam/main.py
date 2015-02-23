__author__ = 'beau'
import serial
ser = serial.Serial('/dev/tty.usbmodem1422',9600, timeout=1)
import time
import sys

def get_angle():
    print "requesting angle"
    start = time.time()

    ser.write('nofddfp\n')
    print "..."
    reply = ser.readline()
    deltaT = time.time()-start
    print reply
    print "round-trip time {}".format(deltaT)
    sys.stdout.flush()

while True:
    get_angle()
    print "-------------"

    #time.sleep(0.1)