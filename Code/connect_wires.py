'''
Code for the connect the wires game intended for use on a RP2040. Designed for 8x8 wire connections.

When all wires have been correctly connected a message will be displayed in morse code on an attached LED.

Assumes that the puzzle is designed for 8 pins that clearly connect to 8 other pins. Does not currently
support connections between pins on the same "side" of an 8x8 setup.

Author: Josh Keller
Date: 3/18/2022
'''
from machine import Pin
from utime import sleep
from code_flasher import morse_code

DEBUG = False

# Define the pins for each wire
ONE = 18
TWO = 19
THREE = 20
FOUR = 26
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

# Define the left and right side pins
PINS_LEFT = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT]
PINS_RIGHT = [BLUE, GREEN, BROWN, ORANGE, BLUE_W, GREEN_W, BROWN_W, ORANGE_W]

# Pin used or the LED morse code output
LED_PIN = 22

# Configure the LED pin for output and flash it as a test
led = Pin(LED_PIN, Pin.OUT)
if DEBUG == True:
    print("LED ON")
    led.high()
    sleep(2)
    print("LED OFF")
    led.low()

# Setup the morse code flasher
morse_flasher = morse_code(LED_PIN, 3)

# Placeholders for the pin lists and connected pins
pins_l = []
pins_r = []
connected_pins = []

def pin_id(pin):
    '''
    Return the pin number as an integer
    '''
    return int(str(pin)[4:6].rstrip(","))

# Loop through all left pins and configure them as input by default, ensure they are low
for p in PINS_LEFT:
    pin = Pin(p, mode=Pin.IN, pull=Pin.PULL_DOWN)
    pin.low()
    pins_l.append(pin)

# Loop through all right pins and configure them as input, ensure they are low
for p in PINS_RIGHT:
    pin = Pin(p, mode=Pin.IN, pull=Pin.PULL_DOWN)
    pin.low()
    pins_r.append(pin)


def read_pins():
    """Read the connection status of all pins.
    """
    global connected_pins
    connected_pins = [0, 0, 0, 0, 0, 0, 0, 0]

    # Loop through the left pins
    for i,p in enumerate(pins_l):

        # Ensure the pin is an input pulled low
        p.init(p.IN, p.PULL_DOWN)
        p.low()

        # Loop through all right pins
        for pr in pins_r:

            # Set the right pin as a high output
            pr.init(pr.OUT)
            pr.high()

            # Check the left pin to see if it is true. If so, we know this right pin is connected to the current left pin.
            if p.value() == True:
                pr_int = pin_id(pr)
                # Append this connection information to the connected_pins list
                connected_pins[i] = pr_int

            # Return the right pin to low and an input
            pr.low()
            pr.init(pr.IN, pr.PULL_DOWN)
    if DEBUG == True:
        print(connected_pins)
        sleep(0.1)

print("Connect the wires v1.5")

# Define one or more possible answers to watch for.
# The pins represent the right pins that should be connected in the order of the left pins they connect to.
# {'pins':[], 'name':'', 'msg':''}
answers = [
    {'pins':[ORANGE_W, ORANGE, GREEN_W, BLUE, BLUE_W, GREEN, BROWN_W, BROWN], 'name':'Standard', 'msg':'avsar'},
]

# Loop forever, if an answer is correct display a message.
# As long as the pins remain connected the message will be repeated.
# The entire message will be displayed even if the pins are disconnected before it has completed.
while True:
    read_pins()

    # Loop through the possible answers and see if anything matches the currently connected wires
    for i, answer in enumerate(answers):
        if connected_pins == answer['pins']:

            # If the answer matches, display the message on the LED
            print("Answer correct: ", answer['name'])
            morse_flasher.display(answer['msg'])





