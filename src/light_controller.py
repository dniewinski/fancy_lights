#!/usr/bin/env python

from ridgeback_msgs.msg import *
import rospy
from colour import Color
import lightPatterns

def RAINBOWS():
    rate = 30
    pub = rospy.Publisher('cmd_lights', ridgeback_msgs.msg.Lights, queue_size=10)
    node = rospy.init_node('rainbows')
    r_os = rospy.Rate(rate)

    patterns = lightPatterns.getPatterns(rate)

    confused = lightPatterns.lerpLightPattern(lightPatterns.LightStatus(Color("purple")), lightPatterns.LightStatus(Color("green")), 1.0, rate) # Picked the ugliest combo i could think of #

    STATE = "TURNING_LEFT"
    LASTSTATE = None

    while not rospy.is_shutdown():
        currentPattern = patterns.get(STATE, confused)
        LASTSTATE = STATE
        for i in currentPattern:
            updateLights(i, pub)
            r_os.sleep()
            if STATE != LASTSTATE or rospy.is_shutdown():
                break

def updateLights(lStatus, pub):
    data = ridgeback_msgs.msg.Lights()

    for i in range(len(lStatus.lights)):
        data.lights[i].red = min(max(lStatus.lights[i].red, 0.0), 1.0)
        data.lights[i].green = min(max(lStatus.lights[i].green, 0.0), 1.0)
        data.lights[i].blue = min(max(lStatus.lights[i].blue, 0.0), 1.0)

    pub.publish(data)

if __name__ == "__main__":
    RAINBOWS()
