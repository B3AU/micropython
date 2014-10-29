__author__ = 'beau'

import pyb
import micropython
from MAX6675 import MAX6675
from PDM import PDM
from rotary import rotary
import lcd as LCD
from PID import PID

micropython.alloc_emergency_exception_buf(100)

pdm = PDM()
tc = MAX6675()
knob = rotary()
lcd = LCD.lcd()

pdm.set_output(0.7)

def get_temp():
    global tc
    return tc.FIR.get_value()*0.25

pid = PID(get_temp,pdm.set_output)


# sw = pyb.Switch()
# sw_state = 1
# def toggle():
#     global sw_state
#     if sw_state == 0:
#         sw_state = 1
#     else:
#         sw_state = 0
# sw.callback(toggle)


def main():
    prev_t = ''
    while True:#sw_state:
        temp,tc_err = tc.read()
        pid.set_point = knob.position
        pid.update()
        avg_temp = tc.FIR.get_value()*0.25
        avg_temp = str(avg_temp)
        t =     "Temperature  " + avg_temp[:4] + "C\r\r"
        t =  t+ "Setpoint     " + str(knob.position) + "C\r\r"
        t =  t+ "Output       "+str(pid.output)[:6]+ "%\r\r\r"
        t =  t+ "P: " + str(pid.P_value)[:5] + "  I: "+str(pid.I_value)[:5]+"\r"


        if t!=prev_t:
            lcd.replace(t)
            prev_t = t
        pyb.delay(50)

main()
