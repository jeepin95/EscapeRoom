from machine import Pin
from utime import sleep

SW1 = Pin(16, mode=Pin.IN, pull=Pin.PULL_DOWN)
SW2 = Pin(17, mode=Pin.IN, pull=Pin.PULL_DOWN)
SW3 = Pin(18, mode=Pin.IN, pull=Pin.PULL_DOWN)
SW4 = Pin(19, mode=Pin.IN, pull=Pin.PULL_DOWN)
SW5 = Pin(20, mode=Pin.IN, pull=Pin.PULL_DOWN)

LED1 = Pin(15, mode=Pin.OUT)
LED2 = Pin(14, mode=Pin.OUT)
LED3 = Pin(13, mode=Pin.OUT)
LED4 = Pin(12, mode=Pin.OUT)
LED5 = Pin(11, mode=Pin.OUT)

RELAY = Pin(9, mode=Pin.OUT)
# RELAY.high()
# sleep(0.5)
RELAY.low()

switches = [SW1, SW2, SW3, SW4, SW5]
leds = [LED1, LED2, LED3, LED4, LED5]

for led in leds:
    led.low()
    sleep(.2)
    led.high()
    sleep(.2)
    led.low()

current_state = [0, 0, 0, 0, 0]

while True:
    for i, sw in enumerate(switches):
        if sw.value() == True:
            leds[i].high()
            current_state[i] = 1
        else:
            leds[i].low()
            current_state[i] = 0
    
    if sum(current_state) == 5:
        print("Puzzle solved")
        RELAY.high()
    else:
        RELAY.low()
        

