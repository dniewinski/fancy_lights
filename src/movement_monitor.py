#!/usr/bin/env python

import rospy
from std_msgs.msg import *
from geometry_msgs.msg import *

STATE = ""

min_translation = 0.1
min_rotation = 0.05
do_strafe = True
long_idle_time = 10.0

def WATCH_MOVEMENT():
    global pub
    node = rospy.init_node('movement_monitor')

    rospy.Subscriber("cmd_vel", Twist, callback)
    pub = rospy.Publisher("movement_state", String, queue_size=5)

    rospy.spin()

def callback(msg):
    global STATE, min_translation, min_rotation, do_strafe, long_idle_time

    newState = ""

    if abs(msg.linear.x) > min_translation or abs(msg.linear.y) > min_translation:  #Translation happening
        if not do_strafe or abs(msg.linear.x) > abs(msg.linear.y):                  #Only care about forward/backwards (X)
            if msg.linear.x > 0:
                newState = "DRIVING"
            else:
                newState = "REVERSING"
        else:
            if msg.linear.y > 0:
                newState = "STRAFE_LEFT"
            else:
                newState = "STRAFE_RIGHT"

    if msg.angular.z > min_rotation:
        if newState != "":
            newState = newState + "_"
        newState = newState + "TURNING_LEFT"
    if msg.angular.z < min_rotation * -1:
        if newState != "":
            newState = newState + "_"
        newState = newState + "TURNING_RIGHT"

    if newState == "":
        newState = "IDLE"

    if newState != STATE:
        lastSetTime = rospy.get_time()
        pub.publish(String(newState))
        print newState
        STATE = newState

if __name__ == "__main__":
    WATCH_MOVEMENT()
