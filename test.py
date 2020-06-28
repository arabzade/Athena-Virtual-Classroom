import sys
sys.path.insert(1, './change_background')
from change_back import driver

processed_img = driver('Empty-Desks.png','/Users/ankitd3/Documents/USC/wePodia/Athena-Virtual-Classroom/change_background/images')
# The driver returns the image as well as saves it in images directory
# Path to processed image: "./change_background/images/processed_img.png"