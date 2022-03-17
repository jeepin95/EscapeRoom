from machine import Pin
from utime import sleep

KEY_UP = 0
KEY_DOWN = 1

col_pins = [
    Pin(6, mode=Pin.IN, pull=Pin.PULL_DOWN),
    Pin(7, mode=Pin.IN, pull=Pin.PULL_DOWN),
    Pin(8, mode=Pin.IN, pull=Pin.PULL_DOWN),
    Pin(9, mode=Pin.IN, pull=Pin.PULL_DOWN)
]

row_pins = [
    Pin(10, mode=Pin.OUT),
    Pin(11, mode=Pin.OUT),
    Pin(12, mode=Pin.OUT)
]

keys = [
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9'],
    ['*','0','#']
]

def init_keypad():
    for row in range(0,4):
        for col in range(0,3):
            rows[row].low()

def read_keys(cols, rows, keys):
    key = None
    for y,row in enumerate(rows):
        for x,col in enumerate(cols):
            # print(col)
            rows[y].high()
            if cols[x].value() == KEY_DOWN:
                key = KEY_DOWN
            if cols[x].value() == KEY_UP:
                key = KEY_UP
            rows[y].low()
            if key == KEY_DOWN:
                print("Key Pressed: ", keys[x][y])
                return keys[x][y]
                
while True:
    read_keys(col_pins, row_pins, keys)
