import socket
import multiprocessing


class simulatorClient:
    def __init__(self, port=6789, host='127.0.0.1'):
        self.__PORT = port
        self.__HOST = host

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        connected = False
        p = self.__PORT
        while not connected:
            try:
                self.__socket.connect((self.__HOST, self.__PORT))
                print 'Connected'
                connected = True
            except socket.error as (no, str):
                print 'Error!'
                self.__PORT += 1
                if self.__PORT - p > 20:
                    raise

        #listenerThread = multiprocessing.Process(target=self.receiver, args=())
        #listenerThread.start()


    def write(self, msg):
        self.__socket.send(msg)

    def receiver(self):
        while (True):
            try:
                data = self.__socket.recv(1)  # stream of single bytes
                print 'Received : ', repr(data)
                
            except:
                pass
