import socket , select , string
import cv2
from struct import pack
from struct import unpack
from PIL import ImageTk, Image , ImageFile
from io import BytesIO
import threading as Thread
import time

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
        # Generating a standard flag which defines data is video or audio
        print("send image" , len(image_data))
        video_flag = "v"
        video_flag_bytes = bytes(video_flag, 'utf-8')
        length = pack('>Q', len(image_data) + 1)
        # sendall to make sure it blocks if there's back-pressure on the socket
        self.socket.sendall(length)
        self.socket.sendall(image_data + video_flag_bytes)
    
    def send_audio(self,audio):
        # Generating a standard flag which defines data is video or audio
        print("send audio" , len(audio))
        audio_flag = "a"
        audio_flag_bytes = bytes(audio_flag, 'utf-8')
        length = pack('>Q', len(audio) + 1)
        print("audio length" , len(length))
        print("audio flag" , len(audio_flag_bytes))
        # sendall to make sure it blocks if there's back-pressure on the socket
        self.socket.sendall(length)
        self.socket.sendall(audio + audio_flag_bytes)
        

    def disconnect(self):
        # use struct to make sure we have a consistent endianness on the length
        # length = pack('>Q', len(image_data))
        pass

    def close(self):
        self.socket.close()
        self.socket = None
    def show_image(self,data):
        # title of the application
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
        data_length = length - 2
        while len(data) < data_length:
            # print("while receiving")
            # doing it in batches is generally better than trying
            # to do it all in one go, so I believe.
            to_read = data_length - len(data)
            data += self.socket.recv(4096 if to_read > 4096 else to_read)
        data_type = self.socket.recv(1)
        reserved_chair = self.socket.recv(1)
        d = data_type.decode('utf-8')
        r = reserved_chair.decode('utf-8')
        return data ,str(d), int(r)
        # callback(data,int(r))
            
def main(callback=None):
    # print("client")
    nw = Client()
    reserved_chair = nw.connect()
    return nw , reserved_chair
