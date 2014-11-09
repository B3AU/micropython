__author__ = 'beau'

import pyb
from FIR import FIR

class MAX31885():

    def __init__(self,CS_pin='Y5',SO_pin='Y7',SCK_pin='Y6'):
        #Thermocouple
        self.CS_pin = pyb.Pin(CS_pin, pyb.Pin.OUT_PP)
        self.CS_pin.high()

        self.SO_pin = pyb.Pin(SO_pin, pyb.Pin.IN)
        self.SO_pin.low()

        self.SCK_pin = pyb.Pin(SCK_pin, pyb.Pin.OUT_PP)
        self.SCK_pin.low()

        self.last_read_time = 0
        self.last_read_room_temp = 0
        self.last_read_tc_temp = 0
        self.fault = 0
        self.open_circuit = 0
        self.short_to_gnd = 0
        self.short_to_vcc = 0

        self.FIR = FIR(window_size=16,div=8)


    def read(self):
        # self.CS_pin.low()
        # pyb.delay(2)
        # self.CS_pin.high()
        # pyb.delay(220)

        #check if new reading should be available
        #if True:
        if pyb.millis()-self.last_read_time > 100:

            #/*
            #  Bring CS pin low to allow us to read the data from
            #  the conversion process
            #*/
            self.CS_pin.low()

            #
            # Read bits D[31:18] for the Temp. Loop for each bit reading
            #   the value and storing the final value in 'temp'
            #
            tc_temp = 0

            self.SCK_pin.high()
            sign = self.SO_pin.value()
            self.SCK_pin.low()
            for i in range(13):
                self.SCK_pin.high()
                read = self.SO_pin.value()
                read = (read << 13 - i)
                tc_temp += read
                self.SCK_pin.low()
            if sign == 1:
                tc_temp*=-1
            self.FIR.push(tc_temp)
            tc_temp/=8.0



            # D17 dummy
            self.SCK_pin.high()
            pyb.delay(1)
            self.SCK_pin.low()

            # D16 fault
            self.SCK_pin.high()
            self.fault = self.SO_pin.value()
            self.SCK_pin.low()


            # D15-D4
            # Roomtemp, signed
            self.SCK_pin.high()
            sign = self.SO_pin.value()
            self.SCK_pin.low()
            room_temp = 0
            for i in range(11):
                self.SCK_pin.high()
                read = self.SO_pin.value()
                read = (read << 11 - i)
                room_temp += read
                self.SCK_pin.low()
            if sign == 1:
                room_temp*=-1
            room_temp/=32.0

            # D3 dummy
            self.SCK_pin.high()
            pyb.delay(1)
            self.SCK_pin.low()

            # D2 fault
            self.SCK_pin.high()
            self.short_to_vcc = self.SO_pin.value()
            self.SCK_pin.low()

            # D1 fault
            self.SCK_pin.high()
            self.short_to_gnd = self.SO_pin.value()
            self.SCK_pin.low()

            # D0 fault
            self.SCK_pin.high()
            self.open_circuit = self.SO_pin.value()
            self.SCK_pin.low()



            self.CS_pin.high()


            self.last_read_time = pyb.millis()
            self.last_read_room_temp = room_temp
            self.last_read_tc_temp = tc_temp


            return tc_temp,room_temp

        #to soon for new reading
        else:
            return self.last_read_tc_temp,self.last_read_room_temp