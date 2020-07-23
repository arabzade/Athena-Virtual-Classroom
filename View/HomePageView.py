import sys
from PyQt5.QtCore import Qt,QMargins
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget,QLabel)
from PyQt5.QtGui import QPixmap,QImage
from PyQt5 import QtWidgets
import time
sys.path.insert(1, '../bodypix/client')
sys.path.insert(1, '../Model')
import ClientV2
import bodypix
sys.path.insert(1, '../')
import HomePageController
import threading as Thread
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5 import QtCore
from PIL import Image
import cv2
from queue import Queue,Empty





network_queue = Queue()
network_thread = None


class Window(QWidget):
    def __init__(self, parent=None ):
        super(Window, self).__init__(parent)
        self.user_image_data = None
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
        # self.img1.updateImage("./View/Images/slide1.jpg")
        # self.img2.updateImage("./View/Images/Professor.jpg")
        # self.img3.updateImage("./View/Images/slide2.jpg")
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
        print(sys.path)
        self.setLayout(grid)
        self.setMouseTracking(True)
        self.setWindowTitle("PyQt5 Group Box")
        print("path    :" , sys.path)
        self.resize(960, 540)
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
        # if network_thread is not None and network_thread.my_reserved_chair is not None:
            # if reserved_chair == network_thread.my_reserved_chair:
            #     print('data set')
            #     network_thread.queue.put(data)
        # print("update_reserved_chair",reserved_chair)
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
    
    class Label(QLabel):
        def __init__(self):
                super().__init__()
                self.initUI()
        @pyqtSlot(str)
        def updateImage(self,img):
            print("update")
            if isinstance(img,bytes):
                print("bytes")
                pixmap = QPixmap()
                pixmap.loadFromData(img)
                smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
                # print(smaller_pixmap)
                self.setPixmap(pixmap)
            elif isinstance(img,QImage):
                print("qimage")
                pixmap = QPixmap.fromImage(img)
                smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.setPixmap(smaller_pixmap)
            else:
                print("no byte")
                # pixmap = QPixmap.fromImage(img)
                # print(type(img))
                pixmap = QPixmap('output.png')
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
            print("layout")
class UIThread(QtCore.QObject):  
    changePixmap = QtCore.pyqtSignal(bytes,int)
    def __init__(self, parent=None):
        print("super")
        super(UIThread, self).__init__(parent)
        # self.window = parent
        self.queue = Queue()
        self.client = None
        self.my_reserved_chair = None
    def process(self):
        print("thread started")
        active = True
        self.connect_to_socket()
        while active:
            try:
                # print("update")
                # imageData,reserved_chair = self.queue.get()
                frameName = bodypix.update_ui()
                with open('../Model/' +frameName, 'rb') as fp:
                    print("open")
                    image_data = fp.read()
                    self.queue.put(image_data)
                    self.changePixmap.emit(image_data,1)
                    # self.client.send_image(image_data) 
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
        self.client,my_reserved_chair = ClientV2.main()

def main(callback=None):
    print("hello")
    app = QApplication(sys.argv)
    hw = Window()
    # hw.updateImage(user_image_data)
    print("shown")
    # app.quit()
    # time.sleep(2)
    # callback(hw)
    ui_thread = UIThread()
    t = Thread.Thread(target=ui_thread.process)
    ui_thread.changePixmap.connect(hw.update_ui)
    t.start()
    # network_thread = HomePageController.MyThread(Queue())
    # nt = Thread.Thread(target=network_thread.process)
    # # network_thread.notify.connect(hw.update_ui)
    # nt.start()
    hw.show()
    sys.exit(app.exec_())
    # image_data = None
    # nw.connect()
if __name__ == '__main__':
    main()
