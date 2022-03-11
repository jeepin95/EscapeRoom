from machine import Pin
from utime import sleep
from code_flasher import morse_code


ONE = 18
TWO = 19
THREE = 20
FOUR = 21
FIVE = 2
SIX = 3
SEVEN = 4
EIGHT = 5
BLUE = 13
GREEN = 12
BROWN = 11
ORANGE = 10
BLUE_W = 9
GREEN_W = 8
BROWN_W = 7
ORANGE_W = 6

PINS_LEFT = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT]
PINS_RIGHT = [BLUE, GREEN, BROWN, ORANGE, BLUE_W, GREEN_W, BROWN_W, ORANGE_W]
LED_PIN = 22

led = Pin(LED_PIN, Pin.OUT)
print("LED ON")
led.high()
sleep(2)
print("LED OFF")
led.low()

morse_flasher = morse_code(LED_PIN, 3)

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

def read_pins():
    global connected_pins
    connected_pins = [0, 0, 0, 0, 0, 0, 0, 0]
    for i,p in enumerate(pins_l):
        p.init(p.IN, p.PULL_DOWN)
        p.low()
        for pr in pins_r:
            pr.init(pr.OUT)
            pr.high()
            if p.value() == True:
                pr_int = pin_id(pr)
                connected_pins[i] = pr_int
            pr.low()
            pr.init(pr.IN, pr.PULL_DOWN)

    print(connected_pins)

print("Connect the wires v1.5")
answers = [
    {'pins':[ORANGE_W, ORANGE, GREEN_W, BLUE, BLUE_W, GREEN, BROWN_W, BROWN], 'name':'Standard'},
]

while True:
    read_pins()
    for i, answer in enumerate(answers):
        if connected_pins == answer['pins']:
            print("Answer correct: ", answer['name'])
            morse_flasher.display('resources')


    # connected_pins = []
    # for i,p in enumerate(pins_l):
    #     pin_connected = False
    #     connected_pin = None
    #     pin_correct = False
    #     p.init(p.IN, p.PULL_DOWN)
    #     for pr in pins_r:
    #         pr.init(pr.OUT)
    #         pr.high()
    #         if p.value() == True:
    #             pin_connected = True
    #             connected_pin = pin_id(pr)
    #             if PINS_RIGHT[i] == connected_pin:
    #                 pin_correct = True
    #             connected_pins.append(connected_pin)
    #         pr.init(pr.IN, pr.PULL_DOWN)
    # print(connected_pins)
    # if connected_pins == PINS_RIGHT:
    #     print("Puzzle Complete")
    #     morse_flasher.display("call fcc")




