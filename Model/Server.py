
import socket
import os
from struct import unpack
from struct import pack
from threading import Thread
from PIL import Image,ImageFile
from io import BytesIO
import time

class Server:
    def __init__(self):
        self.socket = None
        self.output_dir = '.'
        self.file_num = 1
        self.threads = []
        self.header = 8
        self.port = 12345
        self.available_chair = 1
        self.disconnect_message = "!Disconnect"

    def binding(self):
        # "192.168.1.111"
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        # socket.gethostname()
        self.socket.bind(('', self.port))
        # self.socket.bind((socket.gethostname(), self.port))
        print("Server is starting...", self.port)
        # self.socket.listen(5)

    # listen to new connections
    def handle_clients(self):
        try:
            connected = True
            while connected:
                #
                self.socket.listen(5)
                #
                # when new connection is received, establish a new thread
                (connection, addr) = self.socket.accept()
                ###
                print(self.available_chair)
                new_thread = self.Client_Thread(connection,addr[0],addr[1],self.available_chair)
                self.available_chair += 1
                new_thread.start() 
                print(f"new connection has established {addr}")
                self.threads.append(new_thread)
                # print(len(self.threads))
            for t in self.threads:
                t.join()
        finally:
            # print("finally")
            self.close()
    # broadcasting new client's data to other clients
    def broadcast(self,new_client):
        for client in self.threads:
            if client.port != new_client.port:
                # try:
                length = pack('>Q', len(new_client.data))
                print("sent to client")
                client.connection.sendall(length)
                client.connection.sendall(new_client.data)
                client.connection.sendall(str(new_client.reserved_chair).encode("utf-8"))
                self.sending_data_to_new_client(new_client,client)
                # except:
                #     client.connection.close()
                #     self.remove(client)
    # Sending other client's data to new client
    def sending_data_to_new_client(self,new_client,other_client):
        length = pack('>Q', len(other_client.data))
        print("sent to new_client")
        new_client.connection.sendall(length)
        new_client.connection.sendall(other_client.data)
        new_client.connection.sendall(str(other_client.reserved_chair).encode("utf-8"))
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
        def __init__(self,connection,ip,port,reserved_chair):
            Thread.__init__(self)
            self.ip = ip
            self.port = port
            self.connection = connection
            self.output_dir = '.'
            self.file_num = 1
            self.data = b''
            self.reserved_chair = reserved_chair
        def run(self):
            try:
                self.connection.sendall(str(self.reserved_chair).encode("utf-8"))
                bs = self.connection.recv(8)
                (length,) = unpack('>Q', bs)
                while len(self.data) < length:
                    # doing it in batches is generally better than trying
                    # to do it all in one go, so I believe.
                    to_read = length - len(self.data)
                    self.data += self.connection.recv(
                    4096 if to_read > 4096 else to_read)
                # send our 0 ack
                # assert len(b'\00') == 1
                # self.connection.sendall(b'\00')

                # broadcast the image recieved from new client
                sp.broadcast(self)
            finally:
                # connection.shutdown(SHUT_WR)
                # self.connection.close()
                # print("tamam")
                pass
            # with open(os.path.join(self.output_dir, f"{self.file_num}.jpg"), 'wb') as fp:
            #     fp.write(data)
            self.file_num += 1
            


if __name__ == '__main__':
    sp = Server()
    sp.binding()
    sp.handle_clients()



