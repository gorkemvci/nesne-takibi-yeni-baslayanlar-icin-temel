import cv2 as cv
from random import randint
import time
tracker = cv.legacy.TrackerCSRT_create()
video = cv.VideoCapture(0)
ok, frame = video.read()
if not ok:
    print('Error while loading the frame!')
cascade = cv.CascadeClassifier('myhaar.xml')
def detect():
  while True:
    ok,frame = video.read()
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    faces = cascade.detectMultiScale(frame_gray,minSize=(70,90))
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame =cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (0, 0, 255), 2)
         #cv.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 2)
        if x:
            return x, y, w, h

bbox = detect()
ok = tracker.init(frame, bbox)
colors = (randint(0, 255), randint(0, 255), randint(0, 255))

while True:
    ok, frame = video.read()
    if not ok:
        break
    ok, bbox = tracker.update(frame)
    if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        center = (x + w//2, y + h//2)
        cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (0, 0, 255), 2)
    else:
        print('Tracking failure! We will execute the haarcascade detector')
        bbox = detect()
        tracker = cv.legacy.TrackerCSRT_create()
        tracker.init(frame,bbox)

    cv.imshow('Tracking', frame)
    k = cv.waitKey(1) & 0XFF
    if k == 27: # esc
        break




 