#!/bin/env python3
#-*- encoding: utf-8 -*-

import cv2
import numpy as np

# start this:
# ffmpeg -i /dev/video0 -f mpegts udp://localhost:1337
# ffmpeg -i rtsp://... -f mpegts udp://localhost:1337

# cameraCapture = cv2.VideoCapture('udp://@224.0.0.1:9999?pkt_size=1316&overrun_nonfatal=1&fifo_size=50000000')

cameraCapture = cv2.VideoCapture('udp://@224.0.0.1:9999?pkt_size=1316&overrun_nonfatal=1')


print('Showing camera feed. Click window or press any key to stop.')

def pixelTrans(frame):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    light_orange = (12, 130, 200)
    dark_orange = (23, 255, 255)

    light_white = (0,0,230)
    dark_white = (10,20,255)

    mask = cv2.inRange(hsv, light_orange, dark_orange)
    # res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    # cv2.imshow('res',res)

    # return (frame >= [190,200,125]).all(axis = 2) & (frame <= [255,255,255]).all(axis = 2)


while True:
    success, frame = cameraCapture.read()
    pixelTrans(frame)
    # frame[np.where(pixelTrans(frame))] = [0,255,0]     # it works
    # cv2.imshow('MyWindow', frame)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cv2.destroyAllWindows()
cameraCapture.release()

