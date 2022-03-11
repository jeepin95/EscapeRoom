from machine import Pin
import utime
import time
from DFPlayer import dfplayer


call_pin = Pin(21, mode=Pin.IN, pull=Pin.PULL_UP)
end_pin = Pin(20, mode=Pin.IN, pull=Pin.PULL_UP)
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

keys_used = []

mp3 = dfplayer(0, 16, 17)
mp3.play_track(2, 2)

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


valid_answers = [
    {'answer':['2','0','2','8','5','2','2','5','8','5'], 'folder':1, 'track':1, 'pin_high':None},
    {'answer':['2','0','5','7','2','3','2','0','2','1'], 'folder':1, 'track':2, 'pin_high':None},
    {'answer':['2','5','2','4','4','7','1','5','4','5'], 'folder':1, 'track':3, 'pin_high':None},
]

def verify_answer(answer, answer_list):
    """Checks to see if the answer is in the answers list

    Args:
        answer (List): List of strings of keys pressed
        answer_list (List): List of dicts of potential answers with corresponding sound tracks
    """
    # valid = next((index for (index, elem) in enumerate(answer_list) if elem['answer'] == answer), None)

    valid = None
    print("DEBUG (verify_answer): ", answer, answer_list)
    for i,elem in enumerate(answer_list):
        if elem['answer'] == answer:
            valid = i
    print(valid)
    if valid is not None:
        return answer_list[valid]
    else:
        return {'answer':[], 'folder':1, 'track':4}

def place_call(pin):
    global keys_used, valid_answers
    print("Call placed")
    result = verify_answer(keys_used, valid_answers)
    print(result)
    mp3.play_track(result['folder'], result['track'])



    keys_used = []

def end_call(pin):
    global keys_used
    mp3.pause()
    keys_used = []
    print("Call ended")


call_pin.irq(place_call, Pin.IRQ_FALLING)
end_pin.irq(end_call, Pin.IRQ_FALLING)
mp3.play_track(2,3)

while True:
    key = keypad_3x4_read(col_pins, row_pins, key_map)
    if key != None:
        utime.sleep(0.4)
        keys_used.append(key)
        if key in key_tracks.keys():
            mp3.play_track(2, key_tracks[key])
        print(keys_used)






# button_state = p.value()
# while True:
#     b = p.value()
#     if b != button_state:
#         if b == True:
#             print("Button released")
#         else:
#             print("Button pressed")
#         button_state = b
    