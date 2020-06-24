import socket
import os
from struct import unpack
import AVC

# s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

# s.bind((socket.gethostname() , 1234))

# s.listen(5)

# while True:
#     clientsocket , address = s.accept()
#     print(f"connection from {address} has established")
#     # clientsocket.send(bytes("Message",).encode("utf-8"))
#     clientsocket.send(bytes("welcome to the server", encoding="utf-8"))
#     full_message = ""
#     while True:
#         msg = s.recv(1024)
#         if len(msg) <= 0:
#             break
#         full_message += msg.decode("utf-8")
#         print(full_message)
#     clientsocket.close()


class Server:
    def __init__(self):
        self.socket = None
        self.output_dir = '.'
        self.file_num = 1

    def listen(self):
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.socket.bind((socket.gethostname() , 1234))
        self.socket.listen(5)

    def handle_images(self):

        try:
            while True:
                (connection, addr) = self.socket.accept()
                try:
                    bs = connection.recv(8)
                    (length,) = unpack('>Q', bs)
                    data = b''
                    while len(data) < length:
                        # doing it in batches is generally better than trying
                        # to do it all in one go, so I believe.
                        to_read = length - len(data)
                        data += connection.recv(
                            4096 if to_read > 4096 else to_read)

                    # send our 0 ack
                    assert len(b'\00') == 1
                    connection.sendall(b'\00')
                finally:
                    # connection.shutdown(SHUT_WR)
                    connection.close()
                # AVC.Home_Page().show_image(data)
                with open(os.path.join(self.output_dir, f"{self.file_num}.jpg"), 'wb') as fp:
                    fp.write(data)

                self.file_num += 1
                AVC.Home_Page().show_image(f"{self.file_num}.jpg")
        finally:
            self.close()

    def close(self):
        self.socket.close()
        self.socket = None

        # could handle a bad ack here, but we'll assume it's fine.

if __name__ == '__main__':
    sp = Server()
    sp.listen()
    sp.handle_images()