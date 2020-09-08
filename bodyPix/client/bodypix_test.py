import cv2
import numpy as np
from imutils.video import VideoStream
import requests
import sys
from Config import user_frame

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import time

from PIL import Image
from PIL import ImageFilter
from utils import load_graph_model, get_input_tensors, get_output_tensors
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = "3"

# bg = cv2.imread('./assets/Empty-Desks-Default.png')

bg = cv2.imread('../bodypix/client/assets/Empty-Desks-Default.png')

# PATHS
# modelPath = './bodypix_mobilenet_float_050_model-stride16'

# modelPath = './bodypix_mobilenet_quant2_075_model-stride16'
modelPath = '../bodypix/client/bodypix_mobilenet_float_050_model-stride16'
# CONSTANTS
OutputStride = 16
width, height  = user_frame()# 360,480 #450, 640 #90,160

# cap = cv2.VideoCapture(0)
cap = VideoStream(src=0).start()

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

print("Loading model...", end="")
graph = load_graph_model(modelPath)  # downloaded from the link above
print("done.\nLoading sample image...", end="")


# Get input and output tensors
input_tensor_names = get_input_tensors(graph)
output_tensor_names = get_output_tensors(graph)
input_tensor = graph.get_tensor_by_name(input_tensor_names[0])

sess = tf.compat.v1.Session(graph=graph)



def update_ui(bg_resized_32f):
    
    frame = cap.read()
    
    frame = cv2.resize(frame, (width,height))

    img = Image.fromarray(frame)

    imgWidth, imgHeight = img.size

    targetWidth = (int(imgWidth) // OutputStride) * OutputStride 
    targetHeight = (int(imgHeight) // OutputStride) * OutputStride 

    img = img.resize((targetWidth, targetHeight))
    x = tf.keras.preprocessing.image.img_to_array(img, dtype=np.float32)
    InputImageShape = x.shape

    widthResolution = int((InputImageShape[1] - 1) / OutputStride) 
    heightResolution = int((InputImageShape[0] - 1) / OutputStride) 

    #mobile net preprocessing
    x = (x/127.5)-1

    sample_image = x[tf.newaxis, ...]

    output_tensor_names = ['float_segments:0']

    results = sess.run(output_tensor_names, feed_dict={input_tensor: sample_image})

    segments = np.squeeze(results[0], 0)

    # Segmentation MASk
    segmentation_threshold = 0.7
    segmentScores = tf.sigmoid(segments)
    mask = tf.math.greater(segmentScores, tf.constant(segmentation_threshold))
    segmentationMask = tf.dtypes.cast(mask, tf.int32)
    segmentationMask = np.reshape(
        segmentationMask, (segmentationMask.shape[0], segmentationMask.shape[1]))

    print('\t[segmentationMask Dim]', segmentationMask.shape)
    # Create the mask image
    mask_img = Image.fromarray(segmentationMask * 255)
    
    mask_img = mask_img.resize(
        (targetWidth, targetHeight), Image.LANCZOS).convert("RGB")
    
    # Convert the segmentation mask to GRAY
    proc_out = cv2.cvtColor(np.asarray(mask_img), cv2.COLOR_RGB2GRAY)

    #Blur to smoothen the blocky input
    proc_out = cv2.GaussianBlur(proc_out,(151,151),0)

    #Threshold and blur to reduce the part that gets blended
    a, proc_out = cv2.threshold(proc_out,127,255,cv2.THRESH_BINARY)
    proc_out = cv2.GaussianBlur(proc_out,(11,11),0)	

    #Convert back to RGB and float32 for blending	
    proc_out = cv2.cvtColor(proc_out, cv2.COLOR_GRAY2RGB)

    mask_32f = np.float32(proc_out) / 255.0
    #TODO 
    mask_32f = post_process_mask(mask_32f)

    mask_32f_inv = 1.0 - mask_32f
    mask_32f_inv = add_alpha_channel(mask_32f_inv, 0)

    #blend
    img_in  = np.array(img)

    img_in_32f  = np.float32(img_in)
    
    img_fg = cv2.multiply(mask_32f    , img_in_32f    , 1.0/255.0)
    img_fg = add_alpha_channel(img_fg, 255)

    # bg_resized_32f = np.zeros((height, width, 4), dtype=np.uint8)

    # bg_resized_32f = np.zeros(mask_32f_inv.shape, mask_32f_inv.dtype)

    # bg_resized_32f = np.zeros([height, width, 3],dtype=np.float32)
    # bg_resized_32f.fill(255) # or img[:] = 255
    bg_resized_32f = add_alpha_channel(bg_resized_32f, 255)

    print(bg_resized_32f.shape, mask_32f_inv.shape)
    img_bg = cv2.multiply(mask_32f_inv, bg_resized_32f, 1.0/255.0)
    # img_bg = add_alpha_channel(img_bg, 0)

    frame = cv2.add(img_fg, img_bg)

    # frame = cv2.multiply(mask_32f    , frame    , 1.0/255.0)

    # img_out = img_fg
    #convert back to 3channel 8 bit

    # tmp = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
    # b, g, r = cv2.split(frame)
    # rgba = [b,g,r, alpha]
    # frame = cv2.merge(rgba,4)
    print('\t[CHECK frame]',frame.shape, type(frame), frame.dtype)

    frame = np.uint8(frame)

    # frame = cv2.resize(frame, (160,90))
    cv2.imwrite('output.png', frame)
    # len(frame.tobytes())
    return frame

def add_alpha_channel(frame, alpha):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
    frame[... , 3] = alpha
    # b_channel, g_channel, r_channel = cv2.split(frame)
    # if (alpha == 1):
    #     alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50 #creating a dummy alpha channel image.
    # else:
    #     alpha_channel = np.zeros(b_channel.shape, dtype=b_channel.dtype) * 50 #creating a dummy alpha channel image.

    # frame = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    return frame

def post_process_mask(mask):
    mask = cv2.dilate(mask, np.ones((3,3), np.uint8) , iterations=1)
    mask = cv2.blur(mask.astype(float), (10,10))
    return np.float32(mask)

# Resize the background, and preprocess it to 32f.
bg_resized = cv2.resize(bg, (width,height), interpolation = cv2.INTER_AREA)
bg_resized_32f = np.float32(bg_resized)

# while True:

#     frame = update_ui(bg_resized_32f)
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break    