import arduinoComm
import time

comms = arduinoComm.Communication("/dev/ttyACM0", 9600)

comms.drive(7, 7, False, False)
time.sleep(0.7)
comms.drive(0,0)
