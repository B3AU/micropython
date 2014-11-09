__author__ = 'beau'

from pyb import UART

class lcd():
    def __init__(self,uart=3):
        #UART serial
        self.lcd = UART(uart, 115200)  # init with given baudrate

        #set lcd to same baudrate
        b = bytearray(3)
        b[0] = 0x7C
        b[1] = 0x07
        b[2] = 0x36
        self.lcd.write(b)

        #set background duty
        b = bytearray(3)
        b[0] = 0x7C
        b[1] = 0x02
        b[2] = 80
        self.lcd.write(b)

    def clear(self):
        b = bytearray(2)
        b[0] = 0x7c
        b[1] = 0x00
        self.lcd.write(b)

    def send(self,string):
        self.lcd.write(string)

    def replace(self,string):
        self.clear()
        self.lcd.write(string)
