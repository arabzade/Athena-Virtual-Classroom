import socket , select , string
# import os
from struct import pack
from struct import unpack
from PIL import ImageTk, Image , ImageFile
from io import BytesIO

Image.LOAD_TRUNCATED_IMAGES = True
class Client:
    def __init__(self):
        self.socket = None
        self.header = 8
        self.port = 12345
    def connect(self):
        # "192.168.1.111"
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        # socket.gethostname()
        self.socket.connect(("45.79.78.220", self.port))
        print("connected")
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

    def Receiving(self,callback=None):
        print("baaaaaleeee")
        client_number = 2
        while True:
            bs = self.socket.recv(8)
            print("length:",len(bs))
            if len(bs) >= 8:
                print("is bigger than 8")
                (length,) = unpack('>Q', bs)
                data = b''
                # print(column)
                print("other client files received")
                while len(data) < length:
                    print("while receiving")
                    # doing it in batches is generally better than trying
                    # to do it all in one go, so I believe.
                    to_read = length - len(data)
                    data += self.socket.recv(4096 if to_read > 4096 else to_read)
                    print("received till" , len(data) , length)
                callback(data,client_number)
                client_number += 1
                # Home.show_image(data,column)
                
    def show_image(self,data):
        # title of the application
        print("received")
        stream = BytesIO(data)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        image = Image.open(stream).convert("RGBA")
        stream.close()
        image.show()
        # self.navigate_to_homepage()
    
def main(image_data,callback=None):
    print("client")
    nw = Client()
    nw.connect()
    nw.send_image(image_data)
    nw.Receiving(callback)
# if __name__ == '__main__':
    
    # nw.close()
    
    