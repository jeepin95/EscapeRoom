from machine import Pin, Timer
from utime import sleep
import utime
import time
import tm1637
from DFPlayer import dfplayer

mp3 = dfplayer(0, 16, 17)

# mp3.play_track(5,40)
# Create the clock display
clock_display = tm1637.TM1637(clk=Pin(3), dio=Pin(2))

# Configure Pins
reset_pin = Pin(22, mode=Pin.OUT, pull=Pin.PULL_UP)
stop_pin = Pin(26, mode=Pin.IN, pull=Pin.PULL_UP)

MINUTES_REMAINING_50 = {'folder':5, 'track':50}
MINUTES_REMAINING_40 = {'folder':5, 'track':40}
MINUTES_REMAINING_30 = {'folder':5, 'track':30}
MINUTES_REMAINING_20 = {'folder':5, 'track':20}
MINUTES_REMAINING_10 = {'folder':5, 'track':10}
MINUTES_REMAINING_5 = {'folder':5, 'track':5}
ALARM_SOUND = {'folder':5, 'track':100}
WIN_SOUND = {'folder':5, 'track':102}

TOTAL_MINUTES = 11

WARNING_50 = 60*50
WARNING_40 = 60*40
WARNING_30 = 60*30
WARNING_20 = 60*20
WARNING_10 = 60*10
WARNING_5 = 60*5

WARNING_50_ISSUED = False
WARNING_40_ISSUED = False
WARNING_30_ISSUED = False
WARNING_20_ISSUED = False
WARNING_10_ISSUED = False
WARNING_5_ISSUED = False


reset_pin.low()
utime.sleep_ms(100)
reset_pin.high()


# Total time in seconds
total_time = 60*TOTAL_MINUTES

# Global variables to store the remaining minutes and seconds
m = 0
s = 0
puzzle_complete = [False, True, True]
last_time = 0
brightness = 7

# Initialize the display
clock_display.brightness(brightness)
clock_display.show("----")
sleep(1)
clock_display.numbers(60,00)


def pin_id(pin):
    '''
    Return the pin number as an integer
    '''
    return int(str(pin)[4:6].rstrip(","))

def get_numbers(end_time):
    '''
    Return the remaining minutes and seconds
    '''
    remaining_m = 0
    remaining_s = 0
    now = time.time()
    remaining = end_time - now

    if remaining >= 60:
        remaining_m, remaining_s = divmod(remaining, 60)
    else:
        remaining_s = remaining
    
    return (remaining_m, remaining_s)



def puzzle_handler(pin):
    global last_time, puzzle_1_complete, puzzle_2_complete, puzzle_3_complete
    new_time = utime.ticks_ms()

    if(new_time - last_time) > 200:
        puzzle = pin_id(pin)
        puzzle_complete[puzzle] = True
        print(pin)
        print(puzzle_complete)
        print("Fully Complete: ", all(puzzle_complete))
        last_time = new_time

def blink_clock(timer):
    '''
    Blink the clock 1.5 times per second
    '''
    global brightness
    if brightness == 7:
        brightness = 0
    else:
        brightness = 7
    clock_display.brightness(brightness)


def stop_handler(pin):
    global last_time
    new_time = utime.ticks_ms()

    if(new_time - last_time) > 200:
        puzzle_complete[0] = True
        print("Puzzle complete")
        last_time = new_time

# Initialize IRQ handlers for the 3 puzzle completion
# puzzle_1_pin.irq(trigger=Pin.IRQ_FALLING, handler=puzzle_handler)
# puzzle_2_pin.irq(trigger=Pin.IRQ_FALLING, handler=puzzle_handler)
# puzzle_3_pin.irq(trigger=Pin.IRQ_FALLING, handler=puzzle_handler)
stop_pin.irq(trigger=Pin.IRQ_FALLING, handler=stop_handler)

print(puzzle_complete)

# Initialize the timer
start_time = time.time()
end_time = start_time + total_time

# Loop while there is still time remaining and all puzzles have not been completed
while time.time() < end_time and not all(puzzle_complete):
    now = time.time()
    m, s = get_numbers(end_time)
    clock_display.numbers(m, s)
    if (WARNING_50_ISSUED == False and end_time-now < WARNING_50):
        mp3.play_track(MINUTES_REMAINING_50['folder'], MINUTES_REMAINING_50['track'])
        WARNING_50_ISSUED = True
    elif (WARNING_40_ISSUED == False and end_time-now < WARNING_40):
        mp3.play_track(MINUTES_REMAINING_40['folder'], MINUTES_REMAINING_40['track'])
        WARNING_40_ISSUED = True
    elif (WARNING_30_ISSUED == False and end_time-now < WARNING_30):
        mp3.play_track(MINUTES_REMAINING_30['folder'], MINUTES_REMAINING_30['track'])
        WARNING_30_ISSUED = True
    elif (WARNING_20_ISSUED == False and end_time-now < WARNING_20):
        mp3.play_track(MINUTES_REMAINING_20['folder'], MINUTES_REMAINING_20['track'])
        WARNING_20_ISSUED = True
    elif (WARNING_10_ISSUED == False and end_time-now < WARNING_10):
        mp3.play_track(MINUTES_REMAINING_10['folder'], MINUTES_REMAINING_10['track'])
        WARNING_10_ISSUED = True
    elif (WARNING_5_ISSUED == False and end_time-now < WARNING_5):
        mp3.play_track(MINUTES_REMAINING_5['folder'], MINUTES_REMAINING_5['track'])
        WARNING_5_ISSUED = True
    
    

if not all(puzzle_complete):
    mp3.play_track(ALARM_SOUND['folder'], ALARM_SOUND['track'])

timer = Timer()

if time.time() >= end_time:
    # Time ran out, just show dashes
    clock_display.show("----")
else:
    # All puzzles completed under the time limit, flash the final time remaining
    timer.init(freq=1.5, mode=Timer.PERIODIC, callback=blink_clock)
    mp3.play_track(WIN_SOUND['folder'], WIN_SOUND['track'])


