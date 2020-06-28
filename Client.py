import socket , select , string
import os
import sys
from struct import pack
from struct import unpack
import cv2


class Client:
    def __init__(self):
        self.socket = None
        self.header = 8
        self.port = 1234
    def connect(self):
        # "192.168.1.111"
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.socket.connect(( socket.gethostname(), self.port))
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
                # Home.show_image(data,column)
                Home.main()
                column += 1
def callback(imageFileName):
        print(imageFileName)
        # with open(imageFileName, 'rb') as fp:
        #     image_data = fp.read()
        # assert(len(image_data))
        # nw.send_image(image_data)
def take_shot_from_webcam(callback = None):
    cap = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        img_counter = 0
        try:
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            cv2.imshow('Input', frame)

            c = cv2.waitKey(1)
            if c == 27:
                break
            elif c == 32:
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                if callback:
                    callback(img_name)
                    break
                img_counter += 1
        except:
            print("no access")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # nw = Client()
    # image_data = None
    # nw.connect()
    # imageFileName = "Unknown.png"
    
    take_shot_from_webcam(callback)
    # pass
    
    # nw.Receiving()
    # nw.close()
    
    