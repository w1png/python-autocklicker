from argparse import ArgumentParser
import keyboard
from pynput.mouse import Button, Controller
from time import sleep, time

MOUSE = Controller()
CPS = 10
MAX_CPS = 40
KEY = "x"
HOLD = False

def click(button=Button.left):
    MOUSE.press(button)
    sleep(0.01)
    MOUSE.release(button)

def hold_handler(held, button=Button.left):
    if held:
        MOUSE.press(button)
    else:
        MOUSE.release(button)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--cps", help=f"autoclicker's cps. Max cps is {MAX_CPS}. Default cps is {CPS}.")
    parser.add_argument("-k", "--key", help=f"autoclicker's start key. Default key is \"{KEY}\".")
    parser.add_argument("--hold", help="[True/False] hold on keystroke.")

    # Setting cps
    if parser.parse_args().cps:
        cps_raw = parser.parse_args().cps
        if int(cps_raw) >= MAX_CPS:
            CPS = MAX_CPS
        elif int(cps_raw) < 1:
            CPS = 1
        else:
            CPS = int(cps_raw)
    
    if parser.parse_args().key:
        KEY = parser.parse_args().key
    
    if parser.parse_args().hold:
        match parser.parse_args().hold.lower():
            case "true":
                HOLD = True
            case "false":
                HOLD = False

    print((f"CPS: {CPS}\n" if not HOLD else "") + f"Press \"{KEY}\" to activate/stop the autoclicker.")

    # Actual autoclicker
    active = False
    last_press = time()
    held = False

    while True:
        try:
            if keyboard.is_pressed(KEY) and time() > last_press+1: # Only register keystrocke a second after the last one
                last_press = time()
                active = not active
                held = active
                print("Activated." if active else "Stopped.")
            if active:
                if HOLD:
                    hold_handler(held)
                else:
                    click()
                    sleep(1./CPS-(1./CPS)*(CPS/100)) # it's still not really precise but it is close enough.
        except KeyboardInterrupt:
            print("\nStopped.")
            exit(0)
        finally:
            pass # Had to do this because it throws an error evey time the key is not pressed. A really poor design choice by the developers of the keyboard module imo.
            