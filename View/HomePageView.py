import sys
from PyQt5.QtCore import Qt,QMargins
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget,QLabel)
from PyQt5.QtGui import QPixmap,QImage
from PyQt5 import QtWidgets
import time
# sys.path.insert(1, '../bodypix/client')
# import bodypix
import threading as Thread
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5 import QtCore
from PIL import Image
import cv2

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
    def update_ui(self,data,reserved_chair):
        print("update_reserved_chair")
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
                pixmap = QPixmap()
                pixmap.loadFromData(img)
                smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
                # print(smaller_pixmap)
                self.setPixmap(pixmap)
            elif isinstance(img,QImage):
                pixmap = QPixmap.fromImage(img)
                smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.setPixmap(smaller_pixmap)
            else:
                # pixmap = QPixmap.fromImage(img)
                # print(type(img))
                pixmap = QPixmap('output.png')
                smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.setPixmap(smaller_pixmap)
        def initUI(self):
            self.setScaledContents(True)
            pixmap = QPixmap("./View/Images/Empty-Desks-Default.png")
            smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.setPixmap(smaller_pixmap)
            # background = MyThread(self)
            # t = Thread.Thread(target=background.process)
            # background.changePixmap.connect(self.updateImage)
            # t.start()
            print("layout")
class MyThread(QtCore.QObject):  
    changePixmap = QtCore.pyqtSignal(str)
    def __init__(self, parent = None):
        print("super")
        super(MyThread, self).__init__(parent)
    def process(self):
        print("thread started")
        active = True
        while active:
            # try:
            bodypix.update_ui(self)
            # except Empty:
            #     continue
            

        # cap = cv2.VideoCapture(0)
        # while True:
        #     ret, frame = cap.read()
        #     if ret:
        #         # https://stackoverflow.com/a/55468544/6622587
        #         rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #         h, w, ch = rgbImage.shape
        #         bytesPerLine = ch * w
        #         convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        #         p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        #         self.changePixmap.emit(p)

def main(callback=None):
    print("hello")
    app = QApplication(sys.argv)
    hw = Window()
    # hw.updateImage(user_image_data)
    print("shown")
    # app.quit()
    hw.show()
    callback(hw)
    sys.exit(app.exec_())
    # image_data = None
    # nw.connect()
# if __name__ == '__main__':
#     main()
