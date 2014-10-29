__author__ = 'beau'

from pyb import UART

class lcd():
    def __init__(self):
        #UART serial
        self.lcd = UART(3, 115200)  # init with given baudrate


        #set lcd to same baudrate
        b = bytearray(3)
        b[0] = 0x7C
        b[1] = 0x07
        b[2] = 0x36
        self.lcd.send(b)


        #set background duty
        b = bytearray(3)
        b[0] = 0x7C
        b[1] = 0x02
        b[2] = 80
        self.lcd.send(b)



    def clear(self):
        b = bytearray(2)
        b[0] = 0x7c
        b[1] = 0x00
        self.lcd.send(b)

    def send(self,string):
        self.lcd.send(string)

    def replace(self,string):
        self.clear()
        self.lcd.send(string)
