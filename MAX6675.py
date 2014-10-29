__author__ = 'beau'

import pyb
from FIR import FIR

class MAX6675():

    def __init__(self,CS_pin='Y8',SO_pin='Y7',SCK_pin='Y6'):
        #Thermocouple
        self.CS_pin = pyb.Pin(CS_pin, pyb.Pin.OUT_PP)
        self.CS_pin.high()

        self.SO_pin = pyb.Pin(SO_pin, pyb.Pin.IN)
        self.SO_pin.low()

        self.SCK_pin = pyb.Pin(SCK_pin, pyb.Pin.OUT_PP)
        self.SCK_pin.low()

        self.last_read_time = 0
        self.last_read_temp = 0
        self.last_error_tc = 0

        self.FIR = FIR(20)


    def read(self):
        # self.CS_pin.low()
        # pyb.delay(2)
        # self.CS_pin.high()
        # pyb.delay(220)

        #check if new reading should be available
        #if True:
        if pyb.millis()-self.last_read_time > 220:

            #/*
            #  Bring CS pin low to allow us to read the data from
            #  the conversion process
            #*/
            self.CS_pin.low()

            #/* Cycle the clock for dummy bit 15 */
            self.SCK_pin.high()
            pyb.delay(1)
            self.SCK_pin.high()

            #/*
            # Read bits 14-3 from MAX6675 for the Temp. Loop for each bit reading
            #   the value and storing the final value in 'temp'
            # */
            value = 0
            for i in range(12):
                self.SCK_pin.high()
                read = self.SO_pin.value()
                read = (read << 12 - i)
                value += read
                self.SCK_pin.low()


            #/* Read the TC Input inp to check for TC Errors */
            self.SCK_pin.high()
            error_tc = self.SO_pin.value()
            self.SCK_pin.low()

            # /*
            #   Read the last two bits from the chip, faliure to do so will result
            #   in erratic readings from the chip.
            # */
            for i in range(2):
                self.SCK_pin.high()
                pyb.delay(1)
                self.SCK_pin.low()

            self.CS_pin.high()

            self.FIR.push(value)
            temp = (value * 0.25)
            self.last_read_time = pyb.millis()
            self.last_read_temp = temp
            self.last_error_tc = error_tc

            return temp,error_tc

        #to soon for new reading
        else:
            return self.last_read_temp,self.last_error_tc