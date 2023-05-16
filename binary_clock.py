#!/usr/bin/env python3

from sense_hat import SenseHat, ACTION_PRESSED
import time, argparse, signal, sys
from flask import Flask, jsonify
from threading import Thread

#  cd /lib/systemd/system
# sudo systemctl status binary_clock.service

# python3 binary_clock.py --vertical "true" --am_pm "true"

# pandoc binary_clock.1.md -s -t man -o binary_clock.1
# man -l binary_clock.1

# Handler til at kunne stoppe servicen via ^C  eller et eksternt terminal vindue
def term_handler(signum, frame):
    '''SIGTERM til nedlukning af service udefra'''
    sense.show_message("Programmet slutter", scroll_speed = 0.04, text_colour = [255, 0, 0]) # Slut besked
    print("SIG INT/TERM activated")
    sys.exit(0)

signal.signal(signal.SIGTERM, term_handler) # SIGTERM for lukning via terminal (sudo kill)
signal.signal(signal.SIGINT, term_handler)  # SIGINT for lukning via control C (^C)

sense = SenseHat()

sense.show_message("Programmet starter", scroll_speed=0.04, text_colour=[0,255,0]) # Start besked

three_lines = False
vertical = False        # Global til vertikal og horisontal visning
am_pm = False           # Global til skiftning af 24 og 12 timer ur
TIME_SEGMENT = 8        # Global til timer
MINUTE_SEGMENT = 16     # Global til minutter
SECOND_SEGMENT = 24     # Global til sekunder

# Farver til pixels
OFF = [0, 0, 0]
RED = [255, 0, 0]   # Second
BLUE = [0, 0, 255]  # Minute
GREEN = [0, 255, 0] # Hour

# Decimaler konventeres til binært (det er jo et binært ur)
def dec_to_bin(value):
    '''Konventerer decimaler til binært'''
    binary = bin(value)[1:].zfill(8)
    return binary

# Opsætning af hvordan uret skal kører og vise tiden
def get_binary_time(am_pm):
    '''Hentning af tid i binært'''
    hour, minute, second = time.localtime()[3:6]

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


def get_binary_time_for_three_lines(am_pm):
    '''Hentning af tid i binært'''
    hour, minute, second = time.localtime()[3:6]

    hour = int(hour)
    if (am_pm):
        if hour >= 12:
            if hour > 12:
                hour -=12
            if hour == 0:
                hour = 12

    binary_hour_tens = format(int(hour / 10), '08b')
    binary_hour_ones = format(int(hour % 10), '08b')
    binary_minute_tens = format(int(minute / 10), '08b')
    binary_minute_ones = format(int(minute % 10), '08b')
    binary_second_tens = format(int(second / 10), '08b')
    binary_second_ones = format(int(second % 10), '08b')

    binary_time = binary_hour_tens + binary_hour_ones + binary_minute_tens + binary_minute_ones + binary_second_tens + binary_second_ones

    return binary_time



 # Hvordan uret skal fremvises på RaspberryPi SenseHat modulet
def display(vertical: bool, am_pm: bool, three_lines: bool):
    '''Display af uret på SenseHat'''

    if(three_lines):
            binary_time = get_binary_time_for_three_lines(am_pm)
            hour_tens = binary_time[0:8]
            hour_ones = binary_time[8:16]
            minute_tens = binary_time[16:24]
            minute_ones = binary_time[24:32]
            second_tens = binary_time[32:40]
            second_ones = binary_time[40:48]

            segments = [
                (hour_tens, RED),
                (hour_ones, RED),
                (minute_tens, BLUE),
                (minute_ones, BLUE),
                (second_tens, GREEN),
                (second_ones, GREEN)
            ]

            for index, (segment, color) in enumerate(segments):
                for i in range(8):  # Poprawiony zakres dla każdego segmentu
                    if vertical:
                        if segment[i] == "1":
                            sense.set_pixel(index, i, color)
                    else:
                        if segment[i] == "1":
                            sense.set_pixel(i, index, color)
    else:    
        binary_time = get_binary_time(am_pm)
        for x in range(8):
            for y in range(8):
                pixel_index = x * 8 + y
                if(pixel_index > SECOND_SEGMENT - 1):
                    continue
                color = OFF
                if binary_time[pixel_index] == "1":
                    if pixel_index < TIME_SEGMENT:
                        color = RED # Sekunder vises i rødt
                    elif pixel_index < MINUTE_SEGMENT:
                        color = BLUE # Minuter vises i blår
                    else:
                        color = GREEN # Timer vises i grønt
                    if(vertical):
                        sense.set_pixel(x,y,color)
                    else:
                       sense.set_pixel(y,x,color)                       
# Toggle eventet
def toggle_lines(event):
    '''Rotation af uret på Sense Hat'''
    global three_lines
    if(event.action == ACTION_PRESSED):
        three_lines = not three_lines

# Rotations eventet
def set_rotation(event):
    '''Rotation af uret på Sense Hat'''
    global vertical
    if(event.action == ACTION_PRESSED):
        vertical = not vertical

# 24 timer eventet
def set_24_hour(event):
    '''Sætter uret til 24 timer visning'''
    global am_pm
    if(event.action == ACTION_PRESSED):
        am_pm = False # Hvis false er den på 24 timers visning

# 12 timer eventet
def set_12_hour(event):
    '''Sætter uret til 12 timer visning'''
    global am_pm
    if(event.action == ACTION_PRESSED):
        am_pm = True # Hvis true er den på 12 timers visning


sense.clear()

parser = argparse.ArgumentParser()
parser.add_argument('--vertical', type=str, default="false", help="Diplay vertical")
parser.add_argument('--am_pm', type=str,default="false", help="Display 12-hour format")
args = parser.parse_args()

if (args.vertical.lower() == 'true'):
    vertical = True

if (args.am_pm.lower() == 'true'):
    am_pm = True


# GET request der viser temperatur og luftfugtighed
app = Flask(__name__)
@app.route('/', methods=['GET'])
def sensehat_data():
    '''Aflæser temp og luftfugtighed, returnere det i JSON format'''
    temprature = sense.get_temperature()
    humidity = sense.get_humidity()
    data = {
        'temperature': temprature,
        'humidity': humidity
    }
    return jsonify(data)

def run_flask():
    app.run(port = 5000)

# Main så man-page kunne fungerer
def main():
    '''
    ENTRY POINT TO THE PROGRAM
    '''
    sense.stick.direction_up = set_rotation
    sense.stick.direction_right = set_24_hour
    sense.stick.direction_left = set_12_hour
    sense.stick.direction_down = toggle_lines

    while True:
            time.sleep(0.1)
            sense.clear()
            display(vertical, am_pm, three_lines)

if __name__ == '__main__':
    # Starter API via seperat thread.
    Thread(target=run_flask).start()

    main()
