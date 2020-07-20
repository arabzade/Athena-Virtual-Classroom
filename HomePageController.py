import sys
sys.path.insert(1, './change_background')
from change_back import driver
import cv2
sys.path.insert(1, './View')
from View import HomePageView
sys.path.insert(1, './Model')
# from Model import Client
sys.path.insert(1, './bodypix/client')
import bodypix
from Model import ClientV2
import time
import threading as Thread
from PyQt5 import QtCore
import sys
from imutils.video import VideoStream

class HomePage_Controller():
    def __init__(self):
        self.user_image_data = None
        # self.take_shot(self.callback)
        # self.take_shot_from_webcam(self.callback)
        self.callback(None)
        self.window = None
    def take_shot(self, callback=None):
        print("start process")
        processed_img = driver('Empty-Desks.png','./change_background/images')
        print("finish process")
        isProcessing = True
        while isProcessing:
            print("process")
            if processed_img != None:
                print("received processed image")
                callback('Empty-Desks.png')
                isProcessing = False 
    # def take_shot(self,callback=None):
    #     vs = VideoStream(src=0).start()
    #     while True:
    #         vs.read()
    def callback(self,imageFileName):
        # print("call back from processing")
        # print("opened")
        # assert(len(image_data))
        print("imagedata")
        # self.user_image_data = image_data
        self.navigate_to_homepage()
        # self.connect_to_socket(image_data)
    def callback_from_hmpage(self,window):
        print("home page is created and call back from homepage")
        self.window = window
        background = MyThread(window)
        t = Thread.Thread(target=background.process)
        t.start()
        background.notify.connect(self.notify)
        # background.notify.connect(self.notify)
    def navigate_to_homepage(self):
        print("navigate to homepage")
        # HomePageView.main(user_image_data,self.callback_from_hmpage)
        HomePageView.main(self.callback_from_hmpage)
    # @QtCore.pyqtSlot()
    def notify(self,data,reserved_chair):
        print("I have been notified",len(data),reserved_chair)
        self.window.update_ui(data,reserved_chair)
    def take_shot_from_webcam(self,callback = None):
        #cap = cv2.VideoCapture(0)
        vs = VideoStream(src=0).start()

        # Check if the webcam is opened correctly
        # if not cap.isOpened():
        #     raise IOError("Cannot open webcam")
        while True:
            frame = vs.read()
            # ret, frame = cap.read()
            img_counter = 0
            # try:
            # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            cv2.imshow('Input', frame)
            c = cv2.waitKey(1)
            if c == 27:
                break
            elif c == 32:
                cv2.destroyAllWindows()
                vs.stop()
                
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)

                path = "./"
                frame = driver(path+"opencv_frame_{}.png".format(img_counter),path+"change_background/images/Empty-Desks.png",path)

                # cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                if callback:
                    # cap.release()
                    vs.stop()
                    cv2.destroyAllWindows()
                    callback(img_name)
                    break
                img_counter += 1
            # except:
            # print("no access")
        # cap.release()
        cv2.destroyAllWindows()


class MyThread(QtCore.QObject):
    notify = QtCore.pyqtSignal(bytes,int)
    def __init__(self, parent):
        print("thread")
        super(MyThread, self).__init__(parent)
        print("thread1")
        self.should_continue = True
        self.client = None
        # self.user_image_data = user_image_data
        self.other_client_data = None
    def callback(self,data,client_number):
        print("client_number" , client_number)
        self.notify.emit(data,client_number)
    def send_image(self,frame):
        self.client.send_image(frame,self.callback)
    def process(self):
        self.connect_to_socket()
        # while self.should_continue:
        print("should countinue")
        bodypix.update_ui(self,self.send_image)
            # Here, do your server stuff.
    def connect_to_socket(self):
        print("socket is connecting")
        # Client.main(user_image_data,self.callback)
        self.client = ClientV2.main(self.callback)
    
if __name__ == "__main__":
    hm_p = HomePage_Controller()