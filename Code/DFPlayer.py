from machine import UART, Pin
from utime import sleep_ms

class dfplayer:
    def __init__(self, uart_bus, tx, rx, volume=100):
        """Limited DFPlayer.mini functionality

        All commands sent will result in a 1000ms sleep
        Args:
            uart_bus (INT): UART Bus Number
            tx (Int): Pin number
            rx (Int): RX Pin number
            volume (Int): Initial volume percentage
        """
        self._uart = UART(uart_bus, baudrate=9600, bits=8, parity=None, stop=1, tx=Pin(tx), rx=Pin(rx))
        # self.set_device()
        # self.set_volume(volume) # TODO: Volume doesn't seem to work and crashes the DFPlayer
    
    def _checksum(self, msg):
        total = 0x00
        for b in msg:
            total += int.from_bytes(b, 'big')
        total += 1
        check = total.to_bytes(2, 'big')
        # print("Checksum: ", check)
        return check

    def _tx(self, cmd, lsb=b'\x00', msb=b'\x00'):
        msg = []
        
        msg.append(b'\xFF') # Version
        msg.append(b'\x06') # Lenth
        msg.append(bytes([cmd])) # Command to send
        msg.append(b'\x00') # Don't ask for feedback
        msg.append(lsb) # first parameter
        msg.append(msb) # second parameter
        # check = self._checksum(msg)
        # msg.append(check)

        msg.insert(0,b'\x7E') # Start message

        msg.append(b'\xEF') # stop message
        # print(msg)
        for chunk in msg:
            self._uart.write(chunk)
        sleep_ms(500)

    def set_volume(self, volume):
        """Set the DFPlayer output volume (NOT CURRENTLY WORKING)

        Args:
            volume (Int): Volume percentage 0-100
        """
        #! The volume command isn't working and crashes the DFPlayer
        # self._tx(0x06, chr(int(volume*0x1E/100)))
        pass


    def set_device(self, device=2):
        self._tx(0x09, b'\x00', b'\x02')



    def pause(self):
        """Pause playback on the DRPlayer
        """
        print("Pause")
        self._tx(0x0E)

    def play_track(self, folder, track):
        """Plays a track from the SD card

        Args:
            folder (Int): The folder number (01-99) to play from
            track (Int): The file to play (001-999)
        """
        print("Playing: {}, {}".format(folder,track))
        self._tx(0x0F, chr(folder), chr(track))

