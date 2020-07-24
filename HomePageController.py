import sys
sys.path.insert(1, '../change_background')
from change_back import driver
import cv2
sys.path.insert(1, '../bodyPix/client')
sys.path.insert(1, '../View')
from View import HomePageView
sys.path.insert(1, '../Model')
# from Model import Client
import bodypix
from Model import ClientV2
import time
import threading as Thread
from PyQt5 import QtCore
import sys
from imutils.video import VideoStream
from queue import Queue,Empty

class HomePage_Controller():
    def __init__(self):
        self.user_image_data = None
        # self.take_shot(self.callback)
        # self.take_shot_from_webcam(self.callback)
        # self.callback(None)
        self.navigate_to_homepage()
        self.window = None
        self.clientBgThread = None
        self.bgQueue = Queue()
    def startBgQueue(self,notify):
        background = MyThread()
        t = Thread.Thread(target=background.process)
        background.notify.connect(notify)
        t.start()

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
        with open('./Model/' +frameName, 'rb') as fp:
            print("open")
            image_data = fp.read()
            self.window.update_ui(image_data,1)
        
    def callback_from_hmpage(self,window):
        print("home page is created and call back from homepage")
        q = Queue()
        self.window = window
        # ui_thread = HomePageView.UIThread(window,ui_queue)
        # ui_t = Thread.Thread(target=ui_thread.process)
        # ui_thread.changePixmap.connect(window.notify)
        # ui_t.start()
        background = MyThread(window,q)
        t = Thread.Thread(target=background.process)
        background.notify.connect(self.notify)
        t.start()
        # while True:
        #     time.sleep(10)
        #     frameName = bodypix.update_ui()
        #     with open('./Model/' +frameName, 'rb') as fp:
        #         print("open")
        #         image_data = fp.read()
        #         # background.queue.put(image_data)
        #         self.window.update_ui(image_data,1)
        #         self.window.show()
        #     background.queue.put(image_data)
        # # if background.client.user_reserved_chair is not None:
        #     if Thread.current_thread() is Thread.main_thread():
        #         print("yes")
            # self.window.update_ui(image_data,1)
    # background.notify.connect(self.notify)
    def navigate_to_homepage(self):
        print("navigate to homepage")
        # HomePageView.main(user_image_data,self.callback_from_hmpage)
        HomePageView.main(self.callback_from_hmpage)
    # @QtCore.pyqtSlot(bytes,str)
    def notify(self,data,reserved_chair):
        print("notify")
        with open('./Model/' +'output.png', 'rb') as fp:
            print("open")
            image_data = fp.read()
        # print("I have been notified",len(data),int(reserved_chair))
            self.window.update_ui(image_data,1)
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


class MyThread(QtCore.QThread):
    notify = QtCore.pyqtSignal()
    def __init__(self,queue,parent = None):
        super(MyThread, self).__init__(parent)
        self.should_continue = True
        self.client = None
        # self.user_image_data = user_image_data
        # self.queue = queue
        self.my_reserved_chair = None
        self.other_client_data = None
    def callback(self,data,client_number):
        print("client_number" , client_number)
        self.notify.emit(data,client_number)
    # def send_image(self,frame):
    #     self.client.send_image(frame,self.callback)
    def process(self):
        self.connect_to_socket()

        # while self.should_continue:
        print("should countinue")
        while True:
            try:
                frame = self.queue.get()
                self.client.send_image(frame) 
            except:
                continue
            # Here, do your server stuff.
    def connect_to_socket(self):
        print("socket is connecting")
        # Client.main(user_image_data,self.callback)
        self.client,my_reserved_chair = ClientV2.main()
    
if __name__ == "__main__":
    hm_p = HomePage_Controller()