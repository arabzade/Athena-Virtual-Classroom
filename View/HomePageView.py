import sys
from PyQt5.QtCore import Qt,QMargins
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget,QLabel , QMainWindow)
from PyQt5.QtGui import QPixmap,QImage
from PyQt5 import QtWidgets
import time
sys.path.insert(1, '../bodypix/client')
sys.path.insert(1, '../Audio')
sys.path.insert(1, '../Model')
sys.path.insert(1, '../')
import Client
import bodypix
import bodypix_node
import mic
import HomePageController
import threading as Thread
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5 import QtCore
from PIL import Image
import cv2
from queue import Queue,Empty
import enum
import pyaudio
import Config


class standard_letter(enum.Enum): 
    video = "v"
    audio = "a"

network_thread = None

client_socket = None
hw = None

player1 = mic.AudioRecorder()
def create_receive_thread(socket,window):
    # video receiving thread
    video_receiving_thread = ReceivingThread(socket)
    vrt = Thread.Thread(target=video_receiving_thread.video_process)
    # audio receiving thread
    audio_receiving_thread = ReceivingThread(socket)
    art = Thread.Thread(target=audio_receiving_thread.audio_process)
    # audio_receiving_thread.notify_audio.connect(play)
    video_receiving_thread.notify_video.connect(window.update_ui)
    vrt.start()
    art.start()
    
class Window(QMainWindow):
    def __init__(self, parent=None ):
        super(Window, self).__init__(parent)
        self.user_image_data = None
        widget = QWidget(self)
        grid = QGridLayout()
        self.img1 = self.Label()
        self.img2 = self.Label()
        self.img3 = self.Label()
        self.img4 = self.Label()
        self.img5 = self.Label()
        self.img6 = self.Label()
        self.img7 = self.Label()
        self.img8 = self.Label()
        self.img9 = self.Label()
        self.img1.updateImage("./Images/slide1.jpg")
        self.img2.updateImage("./Images/Professor.jpg")
        self.img3.updateImage("./Images/slide2.jpg")
        grid.addWidget(self.img1, 0, 0)
        grid.addWidget(self.img2, 0, 1)
        grid.addWidget(self.img3, 0, 2)
        grid.addWidget(self.img4, 1, 0)
        grid.addWidget(self.img5, 1, 1)
        grid.addWidget(self.img6, 1, 2)
        # grid.addWidget(self.img7, 2, 0)
        # grid.addWidget(self.img8, 2, 1)
        # grid.addWidget(self.img9, 2, 2)
        grid.setContentsMargins(QMargins(0,0,0,0))
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        widget.setLayout(grid)
        widget.setMouseTracking(True)
        widget.setWindowTitle("PyQt5 Group Box")
        self.setCentralWidget(widget)
        self.resize(Config.mainWindow_frames()[0], Config.mainWindow_frames()[1])
        self.setStyleSheet("QMainWindow {background-image: url(./images/background.png); background-size: 1056px 576px; }")
    def mouseMoveEvent(self,e):
        x = e.x()
        y = e.y()
        text = f'x: {x},  y: {y}'
        print(text)
    def pushButton_clicked(self):
        self.b1.updateImage()
    def notify(self,data,chair):
        print("notified")
    def update_ui(self,data,reserved_chair):
        if reserved_chair == 1:
            self.img4.updateImage(data)
        if reserved_chair == 2:
            self.img5.updateImage(data)
        elif reserved_chair == 3:
            self.img6.updateImage(data)
        elif reserved_chair == 4:
            self.img7.updateImage(data)
        elif reserved_chair == 5:
            self.img8.updateImage(data)
        elif reserved_chair == 6:
            self.img9.updateImage(data)
    # def play_audio(self,data,reserved_chair):
    #     audio_stream.play(data)
    class Label(QLabel):
        def __init__(self):
            super().__init__()
            self.userImage_w = Config.user_frame()[0]
            self.userImage_h = Config.user_frame()[1]
            self.initUI()
        @pyqtSlot(str)
        def updateImage(self,img):
            if isinstance(img,bytes):
                pixmap = QPixmap()
                pixmap.loadFromData(img)
                smaller_pixmap = pixmap.scaled(self.userImage_w, self.userImage_h, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.setPixmap(pixmap)
            elif isinstance(img,QImage):
                print("qimage")
                pixmap = QPixmap.fromImage(img)
                smaller_pixmap = pixmap.scaled(self.userImage_w, self.userImage_h, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.setPixmap(smaller_pixmap)
            else:
                print("no byte")
                pixmap = QPixmap(img)
                smaller_pixmap = pixmap.scaled(self.userImage_w, self.userImage_h, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.setPixmap(smaller_pixmap)
                
        def initUI(self):
            self.setScaledContents(True)
            pixmap = QPixmap()
            smaller_pixmap = pixmap.scaled(self.userImage_w, self.userImage_h, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.setPixmap(smaller_pixmap)
            # background = MyThread(self)
            # t = Thread.Thread(target=background.process)
            # background.changePixmap.connect(self.updateImage)
            # t.start()
# user interface thread
class UIThread(QtCore.QObject):  
    changePixmap = QtCore.pyqtSignal(bytes,int)
    def __init__(self,window, parent=None,rate=44100, fpb=4*1024, channels=1):
        super(UIThread, self).__init__(parent)
        self.window = window
        self.queue = Queue()
        self.client = None
        self.my_reserved_chair = None
        self.audio = mic.AudioRecorder(self.client)
    def process(self):
        active = True
        # connect to socket       
        self.connect_to_socket()
        #stream audio in different thread
        mic.main(self.client)
        # stream video in current thread
        fps = 0
        time1 = time.time()
        while active:
            try:
            # imageData,reserved_chair = self.queue.get()
                # print("send")
                # _ = bodypix.update_ui()
                _ = bodypix_node.update_ui()
                with open('../Model/output.png', 'rb') as fp:
                    image_data = fp.read()
                    # self.queue.put(image_data)
                    # self.user1_queue.put(image_data,1)
                    self.changePixmap.emit(image_data,int(self.my_reserved_chair))
                    self.client.send_image(image_data) 
                    # time.sleep(2)
                fps += 1
                if (time.time() - time1) > 1 :
                    print("fps is ",fps)
                    fps = 0 
                    time1 = time.time()
            except:
                continue
        ########################
    # def connect(self):
    #     self.connect_to_socket()
    #     # while self.should_continue:
    #     print("should countinue")
    #     while True:
    #         try:
    #             frame = self.queue.get()
    #             self.client.send_image(frame) 
    #         except:
    #             continue
    #         # if not self.queue.Empty:
    #         #     frame = self.queue.get()
    #         #     self.client.send_image(frame)
    #         # Here, do your server stuff.
    def connect_to_socket(self):
        print("socket is connecting")
        # connect to socket
        self.client,self.my_reserved_chair = Client.main()
        # create both audio and video threads
        create_receive_thread(self.client,self.window)



class ReceivingThread(QtCore.QObject):  
    notify_video = QtCore.pyqtSignal(bytes,int)
    notify_audio = QtCore.pyqtSignal(bytes)
    def __init__(self,client,parent=None):
        super(ReceivingThread, self).__init__(parent)
        self.client = client
    def notify(self,image_data,reserved_chair):
        # print("received image is notified")
        print("received",len(image_data))
        # self.notify_ui.emit(image_data,reserved_chair)
    # video receiving block
    def video_process(self):
        while True:
            try:
                data,reserved_chair = self.client.receive_image()
                self.notify_video.emit(data,reserved_chair)
            except:
                # print("video receiving exception")
                continue
    # audio receiving block
    def audio_process(self):
        print("audio process")
        while True:
            # print("start")
            data = self.client.receive_audio()
            # print("data",len(data))
            # self.notify_audio.emit(data)
            # if reserved_chair == 1:
            player1.play(data)
            # elif reserved_chair == 2:
            #     player2.play(data)
            # elif reserved_chair == 3:
            #     player3.play(data)
            

                


def main(callback=None):
    app = QApplication(sys.argv)
    hw = Window()
    print("shown")
    # app.quit()
    # time.sleep(2)
    # callback(hw)
    ui_thread = UIThread(hw)
    t = Thread.Thread(target=ui_thread.process)
    ui_thread.changePixmap.connect(hw.update_ui)
    t.start()
    hw.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
