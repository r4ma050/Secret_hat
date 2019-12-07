# -*- coding: utf-8 -*-
from sense_hat import SenseHat
from .lib.init import show_message_break, passed, get_joystick, loading
from .lib import globals

import netifaces as ni
import time
import datetime
from multiprocessing import Process

"""
Display informations about the raspberry (system temperature, ip, date and time) and the Sense Hat (sensor temperature, pressure, compass, humidity )

"""

sense = SenseHat()
    # Sytem temp isn't finished
yellow = [0,0,255]

def main(color1, color2, speed):

    """
    Args :
        color1 (list or tuple) : rgb color code of titles
        color2 (list or tuple) : rgb color code of subtitles
        speed (float) : speed of the scrolling of message
    """

    passed()
    while globals.run:

        # Display ip
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 0:
            show_message_break("1:IP", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                while globals.direction != 'middle':
                    # Get raspberry's IP address
                    try:
                        ni.ifaddresses('eth0')
                        iface_eth = 'eth0'
                    except:
                        pass
                    try:
                        ni.ifaddresses('wlan0')
                        iface_wlan = 'wlan0'
                    except:
                        while globals.direction != 'middle':
                            show_message_break("Unable to get IP", color2, speed)
                            get_joystick()
                        passed()
                    ip_eth = ni.ifaddresses(iface_eth)[ni.AF_INET][0]['addr']
                    ip_wlan = ni.ifaddresses(iface_wlan)[ni.AF_INET][0]['addr']
                    show_message_break("eth0:{}, wlan0:{}".format(ip_eth, ip_wlan), color2, speed)
                    get_joystick()
                passed()
        passed(6)

        # System date and time
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 1:
            show_message_break("2:System time", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                while globals.direction != 'middle':
                    show_message_break(str(datetime.datetime.now()), color2, speed)
                    get_joystick()
                passed()
        passed(6)

        # System temperature
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 2:
            show_message_break("3:System temperature", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                while globals.direction != 'middle':
                    show_message_break(str(datetime.datetime.now()), color2, speed)
                    get_joystick()
                passed()
        passed(6)

        # Compass
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 3:
            show_message_break("4:Compass", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                loading_process = Process(target = loading, args = (color1,))
                loading_process.start()
                timeout = 5
                timeout_start = time.time()
                while time.time() < timeout_start + timeout:                # Calibration
                    sense.get_compass()
                loading_process.terminate()
                while globals.direction != 'middle':
                    show_message_break('Press ok!', color2, speed)
                    get_joystick()
                passed()
                while globals.direction != 'middle':
                    compass_process = Process(target = compass)
                    compass_process.start()
                    get_joystick()
                compass_process.terminate()

                passed()
        passed(6)

        # Sensor temperature
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 4:
            show_message_break("5:Sensor temperature", color1, speed)
            get_joystick()
            if globals.direction == 'left':
                passed()
                run = False
                break
            if globals.direction == 'middle':
                passed()
                while globals.direction != 'middle':
                        show_message_break("{} degrees C".format(round(sense.get_temperature(), 1)), color2, speed)
                        get_joystick()
                passed()
        passed(6)

        # Pressure
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 5:
            show_message_break("6:Pressure", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                while globals.direction != 'middle':
                    show_message_break("{} millibars".format(round(sense.get_pressure(), 3)), color2, speed)
                    get_joystick()
                passed()
        passed(6)

        # Humidity
        while globals.direction != 'down' and globals.direction != 'up' and globals.direction != 'left' and globals.section == 6:
            show_message_break("7:Humidity", color1, speed)
            get_joystick()
            if globals.direction == 'middle':
                passed()
                while globals.direction != 'middle':
                    show_message_break("{} %".format(round(sense.get_humidity(), 3)), color2, speed)
                    get_joystick()
                passed()
        passed(6)
    passed()



def compass():

    """Simple compass displaying numbers between cardinal points

    """
    state_changed = 0
    while True:
        degrees = sense.get_compass()
        if (degrees <= 15 or degrees >= 345) and state_changed != 1:
            sense.clear()
            sense.show_letter("N")
            state_changed = 1
        elif degrees >= 15 and degrees < 30 and state_changed != 2:
            sense.clear()
            sense.show_letter("1")
            state_changed = 2
        elif degrees >= 30 and degrees < 45 and state_changed != 3:
            sense.clear()
            sense.show_letter("2")
            state_changed = 3
        elif degrees >= 45 and degrees < 60 and state_changed != 4:
            sense.clear()
            sense.show_letter("3")
            state_changed = 4
        elif degrees >= 60 and degrees < 75 and state_changed != 5:
            sense.clear()
            sense.show_letter("4")
            state_changed = 5
        elif degrees >= 75 and degrees < 105 and state_changed != 6:
            sense.clear()
            sense.show_letter("E")
            state_changed = 6
        elif degrees >= 105 and degrees < 120 and state_changed != 7:
            sense.clear()
            sense.show_letter("6")
            state_changed = 7
        elif degrees >= 135 and degrees < 150 and state_changed != 8:
            sense.clear()
            sense.show_letter("7")
            state_changed = 8
        elif degrees >= 150 and degrees < 165 and state_changed != 9:
            sense.clear()
            sense.show_letter("8")
            state_changed = 9
        elif degrees >= 165 and degrees < 195 and state_changed != 10:
            sense.clear()
            sense.show_letter("S")
            state_changed = 10
        elif degrees >= 195 and degrees < 210 and state_changed != 11:
            sense.clear()
            sense.show_letter("8")
            state_changed = 11
        elif degrees >= 225 and degrees < 240 and state_changed != 12:
            sense.clear()
            sense.show_letter("7")
            state_changed = 12
        elif degrees >= 240 and degrees < 255 and state_changed != 13:
            sense.clear()
            sense.show_letter("6")
            state_changed = 13
        elif degrees >= 255 and degrees < 285 and state_changed != 14:
            sense.clear()
            sense.show_letter("W")
            state_changed = 14
        elif degrees >= 285 and degrees < 300 and state_changed != 15:
            sense.clear()
            sense.show_letter("4")
            state_changed = 15
        elif degrees >= 300 and degrees < 315 and state_changed != 16:
            sense.clear()
            sense.show_letter("3")
            state_changed = 16
        elif degrees >= 315 and degrees < 330 and state_changed != 17:
            sense.clear()
            sense.show_letter("2")
            state_changed = 17
        elif degrees >= 330 and degrees < 345 and state_changed != 18:
            sense.clear()
            sense.show_letter("1")
            state_changed = 18