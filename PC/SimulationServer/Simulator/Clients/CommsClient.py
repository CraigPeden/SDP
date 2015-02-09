import socket
import array
from math import degrees
import multiprocessing


class CommsClient:
    def __init__(self, host=None, port=None):
        self.__HOST = host if not host == None else socket.gethostname()
        self.__PORT = port if not port == None else 6789
        self.__MOVE = 1
        self.__KICK = 2
        self.__TURN = 3
        self.__STOP = 4
        self.__TRAVEL = 5
        self.__ARC = 6
        self.__ARC_SCORE = 7
        self.__RESET = 98
        self.__EXIT = 99

        self.__BUMPER_NOT_TOUCHED = '\x01' # check these later
        self.__BUMPER_TOUCHED = '\x02'

        self.__bumperTouched = multiprocessing.Value('B', False)

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        p = self.__PORT
        while not connected:
            try:
                self.__socket.connect((self.__HOST, self.__PORT))
                connected = True
            except socket.error as (no, str):
                self.__PORT += 1
                if self.__PORT-p > 20:
                    raise

        listenerThread = multiprocessing.Process(target=self.receiver, args=())
        listenerThread.start()


    def receiver(self):
        while(True):
            try:
                data = self.__socket.recv(1) # stream of single bytes
                print 'Received : ', repr(data)
                if (data == self.__BUMPER_NOT_TOUCHED):
                    self.__bumperTouched.value = False
                    # print 'Bumper not touched!'

                elif (data == self.__BUMPER_TOUCHED):
                    self.__bumperTouched.value = True
                    # print 'Bumper touched!'

            except socket.error as (no, str):
                print 'ERROR: Could not receive Bluetooth status'

    def isBumperTouched(self):
        return self.__bumperTouched.value

    def forwards(self, motor_speed = 40):
        #print "Going forwards"
        self.move(motor_speed, motor_speed)

    def backwards(self, motor_speed = 20):
        #print "Going backwards"
        motor_speed = -motor_speed
        self.move(motor_speed, motor_speed)

    def stop(self):
        #print "Stopping"
        command = array.array('b', [self.__STOP, 0, 0, 0, 0])
        self.__socket.send(command)

    def move(self, left, right):
        #print "Moving"
        command = array.array('b', [self.__MOVE, left, right, 0, 0])
        self.__socket.send(command)

    def turn(self, angle, radians=True):
        # print "Turning by %f"%angle
        angle = int(degrees(angle)) if radians else int(angle)
        command = array.array('B', [self.__TURN, (angle>>8)&255, 
            (angle)&255, 0, 0])
        self.__socket.send(command)

    def kick(self):
        #print "Kicking"
        command = array.array('b', [self.__KICK, 0, 0, 0, 0])
        self.__socket.send(command)

    def reset(self):
        #print "Resetting"
        command = array.array('b', [self.__RESET, 0, 0, 0, 0])
        self.__socket.send(command)

    def travel(self, speed, distance):
        print "Travelling"
        distance = int(distance)
        command = array.array('B', [self.__TRAVEL, speed, (distance>>8)&255, 
            (distance)&255, 0])
        self.__socket.send(command)

    def arc(self, speedL, speedR, rotations):
        print "Arc-ing"
        command = array.array('b', [self.__ARC, speedL, speedR, rotations, 0])
        self.__socket.send(command)

    def arcScore(self, radius, angle, abstract = True, radians=True):
        print "Arc-ing Score"
        #print "Turning by %f"%angle
        angle = int(degrees(angle)) if radians else int(angle)
        radius = int(abst2cm(radius)) if abstract else int(radius)
        command = array.array('B', [self.__ARC_SCORE, (radius>>8)&255, 
            (radius)&255, (angle>>8)&255, (angle)&255])
        self.__socket.send(command)

    def exit(self):
        #print "Exiting"
        command = array.array('b', [self.__EXIT, 0, 0, 0, 0])
        self.__socket.send(command)
