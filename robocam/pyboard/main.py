import pyb
usb = pyb.USB_VCP()

# servo1 = pyb.Servo(1)
# servo2 = pyb.Servo(2)







def main_loop():
    while True:
        r = usb.readline()
        #usb.write("message received ")
        if r==b'angle':
            # X = servo1.angle()
            # Y = servo2.angle()
            # result = str(X)+" "+str(Y)
            usb.write("angle\n")

        else:
            usb.write(str(r))
            usb.write("   error\n")

        #pyb.delay(10)


main_loop()