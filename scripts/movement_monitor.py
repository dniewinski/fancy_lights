#!/usr/bin/env python

import rospy
from std_msgs.msg import *
from geometry_msgs.msg import *

STATE = ""

def WATCH_MOVEMENT():
    global pub, min_translation, min_rotation, do_strafe, long_idle_time
    node = rospy.init_node('movement_monitor')

    min_translation = rospy.get_param('~min_translation', 0.1)
    min_rotation = rospy.get_param('~min_rotation', 0.05)
    do_strafe = rospy.get_param('~do_strafe', True)
    long_idle_time = rospy.get_param('~long_idle_time', 10.0)
    cmd_vel_topic = rospy.get_param('~cmd_vel_topic', "/cmd_vel")

    rospy.Subscriber(cmd_vel_topic, Twist, callback)
    pub = rospy.Publisher("movement_state", String, queue_size=5, latch=True)

    pub.publish(String("IDLE"))
    rospy.spin()

def callback(msg):
    global STATE, min_translation, min_rotation, do_strafe, long_idle_time, lastSetTime
    lastSetTime = rospy.get_time()
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
        if rospy.get_time() - lastSetTime >= long_idle_time:
            newState = "IDLE_LONG"

    if newState != STATE:
        lastSetTime = rospy.get_time()
        pub.publish(String(newState))
        STATE = newState

if __name__ == "__main__":
    WATCH_MOVEMENT()
