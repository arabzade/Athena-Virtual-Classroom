import cv2
import numpy as np
from imutils.video import VideoStream
import requests

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

def get_frame(cap, background, mod = False):
    frame = cap.read()

    frame = cv2.resize(frame, (width, height))

    print(frame.shape, background_scaled.shape)

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
        frame[:,:,c] = frame[:,:,c]*mask + background_scaled[:,:,c]*inv_mask
    return frame

# setup access to the *real* webcam

# cap.set(cv2.CAP_PROP_FPS, 60)

# setup the fake camera
# fake = pyfakewebcam.FakeWebcam('/dev/video20', width, height)

# load the virtual background
background_scaled = cv2.imread("Empty-Desks.png")

print(background_scaled.shape)
# frames forever
# while True:
#     frame = get_frame(cap, background_scaled)
#     # fake webcam expects RGB
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     fake.schedule_frame(frame)

mod, mod1 = False, False

height, width = 360,640
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

vs = VideoStream(src=0).start()

while True:

    frame = get_frame(vs, background_scaled, mod)

    if mod1:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("w"):
        mod = True
    elif key == ord("e"):
        mod1 = True
    elif key == ord("r"):
        mod = False
        mod1 = False

    print('got frame...')
    cv2.imshow('video call' , frame)