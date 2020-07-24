import socket , select , string
import cv2
from struct import pack
from struct import unpack
from PIL import ImageTk, Image , ImageFile
from io import BytesIO
import threading as Thread

Image.LOAD_TRUNCATED_IMAGES = True
class Client:
    def __init__(self):
        self.socket = None
        self.header = 8
        self.port = 12345
        self.user_reserved_chair = None
    def connect(self):
        # "192.168.1.111"
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        # socket.gethostname()
        self.socket.connect(("45.79.78.220", self.port))
        # self.socket.connect((socket.gethostname(), self.port))
        bs = self.socket.recv(8)
        reserved_chair = bs.decode("utf-8")
        self.user_reserved_chair = reserved_chair
        return reserved_chair
    
    def send_image(self,image_data):
        length = pack('>Q', len(image_data))
        # sendall to make sure it blocks if there's back-pressure on the socket
        self.socket.sendall(length)
        self.socket.sendall(image_data)
        

    def disconnect(self):
        # use struct to make sure we have a consistent endianness on the length
        # length = pack('>Q', len(image_data))
        pass

    def close(self):
        self.socket.close()
        self.socket = None
    def show_image(self,data):
        # title of the application
        # print("received")
        stream = BytesIO(data)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        image = Image.open(stream).convert("RGBA")
        stream.close()
        image.show()
        # self.navigate_to_homepage()
    def receive_message(self):
        print('wait for broadcast')
        data = b''
        bs = self.socket.recv(8)
        (length,) = unpack('>Q', bs)
        data_length = length - 1
        while len(data) < length - 1:
            # print("while receiving")
            # doing it in batches is generally better than trying
            # to do it all in one go, so I believe.
            to_read = data_length - len(data)
            data += self.socket.recv(4096 if to_read > 4096 else to_read)
            # print("received till" , len(data) , length)
        reserved_chair = self.socket.recv(1)
        r = reserved_chair.decode('utf-8')
        return data , int(r)
        # callback(data,int(r))
            
def main(callback=None):
    # print("client")
    nw = Client()
    reserved_chair = nw.connect()
    return nw , reserved_chair
