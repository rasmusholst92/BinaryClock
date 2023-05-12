from sense_hat import SenseHat, ACTION_PRESSED
import time, argparse, signal, sys

def term_handler(signum, frame):
    '''SIGTERM til nedlukning af service udefra'''
    sense.show_message("Programmet slutter", scroll_speed = 0.04, text_colour = [255, 0, 0])
    print("SIG INT/TERM activated")
    sys.exit(0)

signal.signal(signal.SIGTERM, term_handler)
signal.signal(signal.SIGINT, term_handler)

sense = SenseHat()

sense.show_message("Programmet starter", scroll_speed=0.04, text_colour=[0,255,0])

vertical = False
am_pm = False

OFF = [0, 0, 0]
RED = [255, 0, 0]   # Second
BLUE = [0, 0, 255]  # Minute
GREEN = [0, 255, 0] # Hour

def dec_to_bin(value):
    '''Konventerer decimaler til binært'''
    binary = bin(value)[1:].zfill(8)
    return binary

def get_binary_time(am_pm):
    '''Hentning af tid i binært'''
    current_time = time.strftime("%H:%M:%S")
    hour, minute, second = current_time.split(":")
    hour = int(hour)
    if (am_pm):
        if hour >= 12:
            if hour > 12:
                hour -=12
            if hour == 0:
                hour = 12
    binary_hour = dec_to_bin(int(hour))
    binary_minute = dec_to_bin(int(minute))
    binary_second = dec_to_bin(int(second))
    binary_time = binary_hour + binary_minute + binary_second
    return binary_time

def display(vertical, am_pm):
    '''Display af uret på Sense Hat'''
    binary_time = get_binary_time(am_pm)
    for x in range(8):
        for y in range(8):
            pixel_index = x * 8 + y
            if(pixel_index > 23):
                continue
            color = OFF
            if binary_time[pixel_index] == "1":
                if pixel_index < 8:
                    color = RED
                elif pixel_index < 16:
                    color = BLUE
                else:
                    color = GREEN
                if(vertical):
                    sense.set_pixel(x,y,color)
                else:
                    sense.set_pixel(y,x,color)

def set_rotation(event):
    '''Rotation af uret på Sense Hat'''
    global vertical
    if(event.action == ACTION_PRESSED):
        vertical = not vertical

def set_24_hour(event):
    '''Sætter uret til 24 timer visning'''
    global am_pm
    if(event.action == ACTION_PRESSED):
        am_pm = False

def set_12_hour(event):
    '''Sætter uret til 12 timer visning'''
    global am_pm
    if(event.action == ACTION_PRESSED):
        am_pm = True


sense.clear()

parser = argparse.ArgumentParser()
parser.add_argument('--vertical', type=str, default="false", help="Diplay vertical")
parser.add_argument('--am_pm', type=str,default="false", help="Display 12-hour format")
args = parser.parse_args()

if (args.vertical.lower() == 'true'):
    vertical = True

if (args.am_pm.lower() == 'true'):
    am_pm = True

while True:
        time.sleep(0.1)
        sense.stick.direction_up = set_rotation
        sense.stick.direction_right = set_24_hour
        sense.stick.direction_left = set_12_hour
        sense.stick.direction_down = set_rotation
        sense.clear()
        display(vertical, am_pm)