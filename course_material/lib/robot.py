#!/usr/bin/env python


import rospy
import roslib
from std_msgs.msg import Float32MultiArray, String, MultiArrayLayout, MultiArrayDimension

deg2rad = 0.0174533

class Robot:

    def __init__(self):
        print('Robot')
        self.cmdPub = rospy.Publisher("/gretchen/joint/cmd", Float32MultiArray, queue_size = 10)
        self.lookatpointPub = rospy.Publisher("/look_at_point", Float32MultiArray, queue_size = 10)

        rospy.Subscriber("/gretchen/joint/poses", Float32MultiArray, self.jointCallback, queue_size = 10)
        self.cur_pan_angle = 0
        self.cur_tilt_angle = 0


        self.cmd_pan = self.getPanAngle()
        self.cmd_tilt = self.getTiltAngle()
        self.max_joint_speed = rospy.get_param('~max_joint_speed', 0.1)
        self.max_pan_angle_radian = rospy.get_param("~max_pan_angle_radian", 1.0)
        self.max_tilt_angle_radian = rospy.get_param("~max_tilt_angle_radian", 1.0)
    def start(self):
        print "starting node"
        rospy.init_node('start', anonymous=True)

        self.initParam()
    def lookatpoint(self, pan, tilt, speed):
        cmd = Float32MultiArray()
        cmd.layout = MultiArrayLayout()
        cmd.layout.dim = []
        obj = MultiArrayDimension()
        obj.label = ""
        obj.size = 0
        obj.stride = 0
        cmd.layout.dim.append(obj)
        cmd.data = [pan, tilt, speed]
        #self.lookatpointPub.publish(cmd)

        #client = actionlib.SimpleActionClient('fibonacci', control_msgs.PointHeadAction)
        #client.wait_for_server()
        #goal = control_msgs.PointHeadGoal()
        #goal.
    def initParam(self):
        self.rate = rospy.get_param("~rate", 20)

            # Joint speeds are given in radians per second
        self.max_joint_speed = rospy.get_param('~max_joint_speed', 0.1)

            # The pan/tilt thresholds indicate what percentage of the image window
            # the ROI needs to be off-center before we make a movement
        self.pan_threshold = rospy.get_param("~pan_threshold", 0.05)
        self.tilt_threshold = rospy.get_param("~tilt_threshold", 0.05)

            # The gain_pan and gain_tilt parameter determine how responsive the
            # servo movements are. If these are set too high, oscillation can result.
        self.gain_pan = rospy.get_param("~gain_pan", 1.0)
        self.gain_tilt = rospy.get_param("~gain_tilt", 1.0)

        self.max_pan_angle_radian = rospy.get_param("~max_pan_angle_radian", 1.0)
        self.max_tilt_angle_radian = rospy.get_param("~max_tilt_angle_radian", 1.0)

    def center(self):
        self.cmd_pan = 0
        self.cmd_tilt = 0
        cmd = Float32MultiArray()
        cmd.data = [self.cmd_pan, self.cmd_tilt]
        self.cmdPub.publish(cmd)

    def move(self, pan_speed, tilt_speed):
        delta_x = -1 * pan_speed
        self.cmd_pan += delta_x
        if self.cmd_pan > self.max_pan_angle_radian:
            self.cmd_pan = self.max_pan_angle_radian
        elif self.cmd_pan < -1.0 * self.max_pan_angle_radian:
            self.cmd_pan = -1.0 * self.max_pan_angle_radian

        delta_y = -1 * tilt_speed
        self.cmd_tilt += delta_y
        if self.cmd_tilt > 1.0 * self.max_tilt_angle_radian:
            self.cmd_tilt = 1.0 * self.max_tilt_angle_radian
        elif self.cmd_tilt < -1.0 * self.max_tilt_angle_radian:
            self.cmd_tilt = -1.0 * self.max_tilt_angle_radian

        cmd = Float32MultiArray()
        cmd.data = [self.cmd_pan, self.cmd_tilt]
        self.cmdPub.publish(cmd)


    def up(self, delta=0.1):
        self.cmd_tilt -= delta
        if self.cmd_tilt < -1.0:
            self.cmd_tilt = -1.0
        cmd = Float32MultiArray()
        cmd.data = [self.cmd_pan, self.cmd_tilt]
        self.cmdPub.publish(cmd)

    def down(self, delta=0.1):
        self.cmd_tilt += delta
        if self.cmd_tilt > 1.0:
            self.cmd_tilt = 1.0
        cmd = Float32MultiArray()
        cmd.data = [self.cmd_pan, self.cmd_tilt]
        self.cmdPub.publish(cmd)

    def left(self, delta=0.1):
        self.cmd_pan += delta
        if self.cmd_pan > 1.0:
            self.cmd_pan = 1.0
        cmd = Float32MultiArray()
        cmd.data = [self.cmd_pan, self.cmd_tilt]
        self.cmdPub.publish(cmd)

    def right(self, delta=0.1):
        self.cmd_pan -= delta
        if self.cmd_pan < -1.0:
            self.cmd_pan = -1.0
        cmd = Float32MultiArray()
        cmd.data = [self.cmd_pan, self.cmd_tilt]
        self.cmdPub.publish(cmd)

    def publishCommand(self, x,y):
        cmd = Float32MultiArray()
        cmd.data = [x, y]
        self.cmdPub.publish(cmd)

    def jointCallback(self, joint_angles):
        self.cur_pan_angle = joint_angles.data[0]
        self.cur_tilt_angle = joint_angles.data[1]

    def getPanAngle(self):
        return self.cur_pan_angle

    def getTiltAngle(self):
        return self.cur_tilt_angle


    def test(self):
        self.cmd_pan += self.max_joint_speed
        print(self.cmd_pan)
        if self.cmd_pan > 1.0 or self.cmd_pan < -1.0 :
            self.max_joint_speed = -1* self.max_joint_speed
        cmd = Float32MultiArray()
        cmd.data = [self.cmd_pan, self.cmd_tilt]
        self.cmdPub.publish(cmd)