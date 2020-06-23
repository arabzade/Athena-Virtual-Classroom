import tkinter
from PIL import ImageTk, Image
import os

######################

# TKinter GUI

#####################


# root = Tk()
# root.title('AVC')
# root.geometry("600x400")


root = tkinter.Tk() 

root.title('AVC')
root.geometry("600x400")
  
# loading the image 
img = ImageTk.PhotoImage(Image.open("/Users/hanieharabzadeh/Downloads/Minimizing.jpg")) 
  
# reading the image 
panel = tkinter.Label(root, image = img) 
  
# setting the application 
panel.pack(side = "bottom", fill = "both", 
           expand = "yes") 
  
# running the application 
root.mainloop() 