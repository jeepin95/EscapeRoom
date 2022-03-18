'''
Code for the DEC escape room switches game. Watches for pins to go high then sets an LED pin high.

When all switches are correct, sets a relay pin high to release a latch.

This puzzle was designed with SPDT switches in mind. The correct side of the switch is connected to the microcontroller,
the other side of the switch is directly connected to a different LED. The microcontroller only knows if the switch
is correct and is bypassed when the switch is off or incorrect.

Author: Josh Keller
Date: 3/18/2022
'''
from machine import Pin
from utime import sleep

DEBUG = True

# Configure the switch pins
SW1 = Pin(16, mode=Pin.IN, pull=Pin.PULL_DOWN)
SW2 = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN)
SW3 = Pin(18, mode=Pin.IN, pull=Pin.PULL_DOWN)
SW4 = Pin(19, mode=Pin.IN, pull=Pin.PULL_DOWN)
SW5 = Pin(20, mode=Pin.IN, pull=Pin.PULL_DOWN)

# Configure the LED pins
LED1 = Pin(15, mode=Pin.OUT)
LED2 = Pin(14, mode=Pin.OUT)
LED3 = Pin(13, mode=Pin.OUT)
LED4 = Pin(12, mode=Pin.OUT)
LED5 = Pin(11, mode=Pin.OUT)

# Configure the relay pin
RELAY = Pin(9, mode=Pin.OUT)

# In debug mode cycle the relay to ensure it is working
if DEBUG = True:
    RELAY.high()
    sleep(0.5)
    RELAY.low()

# Make lists of switches and LEDs in the same order
switches = [SW1, SW2, SW3, SW4, SW5]
leds = [LED1, LED2, LED3, LED4, LED5]

# In debug mode cycle the LEDs
# Don't leave debug on or it will give away the answer
if DEBUG == True:
    for led in leds:
        led.low()
        sleep(.2)
        led.high()
        sleep(.2)
        led.low()

# Current switch state
current_state = [0, 0, 0, 0, 0]

# Loop forever
while True:
    # Loop through all switches and check their state
    for i, sw in enumerate(switches):
        # If the switch is correct, set the LED and update the list
        if sw.value() == True:
            leds[i].high()
            current_state[i] = 1

        # If the switch is low turn off the LED and update the list
        else:
            leds[i].low()
            current_state[i] = 0
    
    # Quick check if the puzzle is solved
    if sum(current_state) == 5:
        print("Puzzle solved")
        # Set the relay high, it will remain high as long as the switches are correct
        # TODO Should this be timed in case the latch is not connected with a cutoff switch??
        RELAY.high()

    # Set the relay low if the switches are not all flipped
    else:
        RELAY.low()
        

