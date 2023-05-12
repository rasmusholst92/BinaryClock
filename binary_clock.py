from sense_hat import SenseHat, ACTION_PRESSED
import time, argparse

sense = SenseHat()

try:

    is_24_hour = None
    rotation = 0
    vertical = False
    am_pm = False

    OFF = [0, 0, 0]
    RED = [255, 0, 0]
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]


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

    def change_rotation(event):
        '''Skifter rotationen mellem 0 & 90 grader'''
        global rotation
        if event.action == ACTION_PRESSED:
            rotation = 0 if rotation == 90 else 90
            sense.rotation = rotation
            sense.clear()

    def set_rotation(event):
        global vertical
        if(event.action == ACTION_PRESSED):
            vertical = not vertical
            sense.clear()

    def set_24_hour(event):
        global am_pm
        if(event.action == ACTION_PRESSED):
            am_pm = False
            sense.clear()

    def set_12_hour(event):
        global am_pm
        if(event.action == ACTION_PRESSED):
            am_pm = True
            sense.clear()


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
            sense.clear()
            display(vertical, am_pm)

except KeyboardInterrupt:
    sense.show_message("Programmet slutter", scroll_speed = 0.06, text_colour = [255, 0, 0])