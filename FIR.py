__author__ = 'beau'

import array
class FIR():
    """
        Finit impulse response filter, aka moving average.
    """
    def __init__(self, window_size=30):
        self.win_size = window_size
        self.a = array.array('l', window_size * [0])  # no double on pyboard? integers logic for now
        self.arr_position = 0
        self.sum = 0

    def push(self, value):
        old_val = self.a[self.arr_position]
        self.a[self.arr_position] = value
        self.arr_position += 1
        self.arr_position %= self.win_size
        self.sum -= old_val
        self.sum += value

    def get_value(self):
        return self.sum / self.win_size
