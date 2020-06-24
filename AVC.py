import tkinter
import Server
from PIL import ImageTk, Image
import os

######################

# TKinter GUI

#####################


# root = Tk()
# root.title('AVC')
# root.geometry("600x400")

class Home_Page:
    def __init__(self):
        self.image = None
        self.root = tkinter.Tk() 
    def show_image(self,image):
        # title of the application
        self.root.title('AVC')
        self.root.geometry("600x400")

        # loading the image 
        imgLabel = ImageTk.PhotoImage(Image.open(image))
        
        # reading the image 
        panel = tkinter.Label(self.root, image = imgLabel) 
        
        # setting the application 
        panel.pack(side = "bottom", fill = "both", 
                expand = "yes") 

        # running the application 
        self.root.mainloop() 


