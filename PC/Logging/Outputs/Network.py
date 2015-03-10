import socket
import struct

from Output import Output

class Network(Output):
    def __init__(self, host='',port=16180, formatString=None):
        super(Network, self).__init__(formatString)
        self.port = port
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def write(self, tag, message):
        tagLength = struct.pack('B', len(tag))
        sendString = "%c%s%s\r\n" % (tagLength, tag, message)
        self.socket.send(sendString)

    def close(self):
        self.socket.close()
