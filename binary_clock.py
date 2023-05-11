from sense_hat import SenseHat, ACTION_PRESSED
import time
import argparse

sense = SenseHat()

is_24_hour = None
rotation = 0

def set_24_hour(event):
    '''Koden for 24 timers ur'''
    global is_24_hour
    if event.action == ACTION_PRESSED:
        is_24_hour = True
        sense.show_letter("2")

def set_12_hour(event):
    '''Koden for 12 timers ur'''
    if event.action == ACTION_PRESSED:
        global is_24_hour
        global am_pm
        is_24_hour = False
        am_pm = True
        sense.show_letter("1")

def set_rotation(event):
    '''Skifter rotationen mellem 0 & 90 grader'''
    global rotation
    global vertical
    if event.action == ACTION_PRESSED:
        rotation = 0 if rotation == 90 else 90
        vertical = True
        sense.rotation = rotation

def dec_to_bin(value):
    binary = bin(value)[1:].zfill(8)
    return binary

def get_binary_time(am_pm):
    current_time = time.strftime("%H:%M:%S")
    hour, minute, second = current_time.split(":")
    hour = int(hour)
    if (am_pm):
        if hour >= 12:
            if hour > 12:
                hour -=12
            if hour == 0:
                hour = 12
    hour = 12
    binary_hour = dec_to_bin(int(hour))
    binary_minute = dec_to_bin(int(minute))
    binary_second = dec_to_bin(int(second))
    binary_time = binary_hour + binary_minute + binary_second
    return binary_time

def display(vertical, am_pm):
    binary_time = get_binary_time(am_pm)
    for x in range(8):
        for y in range(8):
            pixel_index = x * 8 + y
            if(pixel_index > 23):
                continue
            if binary_time[pixel_index] == "1":
                if(vertical):
                    sense.set_pixel(x,y,(255,255,255))
                else:
                    sense.set_pixel(y,x,(255,255,255))
            else:
                if(vertical):
                    sense.set_pixel(x,y,(0,0,0))
                else:
                    sense.set_pixel(y,x,(0,0,0))

sense.clear()

parser = argparse.ArgumentParser()
parser.add_argument('--vertical', type=str, default="false", help="Diplay vertical")
parser.add_argument('--am_pm', type=str,default="false", help="Display 12-hour format")
args = parser.parse_args()

vertical = False
am_pm = False

if (args.vertical.lower() == 'true'):
    vertical = True

if (args.am_pm.lower() == 'true'):
    am_pm = True

while True:
    display(vertical, am_pm)


while True:
    while is_24_hour is None:
        time.sleep(0.1)
        sense.stick.direction_right = set_24_hour
        sense.stick.direction_left = set_12_hour
        sense.stick.direction_up = set_rotation
        display(vertical, am_pm)



