import socket , select , string
import os
import sys
from struct import pack
from struct import unpack
import Home


class Client:
    def __init__(self):
        self.socket = None
        self.header = 8
        self.port = 1234
    def connect(self):
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.socket.connect(("192.168.1.111" , self.port))
        # self.open_image(image)
    
    def send_image(self, image_data):

        # use struct to make sure we have a consistent endianness on the length
        length = pack('>Q', len(image_data))

        # sendall to make sure it blocks if there's back-pressure on the socket
        self.socket.sendall(length)
        self.socket.sendall(image_data)
    def disconnect(self):
        # use struct to make sure we have a consistent endianness on the length
        length = pack('>Q', len(image_data))

    def close(self):
        self.socket.close()
        self.socket = None

    def Receiving(self):
        column = 0
        while True:
            bs = self.socket.recv(8)
            if len(bs) >= 8:
                (length,) = unpack('>Q', bs)
                data = b''
                # print(column)
                print("other client files received")
                while len(data) < length:
                    # doing it in batches is generally better than trying
                    # to do it all in one go, so I believe.
                    to_read = length - len(data)
                    data += self.socket.recv(4096 if to_read > 4096 else to_read)
                Home.show_image(data,column)
                column += 1



if __name__ == '__main__':

    nw = Client()
    image_data = None
    nw.connect()
    imageFileName = "Figure_2.png"
    with open(imageFileName, 'rb') as fp:
        image_data = fp.read()
    assert(len(image_data))
    nw.send_image(image_data)
    nw.Receiving()
    # nw.close()
    
