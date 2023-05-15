from sense_hat import SenseHat, ACTION_PRESSED
import time, argparse, signal, sys
from flask import Flask, jsonify

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

# Hvordan uret skal fremvises på RaspberryPi SenseHat modulet
def display(vertical: bool, am_pm: bool):
    '''Display af uret på SenseHat'''

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

# Main så man-page kunne fungerer
def main():
    '''
    ENTRY POINT TO THE PROGRAM
    '''
    sense.stick.direction_up = set_rotation
    sense.stick.direction_right = set_24_hour
    sense.stick.direction_left = set_12_hour
    sense.stick.direction_down = set_rotation

    while True:
            time.sleep(0.1)
            sense.clear()
            display(vertical, am_pm)

if __name__ == '__main__':
    app.run(port = 5000)
    exit(main())
