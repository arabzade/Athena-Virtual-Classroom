import sys
from PyQt5.QtCore import Qt,QMargins
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
        QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget,QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets
import time


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
        self.img1.updateImage("./View/Images/slide1.jpg")
        self.img2.updateImage("./View/Images/Professor.jpg")
        self.img3.updateImage("./View/Images/slide2.jpg")
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
    # def updateImage(self,data):
    #     # self.b1.updateImage(data)
    #     self.img1.updateImage(data)
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
    
    class Box(QGroupBox):
        def __init__(self,title):
            super().__init__()
            self.label = QLabel(self)
            self.vbox = QVBoxLayout()
            self.title = title
            self.initUI()
        def initUI(self):
            self.setTitle(self.title)
            self.label.setScaledContents(True)
            # self.label.setStyleSheet("background-color: lightgreen") 
            pixmap = QPixmap("./View/Images/Empty-Desks-Default.png")
            self.label.setPixmap(pixmap)
            self.vbox.addWidget(self.label)
            self.vbox.addStretch(1)
            self.vbox.setAlignment(Qt.AlignCenter)
            self.vbox.setSpacing(0)
            margins = QMargins(0,0,0,0)
            self.vbox.setContentsMargins(margins)
            self.setLayout(self.vbox)
        def updateImage(self,data):
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            smaller_pixmap = pixmap.scaled(275, 183, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label.setPixmap(smaller_pixmap)
    class Label(QLabel):
        def __init__(self):
                super().__init__()
                self.initUI()
        def initUI(self):
            self.setScaledContents(True)
            # self.setStyleSheet("background-color: lightgreen") 
            pixmap = QPixmap("./View/Images/Empty-Desks-Default.png")
            # pixmap = QPixmap("Empty-Desks.png")
            smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.setPixmap(smaller_pixmap)
            # self.setAlignment(Qt.AlignCenter)
            print("layout")
        def updateImage(self,img):
            if isinstance(img,bytes):
                pixmap = QPixmap()
                pixmap.loadFromData(img)
                smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.setPixmap(smaller_pixmap)
            else:
                pixmap = QPixmap(img)
                smaller_pixmap = pixmap.scaled(320, 180, Qt.KeepAspectRatio, Qt.FastTransformation)
                self.setPixmap(smaller_pixmap)

def main(user_image_data,callback=None):
    print("hello")
    app = QApplication(sys.argv)
    hw = Window()
    # hw.updateImage(user_image_data)
    print("shown")
    # app.quit()
    hw.show()
    callback(hw,user_image_data)
    sys.exit(app.exec_())
    # image_data = None
    # nw.connect()
# if __name__ == '__main__':
#     main()
