import tkinter
import Server
from PIL import ImageTk, Image
from io import BytesIO
import os
import sys
from struct import pack
import cv2


######################

# TKinter GUI

#####################

# class Home_Page:
#     def __init__(self):
#         self.image = None
#         self.root = tkinter.Tk() 

def show_image(data,column):
    # title of the application
    print("received")
    stream = BytesIO(data)
    image = Image.open(stream).convert("RGBA")
    stream.close()
    image.show()

def show_image_tkinter(data,column):
    # title of the application
    root = tkinter.Tk()
    root.title('AVC')
    root.geometry("600x300")
    print("received")
    # loading the image
    stream = BytesIO(data)
    image = Image.open(stream).convert("RGBA")
    stream.close()
    imgLabel = ImageTk.PhotoImage(image)
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
            load = Image.open("~/desktop/Developments/Python/Athena-Virtual-Classroom\Minimizing.JPG")
            imgLabel = ImageTk.PhotoImage(load)
            panel = tkinter.Label(self.root, image = imgLabel) 
            panel.grid(row = i, column=j)
    self.root.mainloop()
def access_to_web_cam():
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