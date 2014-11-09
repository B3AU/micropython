__author__ = 'beau'

import pyb

class SPI():
    def __init__(self,CS_pin='X10',SCK_pin='Y6',MISO_pin='Y7',MOSI_pin='Y8',delay=10):
        self.CS = pyb.Pin(CS_pin, pyb.Pin.OUT_PP)
        self.CS.high()

        self.MISO = pyb.Pin(MISO_pin,pyb.Pin.IN)
        self.MOSI = pyb.Pin(MOSI_pin,pyb.Pin.OUT_PP)

        self.SCK = pyb.Pin(SCK_pin, pyb.Pin.OUT_PP)
        self.delay = delay



    def write(self,data):
        self.CS.low()
        pyb.udelay(self.delay)
        self._write(data)
        self.CS.high()

    def read(self,read_addr,nr_bytes):
        buf = bytearray(1)
        buf[0]=read_addr
        self.CS.low()
        pyb.udelay(self.delay)
        self._write(buf)
        result = self._read(nr_bytes)
        self.CS.high()
        return result

    def _read(self,nr_bytes):
        buf = bytearray(nr_bytes)

        for b in range(nr_bytes):
            byte = 0
            for i in range(8):
                self.SCK.high()
                pyb.udelay(self.delay)
                read = self.MISO.value()
                read = (read << 8 - i)
                byte += read
                self.SCK.low()
                pyb.udelay(self.delay)
            buf[b]=byte

        return buf

    def _write(self,data):
        msb = 0b10000000

        for byte in data:
            bits = [(byte<<i&msb)/128 for i in range(8)]
            for b in bits:
                if b:
                    self.MOSI.high()
                else:
                    self.MOSI.low()
                self.SCK.high()
                pyb.udelay(self.delay)
                self.SCK.low()
                pyb.udelay(self.delay)

        self.MOSI.low()


