import arduinoComm
import time

comms = arduinoComm.Communication("/dev/ttyACM0", 9600)

comms.drive(7,7)
time.sleep(1.8)
comms.drive(0,0)
