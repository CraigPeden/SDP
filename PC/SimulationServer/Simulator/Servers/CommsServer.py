""" Simulates the strategy -> robot communications """
import struct
import socket
from multiprocessing import Process
import pygame
import math

# Constants
CMD_MOVE_LEFT = 0
CMD_MOVE_RIGHT = 1
CMD_ROTATION = 2
CMD_KICK = 3

SPEED_MULTIPLIER = 0.5

class CommsServer:
    """ Takes commands and runs them in the simulation """
    def __init__(self, tryPort=6789, host=''):
        self._serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = int(tryPort)
        self.left_speed = 0
        self.right_speed = 0
        gotSocket = False
        # Keep trying to get sockets until we find one that is unused
        while not gotSocket:
            try:
                self._serverSocket.bind((host, port))
                gotSocket = True
            except socket.error:
                port += 1
        self._port = port
        self.__clock = pygame.time.Clock()

    def handle_request(self, (cmd, args)):
        print "Cmd:", cmd
        print "Arg:", args
        #self.simulation.kick()
        # self.simulation.move(50, 50)
        # self.simulation.turn(math.pi)
        # self.simulation.move(50, 50
        
        """ Given a command and some arguments to that command, perform it """

        if cmd == CMD_MOVE_LEFT:
            right_speed= self.right_speed

            if args == 7 or args == 8:
                self.left_speed = 0
                self.simulation.move(0, right_speed)
            else:
                if args > 7:
                    args = 15 - args
                    speed = 100 - ((args *100) / 7)
                    speed *= SPEED_MULTIPLIER

                    self.left_speed = speed
                    self.simulation.move(speed, right_speed)
                else:
                    speed = 100 - ((args *100) / 7)
                    speed *= SPEED_MULTIPLIER

                    self.left_speed = -speed
                    self.simulation.move(- speed, right_speed)

        if cmd == CMD_MOVE_RIGHT:
            left_speed= self.left_speed
            if args == 7 or args == 8:
                self.right_speed = 0
                self.simulation.move(left_speed, 0)
            else:
                if args > 7:
                    args = 15 - args
                    speed = 100 - ((args *100) / 7)
                    speed *= SPEED_MULTIPLIER

                    self.right_speed = -speed
                    self.simulation.move(left_speed, -speed)
                else:
                    speed = 100 - ((args *100) / 7)
                    speed *= SPEED_MULTIPLIER
                    
                    self.right_speed = speed
                    self.simulation.move(left_speed,  speed)

        #(c,) = struct.unpack("b", cmd
        #print c
        # if c == CMD_MOVE:
        #     (l, r) = struct.unpack('bb', args[:2])
        #     self.simulation.move(l, r)
        # elif c == CMD_KICK:
        #     self.simulation.kick()
        # elif c == CMD_TURN:
        #     (angle1,angle2) = struct.unpack('BB', args[:2])
        #     angle = angle2+(angle1<<8)
        #     self.simulation.turn(angle)
        # elif c == CMD_STOP:
        #     self.simulation.stop()
        # elif c == CMD_EXIT:
        #     self.simulation.done.value = True
        self.__clock.tick(30)

    def waitForClient(self):
        """ Listen until a client connects """
        print "COMMS: Listening for client on %d" % self._port
        self._serverSocket.listen(2)
        (self._clientSocket, (self._clientAddr, _)) = self._serverSocket.accept()
        print "COMMS: Got client from %s"%self._clientAddr

    def run(self, simulation):
        """ Take commands from a client until that client disconnects """
        self.simulation = simulation
        while not simulation.done.value:
            data = self.getData()
            self.handle_request(data)
        print "COMMS.run: Simulation done"

    def getData(self):
        """ Get a command out of the socket """
        try:
            msg = ord(self._clientSocket.recv(1))

            if ((msg >> 7) & 1) != 1:
                print "COMMS: Signature not recognised."
                return None

            if ((msg >> 6) & 1) != countSetBits((msg & 0b00111111)) % 2:
                print "COMMS: Checksum failed."
                return None

            return ((msg & 0b00110000) >> 4, msg & 0b00001111)
        except socket.timeout as (str, _):
            print "COMMS: Socket timed out:\n%s"%str
        except socket.error as (str, _):
            print "COMMS: Client disconnected:\n%s"%str
        except AssertionError, e:
            print "COMMS: Assertion failed, client probably disconnected:\n%s"%e
            return None

class CommsServerFactory:
    """ Create a comms server subprocess """
    def __init__(self, simulation):
        self.simulation = simulation

    def start(self, port=6789):
        """ Spawn the subprocess that will take commands """
        self._subp = Process(target=self._start_server, args=(self.simulation, port))
        self._subp.start()

    def _start_server(self, simulation, port):
        """ The subprocess that will run """
        print "COMMS: Subprocess started"
        server = CommsServer(tryPort=port)
        while not simulation.done.value:
            try:
                server.waitForClient()
                server.run(simulation)
            except KeyboardInterrupt:
                print "COMMS: User closed"
            # except:
            #    print "COMMS: Client disconnecteda"

    def stop_server(self):
        """ Cease serving """
        print "COMMS: Terminating"
        self._subp.terminate()

def countSetBits(n):
    count = 0
    while n > 0:
        count += n & 1
        n >>= 1

    return count