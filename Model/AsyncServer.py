import socket
import os
from struct import unpack
from struct import pack
from PIL import Image,ImageFile
import time
import asyncio
from queue import Queue,Empty

loop = asyncio.get_event_loop()
class Server:

    def __init__(self,port,serverType):
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
        self.run()

    def run(self):
            self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            self.socket.bind(('', self.port))
            # self.socket.bind((socket.gethostname(), self.port))
            print("Server is starting...", self.port)
            self.socket.setblocking(False)
            loop.create_task(self.handle_clients())
    # listen to new connections
    async def handle_clients(self):
        chair_No = None
        # try:
        connected = True
        while connected:
            #
            self.socket.listen(5)
            #
            # when new connection is received, establish a new thread
            (connection, addr) = await loop.sock_accept(self.socket)
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
            new_thread = Client(connection,addr[0],addr[1],chair_No,self,self.serverType)
            loop.create_task(new_thread.run())
            loop.create_task(new_thread.broadcast())
            print(f"new connection has established {addr}")
            self.threads.append(new_thread)
            # self.connections[key] = chair_No
            print("chair No" , chair_No)
            print("available chair",self.available_chair)
        for t in self.threads:
            t.join()
        # finally:
            # self.close()
            # pass
    


class Client:
    def __init__(self,connection,ip,port,reserved_chair,server,serverType=None ):
        self.ip = ip
        self.port = port
        self.connection = connection
        self.output_dir = '.'
        self.data = b''
        self.reserved_chair = reserved_chair
        self.chairNo_length = 1
        self.server = server
        self.serverType = serverType
        self.queue = asyncio.Queue()
    async def run(self):
        try:
            if self.serverType == "Video":
                print("send reserved chair" , self.reserved_chair)
                self.connection.sendall(str(self.reserved_chair).encode("utf-8"))
            while True:
                try:
                    bs = await loop.sock_recv(self.connection , 8)
                    (length,) = unpack('>Q', bs)
                    data = b''
                    # print("length is" , length)
                    while len(data) < length:
                        # doing it in batches is generally better than trying
                        # to do it all in one go, so I believe.
                        to_read = length - len(data)
                        data += await loop.sock_recv(self.connection , 4096 if to_read > 4096 else to_read)
                    print(len(data) , self.port)
                    if len(self.server.threads) > 1:
                        loop.call_soon_threadsafe(self.queue.put_nowait,data)
                except:
                    continue
        finally:
            pass
    async def broadcast(self):
        while True:
            # print("broad")
            data = await self.queue.get()
            for client in self.server.threads:
                if client.port != self.port:
                    # try:
                    if self.serverType == "Video":
                        print("video sent")
                        length = pack('>Q', len(data) + self.chairNo_length)
                        await loop.sock_sendall(client.connection , length)
                        r = bytes(str(self.reserved_chair), 'utf-8')
                        print("broadcast" , len(data))
                        await loop.sock_sendall(client.connection , data + r)
                    elif self.serverType == "Audio":
                        r = bytes(str(self.reserved_chair), 'utf-8')
                        await loop.sock_sendall(client.connection , data)
            
if __name__ == '__main__':
    # sp = Server()
    # sp.binding(sp.video_port)
    # sp.binding(sp.audio_port)
    video_port = 12345
    audio_port = 12346
    server_V = Server(video_port,"Video")
    # server_A = ServerAudio.Server_Audio(audio_port,"Audio")
    server_A = Server(audio_port,"Audio")
    loop.run_forever()
    # server_V.run()
    # server_A.broadcast()
    # server_A.run()
    # sp.handle_clients()

