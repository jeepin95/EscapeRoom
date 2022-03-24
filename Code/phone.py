'''
Code for the phone module in the DEC escape room.

Requires a 3x4 keypad, call button, hang up button, MP3 player and relay connected.

Author: Josh Keller
Date: 3/18/2022
'''
from machine import Pin
import utime
import time
from DFPlayer import dfplayer

DEBUG = True

# Configure pins for the buttons and relay
call_pin = Pin(21, mode=Pin.IN, pull=Pin.PULL_UP)
end_pin = Pin(20, mode=Pin.IN, pull=Pin.PULL_UP)
relay_pin = Pin(26, mode=Pin.OUT, pull=Pin.PULL_DOWN)

# Ensure pins start as they should
relay_pin.low()
call_pin.high()
end_pin.high()

KEY_UP = 0
KEY_DOWN = 1

# ROW_1 = Keypad Pin 2 (Blue)
# ROW_2 =  Keypad Pin 7 (Brown)
# ROW_3 =  Keypad Pin 6 (Red)
# ROW_4 =  Keypad Pin 4 (Yellow)
# COL_1 = Keypad Pin 3 (Green)
# COL_2 = Keypad Pin 1 (Purple)
# COL_3 = Keypad Pin 5 (Orange)

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



key_map = [
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9'],
    ['*','0','#']
]

def keypad_3x4_read(cols, rows, keys):
    """Reads the columns and rows from the matrix and returns the key based on the keys map supplied

    Args:
        cols (List): List of pins for the columns
        rows (List): List of pins for the rows
        keys (Matrix): Matrix representing the characters mapped to each key

    Returns:
        String: The character from the keys matrix that was pressed
    """
    key = None
    for y,row in enumerate(rows):
        for x,col in enumerate(cols):
            rows[y].high()
            if cols[x].value() == KEY_DOWN:
                key = KEY_DOWN
            if cols[x].value() == KEY_UP:
                key = KEY_UP
            rows[y].low()
            if key == KEY_DOWN:
                if DEBUG == True:
                    print("Key Pressed: ", keys[x][y])
                return keys[x][y]

# Used to keep the list of keys that have been pressed
keys_used = []

if DEBUG == True:
    mp3 = dfplayer(0, 16, 17)

# The track numbers used for each keypress
key_tracks = {
    '1':1,
    '2':2,
    '3':3,
    '4':4,
    '5':5,
    '6':6,
    '7':7,
    '8':8,
    '9':9,
    '0':10,
    '*':11,
    '#':12
}

# List of possible valid answers with actions to perform when dialed. Answers can be as long or short as needed
# mode = MP3 plays the MP3 track from folder
# mode = PIN sets the pin_high to high
# {'answer':['',''], 'mode':'MP3|PIN', 'folder':int, 'track':int, 'pin_high':None|Pin}
valid_answers = [
    {'answer':['2','0','2','8','5','2','2','5','8','5'], 'mode':'MP3', 'folder':1, 'track':1, 'pin_high':None},
    {'answer':['2','0','5','7','2','3','2','0','2','1'], 'mode':'PIN', 'folder':1, 'track':2, 'pin_high':relay_pin},
    {'answer':['2','5','2','4','4','7','1','5','4','5'], 'mode':'MP3', 'folder':1, 'track':3, 'pin_high':None},
]

if DEBUG == True:
    valid_answers.append({'answer':['2','0'], 'mode':'PIN', 'folder':1, 'track':2, 'pin_high':relay_pin})


def verify_answer(answer, answer_list):
    """Checks to see if the answer is in the answers list

    Args:
        answer (List): List of strings of keys pressed
        answer_list (List): List of dicts of potential answers with corresponding sound tracks
    """

    valid = None
    if DEBUG == True:
        print("DEBUG (verify_answer): ", answer, answer_list)
    for i,elem in enumerate(answer_list):
        if elem['answer'] == answer:
            valid = i
    print(valid)
    if valid is not None:
        return answer_list[valid]
    else:
        # The number dialed does not match a valid answer so play a standard track
        return {'answer':[], 'mode':'MP3', 'folder':1, 'track':4}

# Used when the place call button is pressed
def place_call():
    global keys_used, valid_answers
    print("Call placed")
    result = verify_answer(keys_used, valid_answers)

    # If the answer was an MP3, play the MP3
    if result['mode'] == 'MP3':
        print(result)
        mp3.play_track(result['folder'], result['track'])

    # If the answer sets a pin high, do that for 0.5 seconds then return to low
    elif result['mode'] == 'PIN':
        result['pin_high'].high()
        utime.sleep(0.5)
        result['pin_high'].low()

    # Clear out the keys used
    keys_used = []

# Used when the end call button is pressed
def end_call():
    global keys_used

    # Pause an MP3 if it is playing
    mp3.pause()

    # Reset the keys used
    keys_used = []
    print("Call ended")

# Configure interrupts for the call and end buttons
# call_pin.irq(place_call, Pin.IRQ_FALLING)
# end_pin.irq(end_call, Pin.IRQ_FALLING)

call_low = False
end_low = False
call_ticks = None
end_ticks = None

# Loop forever
while True:

    if call_pin.value() == 0:
        if call_low == False:
            call_low = True
            call_ticks = time.ticks_us()
        elif call_low == True:
            if time.ticks_diff(time.ticks_us(), call_ticks) > 400:
                place_call()
                call_ticks = time.ticks_us()
    else:
        call_low = False

    if end_pin.value() == 0:
        if end_low == False:
            end_low = True
            end_ticks = time.ticks_us()
        elif end_low == True:
            if time.ticks_diff(time.ticks_us(), end_ticks) > 400:
                end_call()
                end_ticks = time.ticks_us()
    else:
        end_low = False


        
    key = keypad_3x4_read(col_pins, row_pins, key_map)
    if key != None:
        # Delay .2 seconds, if key is held it will be repeated
        # There is a built in 500ms delay when playing the MP3
        utime.sleep(0.2)
        keys_used.append(key)
        if key in key_tracks.keys():
            mp3.play_track(2, key_tracks[key])
        print(keys_used)







    