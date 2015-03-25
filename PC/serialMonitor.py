import serial
import sys

ser = serial.Serial(sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0", 9600)

while True:
	if ser.inWaiting() > 0:
		sys.stdout.write(ser.read())