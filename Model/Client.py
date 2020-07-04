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
        # self.socket.connect((socket.gethostname(), self.port))
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

    def Receiving(self,user_image_data,callback=None):
        print("baaaaaleeee")
        client_number = 2
        reserved_chair = None
        your_ui_updated = False
        while True:
            print("came again")
            bs = self.socket.recv(8)
            print(len(bs))
            if len(bs) > 0:
                try:
                    print("length:",len(bs))
                    reserved_chair = bs.decode("utf-8")
                    if int(reserved_chair):
                        if your_ui_updated == False:
                            print("your chair reserved",reserved_chair)
                            callback(user_image_data,int(reserved_chair))
                            your_ui_updated = True 
                        # else:
                        #     print("client reserved",reserved_chair)
                        #     callback(data,int(reserved_chair))
                except:
                    if len(bs) >= 8:
                        print("is bigger than 8")
                        # (length,) = unpack('>Q', bs)
                        (length,) = unpack('>Q', bs)
                        data = b''
                        data_length = length - 1
                        while len(data) < length - 1:
                            print("while receiving")
                            # doing it in batches is generally better than trying
                            # to do it all in one go, so I believe.
                            to_read = data_length - len(data)
                            data += self.socket.recv(4096 if to_read > 4096 else to_read)
                            print("received till" , len(data) , length)
                        print("reserved chait is receiving")
                        reserved_chair = self.socket.recv(1)
                        print(reserved_chair)
                        len(reserved_chair.decode('utf-8'))
                        r = reserved_chair.decode('utf-8')
                        print(reserved_chair)
                        callback(data,int(r))
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
    nw.Receiving(image_data,callback)
    # nw.Receiving(callback)

def main1(image_data,callback=None):
    print("client")
    nw = Client()
    nw.connect()
    nw.send_image(image_data)
    nw.Receiving(image_data,callback)
# if __name__ == '__main__':
    
    # nw.close()
    
    