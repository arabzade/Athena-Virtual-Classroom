import cv2
import numpy as np
from imutils.video import VideoStream
import requests
import sys
view = sys.path.insert(1, '../../View')
import HomePageView
from PyQt5.QtGui import QImage
from PIL import Image
import socketio

def get_mask(frame, bodypix_url='http://localhost:8080'): #https://athena-virtual-classroom.wl.r.appspot.com:8080
    _ , data = cv2.imencode(".jpg", frame)
    r = requests.post(
              url=bodypix_url,
              data=data.tobytes(),
              headers={'Content-Type': 'application/octet-stream'})
    # convert raw bytes to a numpy array
    # # raw data is uint8[width * height] with value 0 or 1
    mask = np.frombuffer(r.content, dtype=np.uint8)
    mask = mask.reshape((frame.shape[0], frame.shape[1]))
    return mask

def post_process_mask(mask):
    mask = cv2.dilate(mask, np.ones((10,10), np.uint8) , iterations=1)
    mask = cv2.blur(mask.astype(float), (30,30))
    return mask

def shift_image(img, dx, dy):
    img = np.roll(img, dy, axis=0)
    img = np.roll(img, dx, axis=1)
    if dy>0:
        img[:dy, :] = 0
    elif dy<0:
        img[dy:, :] = 0
    if dx>0:
        img[:, :dx] = 0
    elif dx<0:
        img[:, dx:] = 0
    return img

def hologram_effect(img):
    # add a blue tint
    holo = cv2.applyColorMap(img, cv2.COLORMAP_WINTER)
    # add a halftone effect
    bandLength, bandGap = 2, 3
    for y in range(holo.shape[0]):
        if y % (bandLength+bandGap) < bandLength:
            holo[y,:,:] = holo[y,:,:] * np.random.uniform(0.1, 0.3)
    # add some ghosting
    holo_blur = cv2.addWeighted(holo, 0.2, shift_image(holo.copy(), 5, 5), 0.8, 0)
    holo_blur = cv2.addWeighted(holo_blur, 0.4, shift_image(holo.copy(), -5, -5), 0.6, 0)
    # combine with the original color, oversaturated
    out = cv2.addWeighted(img, 0.5, holo_blur, 0.6, 0)
    return out

def get_frame(cap, background_scaled, mod = False):
    frame = cap.read()

    frame = cv2.resize(frame, (width, height))
    # background_scaled = cv2.resize(background_scaled, (width, height))

    # print(frame.shape, background_scaled.shape)

    # fetch the mask with retries (the app needs to warmup and we're lazy)
    # e v e n t u a l l y c o n s i s t e n t
    mask = None
    while mask is None:
        try:
            mask = get_mask(frame)
        except requests.RequestException:
            print("mask request failed, retrying")
    # post-process mask and frame
    mask = post_process_mask(mask)

    if mod:
        frame = hologram_effect(frame)
    # composite the foreground and background
    inv_mask = 1-mask
    for c in range(frame.shape[2]):
        frame[:,:,c] = frame[:,:,c]*mask
    
    return frame
# window = None


# setup access to the *real* webcam

# cap.set(cv2.CAP_PROP_FPS, 60)

# setup the fake camera
# fake = pyfakewebcam.FakeWebcam('/dev/video20', width, height)

# load the virtual background


height, width = 360,640

# todo with hanieh
def update_ui(thread,callback):
    print("update label")
    mod, mod1 = False, False
    mode2 = True
    vs = VideoStream(src=0).start()
    background_scaled = cv2.imread("Empty-Desks.png")
    while True:
        frame = get_frame(vs, background_scaled, mod)
        if mod1:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif mode2:
            tmp = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
            b, g, r = cv2.split(frame)
            rgba = [b,g,r, alpha]
            frame = cv2.merge(rgba,4)
        
        key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
            
        if key == ord("w"):
            mod = True
        elif key == ord("e"):
            mod1 = True
        elif key == ord("r"):
            mod = False
            mod1 = False
        # image = Image.fromarray(frame, 'RGB')
        # frame_in_bytes = frame.bytes
        # # print(type(image))
        # height, width, channel = frame.shape
        # bytesPerLine = 3 * width
        # qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_Indexed8)
        # print(type(thread.changePixmap))
        
        # thread.changePixmap.emit('output.png')
        print('got frame...')
        cv2.imwrite('./Model/output.png' , frame)
        len(frame.tobytes())
        callback('output.png')


# todo with ankit
def get_segmented_frame():
    mod, mod1 = False, False
    mode2 = True
    vs = VideoStream(src=0).start()
    background_scaled = cv2.imread("Empty-Desks.png")
    while True:
        frame = get_frame(vs, background_scaled, mod)
        if mod1:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif mode2:
            tmp = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
            b, g, r = cv2.split(frame)
            rgba = [b,g,r, alpha]
            frame = cv2.merge(rgba,4)
        
        key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
            
        if key == ord("w"):
            mod = True
        elif key == ord("e"):
            mod1 = True
        elif key == ord("r"):
            mod = False
            mod1 = False
        return frame








# if __name__ == "__main__":
    

#     # frames forever
#     # while True:
#     #     frame = get_frame(cap, background_scaled)
#     #     # fake webcam expects RGB
#     #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     #     fake.schedule_frame(frame)

#     # cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#     # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    # HomePageView.main(callback_from_hmpage)
#     pass
    