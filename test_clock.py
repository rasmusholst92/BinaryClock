from sense_emu import SenseHat, ACTION_PRESSED
import time
import argparse

OFF = [0, 0, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]


class BinaryClock:
    def __init__(self, vertical=False, am_pm=False):
        self.sense = SenseHat()
        self.vertical = vertical
        self.am_pm = am_pm
        self.rotation = 0
        self.sense.clear()

    def set_24_hour(self, event):
        '''Koden for 24 timers ur'''
        if event.action == ACTION_PRESSED:
            self.is_24_hour = True
            self.vertical = False

    def set_12_hour(self, event):
        '''Koden for 12 timers ur'''
        if event.action == ACTION_PRESSED:
            self.is_24_hour = False
            self.am_pm = True

    def set_rotation(self, event):
        '''Skifter rotationen mellem 0 & 90 grader'''
        if event.action == ACTION_PRESSED:
            self.rotation = 0 if self.rotation == 90 else 90
            self.vertical = True
            self.sense.rotation = self.rotation
            self.sense.clear()

    def dec_to_bin(self, value):
        binary = bin(value)[1:].zfill(8)
        return binary

    def get_binary_time(self):
        current_time = time.strftime("%H:%M:%S")
        hour, minute, second = current_time.split(":")
        hour = int(hour)
        if self.am_pm:
            if hour >= 12:
                if hour > 12:
                    hour -= 12
            if hour == 0:
                hour = 12
        binary_hour = self.dec_to_bin(int(hour))
        binary_minute = self.dec_to_bin(int(minute))
        binary_second = self.dec_to_bin(int(second))
        binary_time = binary_hour + binary_minute + binary_second
        return binary_time

    def display(self):
        binary_time = self.get_binary_time()
        for x in range(8):
            for y in range(8):
                pixel_index = x * 8 + y
                if(pixel_index > 23):
                    continue
                if binary_time[pixel_index] == "1":
                    if(self.vertical):
                        self.sense.set_pixel(x,y,(255,255,255))
                    else:
                        self.sense.set_pixel(y,x,(255,255,255))
                else:
                    if(self.vertical):
                        self.sense.set_pixel(x,y,(0,0,0))
                    else:
                        self.sense.set_pixel(y,x,(0,0,0))

    def r(self, event):
        if(event.action == ACTION_PRESSED):
            self.vertical = not self.vertical
            self.sense.clear()

    def a(self, event):
        if(event.action == ACTION_PRESSED):
            self.am_pm = False
            self.sense.clear()

    def p(self, event):
        if(event.action == ACTION_PRESSED):
            self.am_pm = True
            self.sense.clear()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vertical', action='store_true', help="Display vertical")
    parser.add_argument('--am_pm', action='store_true', help="Display 12-hour format")
    args = parser.parse_args()

    clock = BinaryClock(vertical=args.vertical, am_pm=args.am_pm)

    clock.sense.stick.direction_up = clock.r
    clock.sense.stick.direction_right = clock.a
    clock.sense.stick.direction_left = clock.p

    while True:
        clock.display()
        time.sleep(0.1)

if __name__ == '__main__':
    main()

