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
stdscr.addstr(5,0,"BACKSPACE  : stop")
stdscr.addstr(10,9,"         ")
stdscr.refresh()

# Starts listening for input
key = ''
while key != ord('q') and key != ord('Q'):
    key = stdscr.getch()
    #stdscr.addstr(10, 9, "     ")

    try:
        key_pressed = [False]*4

        if key == curses.KEY_UP: 
            stdscr.addstr(10, 9, "UP       ")
            comms.drive(7,7)

        if key == curses.KEY_DOWN: 
            stdscr.addstr(10, 9, "DOWN     ")
            comms.drive(7,7, False, False)
            
        if key == curses.KEY_LEFT: 
            stdscr.addstr(10, 9, "LEFT     ")
            comms.drive(3, 3, False, True)
            
        if key == curses.KEY_RIGHT: 
            stdscr.addstr(10, 9, "RIGHT    ")
            comms.drive(3, 3, True, False)

        if key == curses.KEY_BACKSPACE:
            stdscr.addstr(10, 9, "BACKSPACE")
            comms.drive(0,0)

        stdscr.refresh()

    except:
        pass

curses.endwin()
