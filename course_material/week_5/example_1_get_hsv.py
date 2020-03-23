#!/usr/bin/env python
import rospy
import roslib
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.ros_environment import ROSEnvironment
camera = Camera()

point = (0,0)

def onMouse(event, u, v, flags, param):
    global point
    if event == cv2.EVENT_LBUTTONDOWN:
        img = camera.getImage()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        point = (u,v)

        print('Point', u,v)
        print('BGR', img[v,u])
        print('HSV', hsv[v,u])

def main():
    global point
    ROSEnvironment()
    camera.start()
    
    while True:
        img = camera.getImage()
        cv2.circle(img, (point[0], point[1]), 10, (0, 0, 255), -1)
        cv2.imshow("Frame", img[...,::-1])
        # when you click pixel on image, onMouse is called.
        cv2.setMouseCallback("Frame", onMouse)
        key = cv2.waitKey(1)
        if key > 0:
            break



if __name__ == '__main__':
    main()
