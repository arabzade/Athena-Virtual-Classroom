
import socket
import os
from struct import unpack
from struct import pack
from threading import Thread
from PIL import Image,ImageFile
# from io import BytesIO
import time
# import ServerAudio

class Server_Thread(Thread):
    def __init__(self,port,serverType):
        Thread.__init__(self)
        self.socket = None
        self.output_dir = '.'
        self.file_num = 1
        self.threads = []
        # self.connections = {}
        self.header = 8
        self.port = port
        self.available_chair = 1
        self.disconnect_message = "!Disconnect"
        self.serverType = serverType

    def run(self):
        # "192.168.1.111"
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.socket.bind(('', self.port))
        # self.socket.bind((socket.gethostname(), self.port))
        print("Server is starting...", self.port)
        # self.socket.listen(5)
        self.handle_clients()

    # listen to new connections
    def handle_clients(self):
        chair_No = None
        try:
            connected = True
            while connected:
                #
                self.socket.listen(5)
                #
                # when new connection is received, establish a new thread
                (connection, addr) = self.socket.accept()
                key = addr[0]
                ############
                ### check with different computers
                # if len(self.connections) != 0:
                #     if key in self.connections:
                #         chair_No = self.connections[key]
                #     else:
                #         chair_No = self.available_chair
                #         self.available_chair += 1
                #         new_thread = Client_Thread(connection,addr[0],addr[1],chair_No)
                #         new_thread.start() 
                #         print(f"new connection has established {addr}")
                #         self.threads.append(new_thread)
                #         self.connections[key] = chair_No
                # else:
                ##################
                chair_No = self.available_chair
                self.available_chair += 1
                new_thread = Client_Thread(connection,addr[0],addr[1],chair_No,self,self.serverType)
                new_thread.start() 
                print(f"new connection has established {addr}")
                self.threads.append(new_thread)
                # self.connections[key] = chair_No
                print("chair No" , chair_No)
                print("available chair",self.available_chair)
                
                # print(len(self.threads))
            for t in self.threads:
                t.join()
        finally:
            # print("finally")
            self.close()
    # # Sending other client's data to new client
    def sending_data_to_new_client(self,new_client,other_client):
        length = pack('>Q', len(other_client.data) + 1)
        r = bytes(str(other_client.reserved_chair), 'utf-8')
        new_client.connection.sendall(length)
        new_client.connection.sendall(other_client.data + r)
        # time.sleep(2)
        # r = bytes(str(other_client.reserved_chair), 'utf-8')
        # new_client.connection.send(r)
    # remove disconnected client from thread       
    def remove(self,connection): 
        if connection in self.threads: 
            self.threads.remove(connection) 
    # close the socket 
    def close(self):
        self.socket.close()
        self.socket = None

    ###########################
    # Multi-thread Connection
    ###########################
class Client_Thread(Thread):
    def __init__(self,connection,ip,port,reserved_chair,server,serverType=None):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.connection = connection
        self.output_dir = '.'
        self.file_num = 1
        self.data = b''
        self.reserved_chair = reserved_chair
        self.chairNo_length = 1
        self.server = server
        self.serverType = serverType
    def run(self):
        try:
            if self.serverType == "Video":
                print("send reserved chair" , self.reserved_chair)
                self.connection.sendall(str(self.reserved_chair).encode("utf-8"))
            while True:
                bs = self.connection.recv(8)
                (length,) = unpack('>Q', bs)
                data = b''
                # print(len(self.data))
                # print("received data" , length)
                # print(self.ip , self.port, "total length" , length)
                while len(data) < length:
                    # doing it in batches is generally better than trying
                    # to do it all in one go, so I believe.
                    to_read = length - len(data)
                    data += self.connection.recv(
                    4096 if to_read > 4096 else to_read)
                self.broadcast(data)
            # send our 0 ack
            # assert len(b'\00') == 1
            # self.connection.sendall(b'\00')

            # broadcast the image recieved from new client
        finally:
            # connection.shutdown(SHUT_WR)
            # self.connection.close()
            # print("tamam")
            pass
        # with open(os.path.join(self.output_dir, f"{self.file_num}.jpg"), 'wb') as fp:
        #     fp.write(data)
        self.file_num += 1
    def broadcast(self,data):
        # time.sleep(2)
        # print("#threads" , len(self.server.threads))
        for client in self.server.threads:
            if client.port != self.port and client.ip != self.ip:
                # try:
                if self.serverType == "Video":
                    print("video sent")
                    length = pack('>Q', len(data) + self.chairNo_length)
                    client.connection.sendall(length)
                    r = bytes(str(self.reserved_chair), 'utf-8')
                    client.connection.sendall(data + r)
                elif self.serverType == "Audio":
                    print("audio sent")
                    # length = pack('>Q', len(data))
                    # client.connection.sendall(length)
                    # length = b''
                    r = bytes(str(self.reserved_chair), 'utf-8')
                    print("broadcast" , len(data))
                    client.connection.sendall(data)
                    # data = b''
                    # print(self.reserved_chair , len(r))
                    # time.sleep(2)
                # r = bytes(str(new_client.reserved_chair), 'utf-8')
                # client.connection.send(r)
                # self.sending_data_to_new_client(new_client,client)
                # except:
                #     client.connection.close()
                #     self.remove(client)
    # Sending other client's data to new client
            


if __name__ == '__main__':
    # sp = Server()
    # sp.binding(sp.video_port)
    # sp.binding(sp.audio_port)
    video_port = 12345
    audio_port = 12346
    server_V = Server_Thread(video_port,"Video")
    # server_A = ServerAudio.Server_Audio(audio_port,"Audio")
    server_A = Server_Thread(audio_port,"Audio")

    server_V.start()
    # server_A.broadcast()
    server_A.start()
    # sp.handle_clients()



