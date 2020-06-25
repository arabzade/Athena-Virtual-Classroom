import tkinter
import Server
from PIL import ImageTk, Image
from io import BytesIO
import os
import sys
from struct import pack


######################

# TKinter GUI

#####################

# class Home_Page:
#     def __init__(self):
#         self.image = None
#         self.root = tkinter.Tk() 
def received_image(data,column):
    # title of the application
    # root = tkinter.Tk()
    # root.title('AVC')
    # root.geometry("600x300")

    # # loading the image 
    # load = Image.open("desktop/Developments/Python/Athena-Virtual-Classroom/1.jpg")
    # imgLabel = ImageTk.PhotoImage(load)
    
    # # reading the image 
    # panel = tkinter.Label(root, image = imgLabel) 

    # panel.grid(row = 0, column=0)

    # loading the image2
    # image = Image.open("desktop/Developments/Python/Athena-Virtual-Classroom/1.jpg")
    stream = BytesIO(data)
    image = Image.open(stream).convert("RGBA")
    stream.close()
    image.show()
    # imgLabel2 = ImageTk.PhotoImage(image)
    # panel = tkinter.Label(root, image = imgLabel2) 

    # panel.grid(row = 0, column=column)
    # setting the application 
    # panel.pack(side = "bottom", fill = "both", 
    #         expand = "yes") 

    # running the application 
    # root.mainloop() 
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

# string = "Disconnect"
# encode = string.encode('utf-8')
# length = pack('10s', encode)
# length1 = pack('>Q', len(encode))
# print(length , length1)

# if __name__ == '__main__':
#     h = Home_Page()
# received_image("1.jpg",0)
    # h.messageWindow()
