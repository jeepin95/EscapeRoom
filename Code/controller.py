'''
Code used for the timer controller on the DEC escape room in a box.

The clock does not start until a pin is pulled low. The clock will stop
once the stop pin is pulled low. There is no "reset" or "resume" other than
power cycling the controller.

Author: Josh Keller
Date: 3/18/2022
'''
from machine import Pin, Timer
from utime import sleep
import utime
import time
import tm1637
from DFPlayer import dfplayer

DEBUG = False

# Define the total number of minutes available for the game
TOTAL_MINUTES = 90

# Configure the MP3 player on pins 16 and 17
mp3 = dfplayer(0, 16, 17)

if DEBUG == True:
    mp3.play_track(5,40)

# Create the clock display
clock_display = tm1637.TM1637(clk=Pin(3), dio=Pin(2))

# Configure Pins

# Start pin is connected to a switch that should go low to start the timer
# No debounce necessary as the pin is only read until the first time it is low
start_pin = Pin(26, mode=Pin.IN, pull=Pin.PULL_UP)
print("Start Pin: ", start_pin.value())

# Stop pin is pulled high and configured later with an interrupt
# Pulling low immediatly stops the timer and it cannot be restarted
stop_pin = Pin(22, mode=Pin.IN, pull=Pin.PULL_UP)

# Identify folder and track for various MP3 files
MINUTES_REMAINING_50 = {'folder':5, 'track':50}
MINUTES_REMAINING_40 = {'folder':5, 'track':40}
MINUTES_REMAINING_30 = {'folder':5, 'track':30}
MINUTES_REMAINING_20 = {'folder':5, 'track':20}
MINUTES_REMAINING_10 = {'folder':5, 'track':10}
MINUTES_REMAINING_5 = {'folder':5, 'track':5}
ALARM_SOUND = {'folder':5, 'track':100}
WIN_SOUND = {'folder':5, 'track':102}
GAME_START = {'folder':5, 'track':103}

# Seconds for each time remaining warning
WARNING_50 = 60*50
WARNING_40 = 60*40
WARNING_30 = 60*30
WARNING_20 = 60*20
WARNING_10 = 60*10
WARNING_5 = 60*5

# Has the warning been issued
WARNING_50_ISSUED = False
WARNING_40_ISSUED = False
WARNING_30_ISSUED = False
WARNING_20_ISSUED = False
WARNING_10_ISSUED = False
WARNING_5_ISSUED = False

# Total time in seconds
total_time = 60*TOTAL_MINUTES

# Global variables to store the remaining minutes and seconds
m = 0
s = 0
puzzle_complete = False
last_time = 0
brightness = 7



# Initialize the display
clock_display.brightness(brightness)
clock_display.show("----")
sleep(1)
clock_display.numbers(TOTAL_MINUTES,00)


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
    '''
    IRQ handler for stopping the clock. Was originally designed to support multiple pins
    required for stopping the game. Some of that functionallity wasn't needed so was
    removed.
    '''
    global last_time, puzzle_complete
    new_time = utime.ticks_ms()

    if(new_time - last_time) > 200:
        puzzle_complete = True
        print("Puzzle complete")
        last_time = new_time

# Initialize IRQ handlers for puzzle completion
# stop_pin.irq(trigger=Pin.IRQ_FALLING, handler=stop_handler)

print(puzzle_complete)


game_started = False

# Loop forever until the start pin is pulled low
while game_started == False:
    val = start_pin.value()
    if DEBUG == True:
        print(val)
    if val == 0:
        game_started = True
    sleep(0.1)
        

# Play the introduction that the game has started
mp3.play_track(GAME_START['folder'], GAME_START['track'])

# Sleep 7 seconds to allow the start audo to complete before starting the clock
sleep(7)

# Initialize the timer
start_time = time.time()
end_time = start_time + total_time
print("Started: ", start_time)
print("End Time: ", end_time)

pin_low = False
ticks_us_pin = None

# Loop while there is still time remaining and all puzzles have not been completed
# TODO: Adjust this to that time will be counted up after it expires
while time.time() < end_time and puzzle_complete == False:
    now = time.time()
    m, s = get_numbers(end_time)
    clock_display.numbers(m, s)

    if stop_pin.value() == 0:
        if pin_low == False:
            pin_low = True
            ticks_us_pin = time.ticks_us()
        elif pin_low == True:
            if time.ticks_diff(time.ticks_us(), ticks_us_pin) > 400:
                puzzle_complete = True
    else:
        pin_low = False

    # Check and issue an MP3 time warning if needed
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
    

# Either time has expired or the puzzle has been completed. Check and respond appropriatly.

# Time must have expired, play an alarm sound
if puzzle_complete == False:
    mp3.play_track(ALARM_SOUND['folder'], ALARM_SOUND['track'])

# Initialize a timer that will be used to flash the clock
timer = Timer()


if time.time() >= end_time:
    # Time ran out, just show dashes
    clock_display.show("----")

else:
    # All puzzles completed under the time limit, flash the final time remaining
    timer.init(freq=1.5, mode=Timer.PERIODIC, callback=blink_clock)

    # Play the MP3 indicating a win
    mp3.play_track(WIN_SOUND['folder'], WIN_SOUND['track'])


