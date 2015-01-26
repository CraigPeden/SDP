import arduinoComm
import time
import curses


# Initializing the screen
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
stdscr.nodelay(1)

# Initializing the object which will handle communications
comms = arduinoComm.Communication("/dev/ttyACM0", 9600)

# Setup screen
stdscr.addstr(0,0,"Q          : quit")
stdscr.addstr(1,0,"UP         : go forwards")
stdscr.addstr(2,0,"DOWN       : go backwards")
stdscr.addstr(3,0,"LEFT       : steer left")
stdscr.addstr(4,0,"RIGHT      : steer right")
stdscr.addstr(5,0,"SPACE      : stop")
stdscr.addstr(6,0,"X          : grab")
stdscr.addstr(7,0,"C          : kick")
stdscr.addstr(10,9,"         ")
stdscr.refresh()

key_pressed = 0

def handle_key_press():
    if key_pressed == 0:
        stdscr.addstr(10, 9, "STOP     ")
        comms.drive(0,0)

    elif key_pressed == 1:
        stdscr.addstr(10, 9, "UP       ")
        comms.drive(7,7)

    elif key_pressed == 2:
        stdscr.addstr(10, 9, "DOWN     ")
        comms.drive(7,7, False, False)

    elif key_pressed == 3:
        stdscr.addstr(10, 9, "LEFT     ")
        comms.drive(5, 5, False, True)

    elif key_pressed == 4:
        stdscr.addstr(10, 9, "RIGHT    ")
        comms.drive(5, 5, True, False)

    elif key_pressed == 5:
        stdscr.addstr(10, 9, "GRAB     ")
        comms.grab()

    elif key_pressed == 6:
        stdscr.addstr(10, 9, "KICK     ")
        comms.kick()

# Starts listening for input
key = ''
while key != ord('q') and key != ord('Q'):
    key = stdscr.getch()

    if key == ord(' '):
        key_pressed = 0

    if key == curses.KEY_UP:
        key_pressed = 1

    if key == curses.KEY_DOWN:
        key_pressed = 2
        
    if key == curses.KEY_LEFT:
        key_pressed = 3
        
    if key == curses.KEY_RIGHT:
        key_pressed = 4

    if key == ord('x'):
        key_pressed = 5

    if key == ord('c'):
        key_pressed = 6

    handle_key_press()
    stdscr.refresh()

curses.endwin()
