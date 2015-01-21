import arduinoComm
"""
initializing the object which will handle communications
"""
comms = Communication()
print("Press q to quit")
print("Press 1 to start left motor")
print("Press 2 to stop left motor")
print("Press 3 to start right motor")
print("Press 4 to stop right motor")
print("Press 5 to activate left rotational motor")
print("Press 6 to activate right rotational motor")
"""
starts listening for input
"""
input = ''
while input!='q':
	input=raw_input()
	if input == '1':
		start_left_power_motor(comms)
	elif input == '2':
		stop_left_power_motor(comms)
	if input == '3':
		start_right_power_motor(comms)
	elif input == '4':
		stop_right_power_motor(comms)
	elif input == '5':
		activate_left_rotational_motor(comms, 30)
	elif input == '6':
		activate_right_rotational_motor(comms, 30)
"""
methods which map the keybord input to the methods of the communications object
"""
def start_left_power_motor(comms):
	print 'Starting Left Power Motor:\n'
	comms.drive("left", 1)

def stop_left_power_motor(comms):
	print 'Stopping Left Power Motor:\n'
	comms.drive("left", 0)

def start_right_power_motor(comms):
	print 'Starting Right Power Motor:\n'
	comms.drive("right", 1)

def stop_right_power_motor(comms):
	print 'Stopping Right Power Motor:\n'
	comms.drive("right", 0)

def activate_left_rotational_motor(comms, degrees):
	print 'Rotate Left Rotational Motor:'+degrees
	comms.rotation("left", degrees)

def activate_right_rotational_motor(comms, degrees):
	print 'Rotate Right Rotational Motor:'+degrees
	comms.rotation("right", degrees)
