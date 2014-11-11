__author__ = 'beau'
import pyb
import SPI
import math
import FIR


class MAX31865():
    def __init__(self,DRDY_pin='X9'):
        self.spi = SPI.SPI()
        self.fir = FIR.FIR(16)

        """
            Configuration bits:
            Vbias           1=on
            Conversion mode 1=auto,0=normally off
            1-shot          1=1-shot (auto-clear)
            3-wire          1=3-wire,0=2/4 wire
            Fault detection
            Fault detection
            Fault Status    1=clear
            Filter          1=50Hz,2=60Hz
        """

        config = 0b11000011

        buf = bytearray(2)
        buf[0] = 0x80 #configuration write addr
        buf[1] = config
        self.spi.write(buf)

        self.RefR = 100.0325 #RefR/2

        self.last_read_time = 0
        self.last_read_temp = 0
        self.last_FIR = 0


        self.conversion_time = 22 #21ms for 50Hz, 17.6 for 60Hz


    def _RawToTemp(self,raw):
        R0 = raw/(1<<15)*200
        R0 = R0/self.RefR*100
        if R0==0:
            return -1,0
        #ITS-90 IEC751 Pt-100 coefficients
        A = 3.90830e-3
        B = -5.77500e-7
        return (A - math.sqrt(A*A - 4*B*(1-100/R0) ) ) / (2*B),R0

    def read(self):
        if pyb.millis()-self.last_read_time > self.conversion_time:
            temp,avg_temp = self._read()
            self.last_read_temp = temp
            self.last_FIR = avg_temp
        return self.last_read_temp,self.last_FIR


    def _read(self):

        #read config
        #config = self.spi.read(0x00,1)[0]
        #print ("Config:"+str(bin(config)[2:]))

        #read data
        MSB = self.spi.read(0x01,1)[0]
        LSB = self.spi.read(0x02,1)[0]

        MSB = MSB<<8
        raw = MSB+LSB
        raw = raw>>1 #remove fault bit




        self.fir.push(raw)
        temp,R0 = self._RawToTemp(raw)
        avg_temp,avg_R0 = self._RawToTemp(self.fir.median())

        return temp,avg_temp

