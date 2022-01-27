from argparse import ArgumentParser
import keyboard
from pynput.mouse import Button, Controller
from time import sleep, time

MOUSE = Controller()
CPS = 10
MAX_CPS = 40
KEY = "x"

def click(button=Button.left):
    MOUSE.press(button)
    sleep(0.01)
    MOUSE.release(button)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--cps", help=f"autoclicker's cps. Max cps is {MAX_CPS}. Default cps is {CPS}.")
    parser.add_argument("-k", "--key", help=f"autoclicker's start key. Default key is \"{KEY}\".")

    # Setting cps
    if parser.parse_args().cps:
        cps_raw = parser.parse_args().cps
        if int(cps_raw) >= MAX_CPS:
            CPS = MAX_CPS
        elif int(cps_raw) < 1:
            CPS = 1
        else:
            CPS = int(cps_raw)

    print(f"CPS: {CPS}\nPress \"{KEY}\" to activate/stop the autoclicker.")

    # Actual autoclicker
    active = False
    last_press = time()

    while True:
        try:
            if keyboard.is_pressed(KEY) and time() > last_press+1: # Only register keystrocke a second after the last one
                last_press = time()
                active = not active
                print("Activated." if active else "Stopped.")
        except KeyboardInterrupt:
            print("\nStopped.")
            exit(0)
        finally:
            pass # Had to do this because it throws an error evey time the key is not pressed. A really poor design choice by the developers of the keyboard module imo.

        if active:
            click()
            sleep(1./CPS-(1./CPS)*(CPS/100)) # it's still not really precise but it is close enough.
            