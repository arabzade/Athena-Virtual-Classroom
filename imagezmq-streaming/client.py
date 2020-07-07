# USAGE
# python client.py --server-ip SERVER_IP

# import the necessary packages
from imutils.video import VideoStream
import numpy as np
import imagezmq
import argparse
import socket
import time
import cv2
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
	help="ip address of the server to which the client will connect")
args = vars(ap.parse_args())

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
	args["server_ip"]))

# get the host name, initialize the video stream, and allow the
# camera sensor to warmup
rpiName = socket.gethostname()
vs = VideoStream(usePiCamera=False).start()
#vs = VideoStream(src=0).start()
time.sleep(2.0)

def resize(dst,img):
	width = img.shape[1]
	height = img.shape[0]
	dim = (width, height)
	resized = cv2.resize(dst, dim, interpolation = cv2.INTER_AREA)
	return resized

ref_img = vs.read()
flag = 1
bg = cv2.imread("./Empty-Desks.png")

while True:
	img = vs.read()
	bg = resize(bg,ref_img)
	if flag==0:
		ref_img = img
	diff1=cv2.subtract(img,ref_img)
	diff2=cv2.subtract(ref_img,img)
	diff = diff1+diff2
	diff[abs(diff)<13.0]=0
	gray = cv2.cvtColor(diff.astype(np.uint8), cv2.COLOR_BGR2GRAY)
	gray[np.abs(gray) < 7] = 0
	fgmask = gray.astype(np.uint8)
	fgmask[fgmask>0]=255
	#invert the mask
	fgmask_inv = cv2.bitwise_not(fgmask)
	#use the masks to extract the relevant parts from FG and BG
	fgimg = cv2.bitwise_and(img,img,mask = fgmask)
	bgimg = cv2.bitwise_and(bg,bg,mask = fgmask_inv)
	#combine both the BG and the FG images
	dst = cv2.add(bgimg,fgimg)
	cv2.imshow("dst",dst)
	key = cv2.waitKey(5) & 0xFF
	if ord('q') == key:
		break
	elif ord('d') == key:
		flag = 1
		print("Background Captured")
	elif ord('r') == key:
		flag = 0
		print("Ready to Capture new Background")
	sender.send_image(rpiName, dst)
cv2.destroyAllWindows()
vs.release()