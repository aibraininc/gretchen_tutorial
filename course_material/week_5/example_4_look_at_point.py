#!/usr/bin/env python
import rospy
import roslib
import cv2
import sys
sys.path.append('..')
from lib.camera_v2 import Camera
from lib.robot import Robot
robot = None

def onMouse(camera, u, v):
    print(u, v)
    (x,y,z) = camera.convert2d_3d(u,v)
    print (x,y,z,'on camera axis')
    (x,y,z) = camera.convert3d_3d(x,y,z)
    print (x,y,z,'on robot axis')

    global robot
    robot.lookatpoint(x,y,z, waitResult = False)
    print('look at point end')

def main():
    rospy.init_node('camera_show', anonymous=True)
    global robot
    robot = Robot()

    camera1 = Camera(click=onMouse)
    camera1.start()
    
    while True:
        frame = camera1.image
        camera1.showImage(frame)

if __name__ == '__main__':
    main()
