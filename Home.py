import tkinter
import Server
from PIL import ImageTk, Image
from io import BytesIO
import os
import sys
from struct import pack
# import cv2
from MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap


######################

# TKinter GUI

#####################

class Home_Page(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(Home_Page, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.title = 'PyQt5 image - pythonspot.com'
        # self.updateUI()
    def updateUI(self):
        pixmap = QPixmap("Unknown.png")
        self.ui.UserImage.setPixmap(pixmap)
        self.ui.UserImage.setScaledContents = True
        self.setWindowTitle(self.title)
        # self.show()

    def show_image(self,data,column):
        # title of the application
        print("received")
        stream = BytesIO(data)
        image = Image.open(stream).convert("RGBA")
        stream.close()
        image.show()

    def show_image_tkinter(self,data,column):
        # title of the application
        root = tkinter.Tk()
        root.title('AVC')
        root.geometry("600x300")
        print("received")
        # loading the image
        # stream = BytesIO(data)
        imageFileName = "Unknown.png"
        with open(imageFileName, 'rb') as fp:
            load = Image.open(fp)
            # image = Image.open(stream).convert("RGBA")
            # stream.close()
            imgLabel = ImageTk.PhotoImage(load)
            # imgLabel = ImageTk.PhotoImage(image)
            # placing in the grid
            panel = tkinter.Label(root, image = imgLabel) 
            panel.grid(row = 0, column=column)
            # running the application 
            root.mainloop()
    def messageWindow(self):
        self.root.title('AVC')
        self.root.geometry("600x400")
        print(os.listdir())
        row = 3
        column = 8
        for i in range(row):
            for j in range(column):
                load = Image.open("desktop/Developments/Python/Athena-Virtual-Classroom\Minimizing.JPG")
                imgLabel = ImageTk.PhotoImage(load)
                panel = tkinter.Label(self.root, image = imgLabel) 
                panel.grid(row = i, column=j)
        self.root.mainloop()
    def take_shot_from_webcam(self,callback = None):
        cap = cv2.VideoCapture(0)
        # Check if the webcam is opened correctly
        if not cap.isOpened():
            raise IOError("Cannot open webcam")

        while True:
            ret, frame = cap.read()
            img_counter = 0
            try:
                frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                cv2.imshow('Input', frame)

                c = cv2.waitKey(1)
                if c == 27:
                    break
                elif c == 32:
                    img_name = "opencv_frame_{}.png".format(img_counter)
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    if callback:
                        callback(img_name)
                    img_counter += 1
            except:
                print("no access")
        cap.release()
        cv2.destroyAllWindows()
# string = "Disconnect"
# encode = string.encode('utf-8')
# length = pack('10s', encode)
# length1 = pack('>Q', len(encode))
# print(length , length1)

# if __name__ == '__main__':
#     h = Home_Page()
# received_image("1.jpg",0)
    # h.messageWindow()
# access_to_web_cam()
# show_image_tkinter(None,0)
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = Home_Page()
    application.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()