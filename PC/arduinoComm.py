import serial
import time

ser = serial.Serial("/dev/ttyACM0", 115200)

while True:
	print ser.write("1")
	time.sleep(1)

	print ser.write("0")
	time.sleep(1)