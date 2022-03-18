'''
Module for displaying morse code on an LED. 

Author: Josh Keller
Date: 3/18/2022
'''
from machine import Pin
from utime import sleep_ms


class morse_code:

    def __init__(self, led_pin, speed_wpm=5):
        """Generates morse code flashing on the provided pin, intended for use with an LED.

        Args:
            led_pin (int): The pin number to set high for the signal
            speed_wpm (int, optional): WPM rate to send code. Defaults to 5.
        """
        self.led = Pin(led_pin, mode=Pin.OUT, pull=Pin.PULL_DOWN)
        self.led.low()
        self.base_time_ms = int((60 / (50 * speed_wpm)) * 1000) # Calculate the base time unit in ms from the speed factor
        self.dot_length = int(self.base_time_ms) # Set the dot length to one time unit
        self.dash_length = int(self.base_time_ms * 3) # Set the dash lenght to 3 time units
        self.gap = int(self.base_time_ms) # Set the spacing between elements to 1 time unit
        self.letter_gap = int(self.base_time_ms * 3) # Set the spacing between letters to 3 time unites
        self.word_gap = int(self.base_time_ms * 7) # Set the word gap to 7 time units 
        print("base_time_unit: ", self.base_time_ms)
        self._morse = [
            ('A', '.-'),
            ('B', '-...'),
            ('C', '-.-.'),
            ('D', '-..'),
            ('E', '.'),
            ('F', '..-.'),
            ('G', '--.'),
            ('H', '....'),
            ('I', '..'),
            ('J', '.---'),
            ('K', '-.-'),
            ('L', '.-..'),
            ('M', '--'),
            ('N', '-.'),
            ('O', '---'),
            ('P', '.--.'),
            ('Q', '--.-'),
            ('R', '.-.'),
            ('S', '...'),
            ('T', '-'),
            ('U', '..-'),
            ('V', '...-'),
            ('W', '.--'),
            ('X', '-..-'),
            ('Y', '-.--'),
            ('Z', '--..'),
            ('0', '-----'),
            ('1', '.----'),
            ('2', '..---'),
            ('3', '...--'),
            ('4', '....-'),
            ('5', '.....'),
            ('6', '-....'),
            ('7', '--...'),
            ('8', '---..'),
            ('9', '----.'),
            (' ', ' ') # Account for spaces between words
        ]
    

    def _show_dot(self):
        self.led.high()
        print('.')
        sleep_ms(self.dot_length)
        self.led.low()
        sleep_ms(self.gap)
    
    def _show_dash(self):
        self.led.high()
        print('-')
        sleep_ms(self.dash_length)
        self.led.low()
        sleep_ms(self.gap)

    def _show_letter_gap(self):
        self.led.low()
        sleep_ms(self.letter_gap)

    def _show_space(self):
        self.led.low()
        sleep_ms(self.word_gap)

    def _show_end(self):
        """Flashes the LED rapidly to indicate the end of the message.
        """
        for x in range(0, 60):
            self.led.toggle()
            sleep_ms(25)
        sleep_ms(self.word_gap)
            

    def _encode(self, message):
        morse_code = []
        for character in message:
            dotdash = [code for code in self._morse if code[0] == character][0][1]
            morse_code.append(dotdash)
        return morse_code

    def display(self, message):
        """Sends the message to the identified pin

        Args:
            message (String): The string to send
        """
        encoded = self._encode(message.upper())
        for character in encoded:
            for digit in character:
                if digit == '.':
                    self._show_dot()
                elif digit == '-':
                    self._show_dash()
                elif digit == ' ':
                    self._show_space()
            self._show_letter_gap()
        self._show_end()


