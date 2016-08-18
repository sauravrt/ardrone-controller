import sys
import tty
import termios
from ardrone_con import ArDrone
# Interface to control drone


def getChar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def printUsage():
    print("\n\n")
    print("Keyboard commands:")
    print("\tq       - quit")
    print("\tt       - takeoff")
    print("\tl       - land")
    print("\t(space) - emergency shutoff")

print("""
NOTE:  This program assumes you are already connected to the
       drone's WiFi network.
""")

mydrone = ArDrone()
while True:
    printUsage()
    ch = getChar()
    if ch == 'q':
        exit(0)
    elif ch == 't':
        mydrone.takeoff()
    elif ch == 'l':
        mydrone.land()
    elif ch == ' ':
        mydrone.reset()
        mydrone.emergency()
    else:
        print("Invalid command!")
