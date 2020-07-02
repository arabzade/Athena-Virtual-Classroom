import sys, cv2
sys.path.insert(1, './change_background')
from change_back import driver

#INPUT IMAGE: my_pic.jpg      ||    Background IMAGE: Empty-Desks.png

path = "/Users/ankitd3/Documents/USC/wePodia/Athena-Virtual-Classroom/change_background/images/"
processed_img = driver(path+'my_pic.jpg',path+'Empty-Desks.png',path)

## ------------- Sample usage:
# cv2.imshow('processed_img',processed_img)
# cv2.waitKey(0)