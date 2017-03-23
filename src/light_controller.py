#!/usr/bin/env python

from ridgeback_msgs.msg import *
from warthog_msgs.msg import *
import rospy
from std_msgs.msg import *
from colour import Color
import lightPatterns

STATE = "IDLE"

def RAINBOWS():
    global STATE
    rate = 30

    node = rospy.init_node('fancy_light_controller')
    r_os = rospy.Rate(rate)

    robot = "ridgeback"

    msg = None
    lightMapping = None
    if robot.upper() == "RIDGEBACK":
        print "Ridgeback configuration used"
        msg = ridgeback_msgs.msg.Lights
        lightMapping = [0, 1, 2, 3, 4, 5, 6, 7]
        pub = rospy.Publisher('cmd_lights', ridgeback_msgs.msg.Lights, queue_size=10)
    if robot.upper() == "WARTHOG":
        print "Warthog configuration used"
        msg = warthog_msgs.msg.Lights
        lightMapping = [1, 0, 3, 2, 5, 4, 7, 6]
        pub = rospy.Publisher('cmd_lights', warthog_msgs.msg.Lights, queue_size=10)

    if lightMapping and msg:
        patterns = lightPatterns.getPatterns(rate, lightMapping)

        rospy.Subscriber("movement_state", String, callback)

        confused = lightPatterns.lerpLightPattern(lightPatterns.LightStatus(Color("purple")), lightPatterns.LightStatus(Color("green")), 1.0, rate) # Picked the ugliest combo i could think of #

        LASTSTATE = None

        while not rospy.is_shutdown():
            currentPattern = patterns.get(STATE, confused)
            LASTSTATE = STATE
            print LASTSTATE
            for i in currentPattern:
                updateLights(i, pub, msg)
                r_os.sleep()
                if STATE != LASTSTATE or rospy.is_shutdown():
                    break

    else:
        print "Light Mapping or Robot not setup properly"

def callback(msg):
    global STATE
    STATE = msg.data

def updateLights(lStatus, pub, msg):
    data = msg()

    for i in range(len(lStatus.lights)):
        data.lights[i].red = min(max(lStatus.lights[i].red, 0.0), 1.0)
        data.lights[i].green = min(max(lStatus.lights[i].green, 0.0), 1.0)
        data.lights[i].blue = min(max(lStatus.lights[i].blue, 0.0), 1.0)

    pub.publish(data)

if __name__ == "__main__":
    RAINBOWS()
