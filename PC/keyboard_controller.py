import arduinoComm
import time
import curses


# Initializing the screen
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

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

# Starts listening for input
key = ''
while key != ord('q') and key != ord('Q'):
    key = stdscr.getch()

    if key == curses.KEY_UP: 
        stdscr.addstr(10, 9, "UP       ")
        comms.drive(7,7)

    if key == curses.KEY_DOWN: 
        stdscr.addstr(10, 9, "DOWN     ")
        comms.drive(7,7, False, False)
        
    if key == curses.KEY_LEFT: 
        stdscr.addstr(10, 9, "LEFT     ")
        comms.drive(7, 7, False, True)
        
    if key == curses.KEY_RIGHT:
        stdscr.addstr(10, 9, "RIGHT    ")
        comms.drive(7, 7, True, False)

    if key == ord(' '):
        stdscr.addstr(10, 9, "SPACE    ")
        comms.drive(0,0)

    if key == ord('x'):
        stdscr.addstr(10, 9, "GRAB     ")
        comms.grab()

    if key == ord('c'):
        stdscr.addstr(10, 9, "KICK     ")
        comms.kick()

    stdscr.refresh()

curses.endwin()
