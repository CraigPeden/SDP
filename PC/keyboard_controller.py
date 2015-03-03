import arduinoComm
import time
import curses

# Initializing the object which will handle communications
comms = arduinoComm.Communication("/dev/ttyACM0", 9600)

# Initializing the screen
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

# Setup screen
stdscr.addstr(0,0,"Q          : quit")
stdscr.addstr(1,0,"UP         : go forwards")
stdscr.addstr(2,0,"DOWN       : go backwards")
stdscr.addstr(3,0,"LEFT       : steer left")
stdscr.addstr(4,0,"RIGHT      : steer right")
stdscr.addstr(5,0,"SPACE      : stop")
stdscr.addstr(6,0,"X          : grabberDown")
stdscr.addstr(7,0,"C          : grabberUp")
stdscr.addstr(8,0,"V          : kick")

stdscr.addstr(12,0,"         ")
stdscr.refresh()

# Starts listening for input
key = ''
while key != ord('q') and key != ord('Q'):
    key = stdscr.getch()

    if key == curses.KEY_UP: 
        stdscr.addstr(12, 0, "UP       ")
        comms.drive(7,7)

    if key == curses.KEY_DOWN: 
        stdscr.addstr(12, 0, "DOWN     ")
        comms.drive(-7,-7)
        
    if key == curses.KEY_LEFT: 
        stdscr.addstr(12, 0, "LEFT     ")
        comms.drive(-7, 7)
        
    if key == curses.KEY_RIGHT:
        stdscr.addstr(12, 0, "RIGHT    ")
        comms.drive(7, -7)

    if key == ord(' '):
        stdscr.addstr(12, 0, "SPACE    ")
        comms.drive(0,0)

    if key == ord('x'):
        stdscr.addstr(12, 0, "GRAB DOWN")
        comms.grabberDown()

    if key == ord('c'):
        stdscr.addstr(12, 0, "GRAB UP  ")
        comms.grabberUp()

    if key == ord('v'):
        stdscr.addstr(12, 0, "KICK     ")
        comms.kick()
        
    stdscr.refresh()

curses.endwin()
