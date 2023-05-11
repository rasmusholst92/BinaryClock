from sense_hat import SenseHat, ACTION_PRESSED
import time

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
        is_24_hour = False
        sense.show_letter("1")

def set_rotation(event):
    '''Skifter rotationen mellem 0 & 90 grader'''
    global rotation
    if event.action == ACTION_PRESSED:
        rotation = 0 if rotation == 90 else 90
        sense.rotation = rotation


while True:
    while is_24_hour is None:
        sense.show_letter("?")
        time.sleep(0.1)
        sense.stick.direction_right = set_24_hour
        sense.stick.direction_left = set_12_hour
        sense.stick.direction_up = set_rotation