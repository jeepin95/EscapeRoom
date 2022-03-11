from machine import Pin
from utime import sleep
from code_flasher import morse_code


PINS_LEFT = [2, 3, 4, 5, 6, 7, 8, 9]
PINS_RIGHT = [10, 11, 12, 13, 21, 20, 19, 18]
LED_PIN = 22

morse_flasher = morse_code(LED_PIN)

pins_l = []
pins_r = []
connected_pins = []

def pin_id(pin):
    '''
    Return the pin number as an integer
    '''
    return int(str(pin)[4:6].rstrip(","))

for p in PINS_LEFT:
    pin = Pin(p, mode=Pin.IN, pull=Pin.PULL_DOWN)
    pin.low()
    pins_l.append(pin)

for p in PINS_RIGHT:
    pin = Pin(p, mode=Pin.IN, pull=Pin.PULL_DOWN)
    pin.low()
    pins_r.append(pin)

print("Connect the wires v1.1")
while True:
    connected_pins = []
    for i,p in enumerate(pins_l):
        pin_connected = False
        connected_pin = None
        pin_correct = False
        p.init(p.IN, p.PULL_DOWN)
        for pr in pins_r:
            pr.init(pr.OUT)
            pr.high()
            if p.value() == True:
                pin_connected = True
                connected_pin = pin_id(pr)
                if PINS_RIGHT[i] == connected_pin:
                    pin_correct = True
                connected_pins.append(connected_pin)
            pr.init(pr.IN, pr.PULL_DOWN)
    print(connected_pins)
    if connected_pins == PINS_RIGHT:
        print("Puzzle Complete")
        morse_flasher.display("call fcc")




