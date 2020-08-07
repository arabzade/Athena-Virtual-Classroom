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
        self.video_socket = None
        self.audio_socket = None
        self.header = 8
        self.video_port = 12345
        self.audio_port = 12346
        self.user_reserved_chair = None
    def connect(self,video_port,audio_port):
        reserved_chair = None
        try:
            self.video_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            self.video_socket.connect(("45.79.78.220", self.video_port))
            # self.video_socket.connect((socket.gethostname(), video_port))
            bs = self.video_socket.recv(8)
            reserved_chair = bs.decode("utf-8")
            print(reserved_chair)
            self.user_reserved_chair = reserved_chair
        except:
            print("video connection is refused")
        try:
            self.audio_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            self.audio_socket.connect(("45.79.78.220", self.audio_port))
            # self.audio_socket.connect((socket.gethostname(), audio_port))
        except:
            print("audio connection is refused")
        return reserved_chair

        


    
    def send_image(self,image_data):
        # Generating a standard flag which defines data is video or audio
        ################
        # print("send image" , len(image_data))
        # video_flag = "v"
        # video_flag_bytes = bytes(video_flag, 'utf-8')
        length = pack('>Q', len(image_data))
        # sendall to make sure it blocks if there's back-pressure on the socket
        self.video_socket.sendall(length)
        self.video_socket.sendall(image_data)
    
    def send_audio(self,audio):
        # Generating a standard flag which defines data is video or audio
        # print("send audio" , len(audio))
        # audio_flag = "a"
        # audio_flag_bytes = bytes(audio_flag, 'utf-8')
        length = pack('>Q', len(audio))
        # print("audio length" , len(length))
        # print("audio flag" , len(audio_flag_bytes))
        # sendall to make sure it blocks if there's back-pressure on the socket
        self.audio_socket.sendall(length)
        self.audio_socket.sendall(audio)
        

    def disconnect(self):
        # use struct to make sure we have a consistent endianness on the length
        # length = pack('>Q', len(image_data))
        pass

    def close(self):
        self.video_socket.close()
        self.video_socket = None
    def show_image(self,data):
        # title of the application
        stream = BytesIO(data)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        image = Image.open(stream).convert("RGBA")
        stream.close()
        image.show()
        # self.navigate_to_homepage()
    def receive_image(self):
        # print('video broadcast')
        data = b''
        bs = self.video_socket.recv(8)
        (length,) = unpack('>Q', bs)
        # print("length is" ,  length)
        data_length = length - 1
        while len(data) < data_length:
            # print("while receiving")
            # doing it in batches is generally better than trying
            # to do it all in one go, so I believe.
            to_read = data_length - len(data)
            data += self.video_socket.recv(4096 if to_read > 4096 else to_read)
        reserved_chair = self.video_socket.recv(1)
        r = reserved_chair.decode('utf-8')
        return data ,int(r)
    def receive_audio(self):
        # print('audio broadcast')
        # bs = self.audio_socket.recv(8)
        # (length,) = unpack('>Q', bs)
        # print(length)
        # reserved_chair = self.audio_socket.recv(1)
        # r = reserved_chair.decode('utf-8')
        data_length = 2048
        # print(data_length)
        data = b''
        while len(data) < data_length:
            # print("while receiving")
            # doing it in batches is generally better than trying
            # to do it all in one go, so I believe.
            to_read = data_length - len(data)
            data += self.audio_socket.recv(2048 if to_read > 2048 else to_read)
        # reserved_chair = self.audio_socket.recv(1)
        # r = reserved_chair.decode('utf-8')
        return data
        # callback(data,int(r))
            
def main(callback=None):
    # print("client")
    nw = Client()
    reserved_chair = nw.connect(nw.video_port , nw.audio_port)
    return nw , reserved_chair
