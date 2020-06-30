import sys
from PyQt5.QtCore import Qt
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
        self.b1 = self.Box("User Image")
        self.b2 = self.Box("User Image")
        self.b3 = self.Box("User Image")
        self.b4 = self.Box("User Image")
        pushButton = QPushButton(self)
        pushButton.setText("click")
        pushButton.clicked.connect(self.pushButton_clicked)
        grid.addWidget(self.b1, 0, 0)
        grid.addWidget(self.b2, 1, 0)
        grid.addWidget(self.b3, 0, 1)
        grid.addWidget(self.b4, 1, 1)
        grid.addWidget(pushButton,2,0)
        # grid.addWidget(self.createExampleGroup(), 0, 0)
        # grid.addWidget(self.createExampleGroup(), 1, 0)
        # grid.addWidget(self.createExampleGroup(), 0, 1)
        # grid.addWidget(self.createExampleGroup(), 1, 1)
        
        self.setLayout(grid)
        self.setMouseTracking(True)
        self.setWindowTitle("PyQt5 Group Box")
        self.resize(400, 300)
        print("init ended")
    def mouseMoveEvent(self,e):
        x = e.x()
        y = e.y()

        text = f'x: {x},  y: {y}'
        print(text)
    def pushButton_clicked(self):
        self.b1.updateImage()
        print("clicked")
    def createExampleGroup(self):
        groupBox = QGroupBox("Best Food")

        radio1 = QRadioButton("&Radio pizza")
        radio2 = QRadioButton("R&adio taco")
        radio3 = QRadioButton("Ra&dio burrito")

        radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox
    def updateImage(self,data):
        self.b1.updateImage(data)
    def createExampleGroup1(self):
        groupBox = QGroupBox("User Image")
        label = QLabel(self)
        label.setScaledContents(True)
        label.setStyleSheet("background-color: lightgreen") 
        pixmap = QPixmap("Unknown.png")
        # qDebug()<<"File exists -"<<QFileInfo("desktop/Developments/Python/Athena-Virtual-Classroom/Unknown.png").exists()<<" "<<QFileInfo("Unknown.png").absoluteFilePath()
        label.setPixmap(pixmap)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)
        vbox.setAlignment(Qt.AlignCenter)
        groupBox.setLayout(vbox)
        return groupBox
    
    class Box(QGroupBox):
        def __init__(self,title):
            super().__init__()
            self.setTitle(title)
            self.label = QLabel(self)
            self.vbox = QVBoxLayout()
            self.initUI()
        def initUI(self):
            self.label.setScaledContents(True)
            self.label.setStyleSheet("background-color: lightgreen") 
            pixmap = QPixmap("Unknown.png")
            self.label.setPixmap(pixmap)
            self.vbox.addWidget(self.label)
            self.vbox.addStretch(1)
            self.vbox.setAlignment(Qt.AlignCenter)
            self.setLayout(self.vbox)
            print("layout")
        def updateImage(self,data):
            # pixmap = QPixmap("steve-jobs.jpg")
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            smaller_pixmap = pixmap.scaled(275, 183, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label.setPixmap(smaller_pixmap)
            print("call back")

def main(user_image_data,callback=None):
    print("hello")
    app = QApplication(sys.argv)
    hw = Window() 
    hw.updateImage(user_image_data)
    print("shown")
    # app.quit()
    hw.show()
    print("caaaallll")
    callback(hw,user_image_data)
    sys.exit(app.exec_())
    # image_data = None
    # nw.connect()
# if __name__ == '__main__':
#     main()
