import cv2
import numpy as np
from imutils.video import VideoStream
import requests

def get_mask(frame, bodypix_url='http://localhost:8080'):
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

vs = VideoStream(src=0).start()
while True:
    frame = vs.read()
    cv2.imwrite('receivedSegmentation.png' , get_mask(frame))




