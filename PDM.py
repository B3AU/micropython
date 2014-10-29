__author__ = 'beau'

import pyb

class PDM():
    def __init__(self,pout='X11',tim=4,freq=50):
        """
        :param pout: output pin nr
        :param tim:  timer number
        :param freq: frequency of the bitstream
        """
        self.max = 2**24-1#2**31-1 crashes with larger ints? 24bit resolution is fine enough ;)

        self.pout = pyb.Pin(pout, pyb.Pin.OUT_PP)

        self.err = 0 # error accumulator
        self.output = 0

        self.freq = freq

        self.tim = pyb.Timer(tim)
        self.tim.init(freq=freq)
        self.tim.callback(lambda t: self.call_me())

    def set_output(self,out):
        """
        :param out: desired output as a value between 0 and 1
        """
        print ('setting output to '+str(out))
        self.tim.deinit()

        self.output = int(self.max*out)

        self.tim.init(freq=self.freq)
        self.tim.callback(lambda t: self.call_me())

    def call_me(self):
        if self.err >= 0:
            self.pout.low()
            self.err -= self.output
        else:
            self.pout.high()
            self.err += self.max
            self.err -= self.output