import socket
import os
import sys
from struct import pack


# s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
# s.connect((socket.gethostname() , 1234))
# full_message = ""
# while True:
#     msg = s.recv(1024)
#     if len(msg) <= 0:
#         break
#     full_message += msg.decode("utf-8")
#     s.send(bytes("received", encoding="utf-8"))
# print(full_message)
    


class Client:
    def __init__(self):
        self.socket = None
    def connect(self):
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.socket.connect((socket.gethostname() , 1234))
        # self.open_image(image)
    
    def open_image(self,image):
        try:
            # open image
            myfile = open(os.path.join(sys.path[0], image), "rb")
            contents = myfile.read()
            size = len(contents)
            # self.send_image(size,contents)
            myfile.close()
        finally:
            self.socket.close()
    # def send_image(self,size,bytes):
    #     # send image size to server
    #     self.sock.sendall(bytes(f"SIZE {size} is" , encoding="utf-8"))
    #     answer = self.sock.recv(4096)
    #     print(f"answer is:  {answer}")
    #     if answer == 'GOT SIZE':
    #         self.sock.sendall(bytes)
    #         # check what server send
    #         answer = self.sock.recv(4096)
    #         print(f"answer is:  {answer}")

    #         if answer == 'GOT IMAGE' :
    #             self.sock.sendall("BYE BYE ")
    #             print("Image successfully send to server")
    def send_image(self, image_data):

        # use struct to make sure we have a consistent endianness on the length
        length = pack('>Q', len(image_data))

        # sendall to make sure it blocks if there's back-pressure on the socket
        self.socket.sendall(length)
        self.socket.sendall(image_data)

        ack = self.socket.recv(1)

        # could handle a bad ack here, but we'll assume it's fine.

    def close(self):
        self.socket.close()
        self.socket = None

    # def Receiving(self):
    #     full_message = ""
    #     while True:
    #         msg = s.recv(1024)
    #         if len(msg) <= 0:
    #             break
    #         full_message += msg.decode("utf-8")
    #     print(full_message)



if __name__ == '__main__':

    nw = Client()

    image_data = None
    with open('Minimizing.JPG', 'rb') as fp:
        image_data = fp.read()
    assert(len(image_data))
    nw.connect()
    nw.send_image(image_data)
    nw.close()
    
