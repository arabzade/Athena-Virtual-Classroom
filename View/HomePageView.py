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


class standard_letter(enum.Enum): 
    video = "v"
    audio = "a"

network_thread = None

client_socket = None
hw = None

audio_stream = mic.AudioRecorder()

def create_receive_thread(socket,window):
    receiving_thread = ReceivingThread(socket)
    rt = Thread.Thread(target=receiving_thread.process)
    receiving_thread.notify_video.connect(window.update_ui)
    receiving_thread.notify_audio.connect(window.play_audio)
    rt.start()
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
        grid.addWidget(self.img7, 2, 0)
        grid.addWidget(self.img8, 2, 1)
        grid.addWidget(self.img9, 2, 2)
        grid.setContentsMargins(QMargins(0,0,0,0))
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        widget.setLayout(grid)
        widget.setMouseTracking(True)
        widget.setWindowTitle("PyQt5 Group Box")
        self.setCentralWidget(widget)
        self.resize(960, 540)
        self.setStyleSheet("QMainWindow {background-image: url(./images/background.png); background-size: 960px 540px; }")
    def mouseMoveEvent(self,e):
        x = e.x()
        y = e.y()
        text = f'x: {x},  y: {y}'
        print(text)
    def pushButton_clicked(self):
        self.b1.updateImage()
        print("clicked")
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
    def play_audio(self,data,reserved_chair):
        audio_stream.play(data)
    class Label(QLabel):
        def __init__(self):
                super().__init__()
                self.initUI()
        @pyqtSlot(str)
        def updateImage(self,img):
            if isinstance(img,bytes):
                pixmap = QPixmap()
                pixmap.loadFromData(img)
                smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.setPixmap(pixmap)
            elif isinstance(img,QImage):
                print("qimage")
                pixmap = QPixmap.fromImage(img)
                smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.setPixmap(smaller_pixmap)
            else:
                print("no byte")
                pixmap = QPixmap(img)
                smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.setPixmap(smaller_pixmap)
                
        def initUI(self):
            self.setScaledContents(True)
            pixmap = QPixmap()
            smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.setPixmap(smaller_pixmap)
            # background = MyThread(self)
            # t = Thread.Thread(target=background.process)
            # background.changePixmap.connect(self.updateImage)
            # t.start()
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
        
        # mic.main(self.client
        while active:
            #stream audio
            try:
                data = self.audio.record()
                self.client.send_audio(data)
            except:
                continue
            # stream video
            try:
            # imageData,reserved_chair = self.queue.get()
                print("send")
                frameName = bodypix.update_ui()
                # data = self.stream.read(self.frames_per_buffer,exception_on_overflow=False)
                with open('../Model/' +frameName, 'rb') as fp:
                    image_data = fp.read()
                    # self.queue.put(image_data)
                    # self.user1_queue.put(image_data,1)
                    self.changePixmap.emit(image_data,int(self.my_reserved_chair))
                    self.client.send_image(image_data) 
                    # time.sleep(2)
            except:
                continue
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
        # Client.main(user_image_data,self.callback)
        self.client,self.my_reserved_chair = Client.main()
        create_receive_thread(self.client,self.window)



class ReceivingThread(QtCore.QObject):  
    notify_video = QtCore.pyqtSignal(bytes,int)
    notify_audio = QtCore.pyqtSignal(bytes,int)
    def __init__(self,socket, parent=None):
        print("super")
        super(ReceivingThread, self).__init__(parent)
        self.socket = socket
        self.standard_letter = ''
        # self.window = parent
        # self.queue = Queue()
    def notify(self,image_data,reserved_chair):
        print("received image is notified")
        print("received",len(image_data))
        # self.notify_ui.emit(image_data,reserved_chair)
    def process(self):
        print("process")
        while True:
            data,data_type,reserved_chair = self.socket.receive_message()
            if data_type == standard_letter.video.value:
                self.notify_video.emit(data,reserved_chair)
            elif data_type == standard_letter.audio.value:
                self.notify_audio.emit(data,reserved_chair)
                


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
