from machine import Pin
import utime
import time
from DFPlayer import dfplayer


call_pin = Pin(21, mode=Pin.IN, pull=Pin.PULL_UP)
end_pin = Pin(20, mode=Pin.IN, pull=Pin.PULL_UP)
call_pin.high()
end_pin.high()

row_list = [6, 7, 8, 9]
col_list = [13, 12, 11, 10]

for x in range(0,4):
    row_list[x] = Pin(row_list[x], mode=Pin.OUT)
    row_list[x].value(1)
    col_list[x] = Pin(col_list[x], mode=Pin.IN, pull=Pin.PULL_UP)

key_map = [['A', '3', '2', '1'],
           ['B', '6', '5', '4'],
           ['C', '9', '8', '7'],
           ['D', '#', '0', '*']]

def keypad_4x4_read(cols, rows):
    for r in rows:
        r.value(0)
        result = [cols[0].value(), cols[1].value(),
                  cols[2].value(), cols[3].value()]
        if min(result) == 0:
            key = key_map[int(rows.index(r))][int(result.index(0))]
            r.value(1)  # manages key keept pressed
            return(key)
        r.value(1)

keys_used = []

mp3 = dfplayer(0, 16, 17)
# mp3.play_track(2, 2)

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
    {'answer':['2','0','2','8','5','2','2','5','8','5'], 'folder':4, 'track':1, 'pin_high':None},
    {'answer':['4','0','4'], 'folder':2, 'track':2, 'pin_high':None},
    {'answer':['9','1','1'], 'folder':2, 'track':3, 'pin_high':None},
    {'answer':['*','*','*'], 'folder':2, 'track':4, 'pin_high':None},
    {'answer':['7','2','8','5','1','6','2','1','0','5'], 'folder':2, 'track':2, 'pin_high':None}
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
        return {'answer':[], 'folder':2, 'track':1}

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
    key = keypad_4x4_read(col_list, row_list)
    if key != None:
        utime.sleep(0.4)
        keys_used.append(key)
        if key in key_tracks.keys():
            mp3.play_track(3, key_tracks[key])
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
    