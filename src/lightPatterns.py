from colour import Color

FLT = 0
FLB = 1
FRT = 2
FRB = 3
BLT = 4
BLB = 5
BRT = 6
BRB = 7

def getPatterns(rate):
    patterns = {}

    print "INITIALIZING PATTERNS"

    FRONT = [FLT, FLB, FRT, FRB]
    BACK = [BLT, BLB, BRT, BRB]
    LEFT = [FLT, FLB, BLT, BLB]
    RIGHT = [FRT, FRB, BRT, BRB]
    TOP = [FRT, FLT, BRT, BLT]
    BOTTOM = [FRB, FLB, BLB, BRB]
    ALL = [0,1,2,3,4,5,6,7]

    DRIVING_STATUS = LightStatus(Color("white"))
    DRIVING_STATUS = augmentLightStatus(Color("red"), DRIVING_STATUS, BACK)

    driving = []
    driving.extend(lerpLightPattern(DRIVING_STATUS, DRIVING_STATUS, 1.0, rate))

    turning_left = []
    left_on = LightStatus()
    left_on.copyLights(DRIVING_STATUS)
    left_on = augmentLightStatus(Color("yellow"), left_on, LEFT, BOTTOM)
    left_off = LightStatus()
    left_off.copyLights(DRIVING_STATUS)
    left_off = augmentLightStatus(Color("black"), left_off, LEFT, BOTTOM)
    turning_left.extend(lerpLightPattern(left_on, left_off, 1.5, rate))

    turning_right = []
    right_on = LightStatus()
    right_on.copyLights(DRIVING_STATUS)
    right_on = augmentLightStatus(Color("Yellow"), right_on, RIGHT, BOTTOM)
    right_off = LightStatus()
    right_off.copyLights(DRIVING_STATUS)
    right_off = augmentLightStatus(Color("Black"), right_off, RIGHT, BOTTOM)
    turning_right.extend(lerpLightPattern(right_on, right_off, 1.5, rate))

    rainbow = []
    rainbow.extend(lerpLightPattern(LightStatus(Color("red")), LightStatus(Color(rgb=(1, 1, 0))), 2.0, rate))
    rainbow.extend(lerpLightPattern(LightStatus(Color(rgb=(1, 1, 0))), LightStatus(Color("green")), 2.0, rate))
    rainbow.extend(lerpLightPattern(LightStatus(Color("green")), LightStatus(Color(rgb=(0, 1, 1))), 2.0, rate))
    rainbow.extend(lerpLightPattern(LightStatus(Color(rgb=(0, 1, 1))), LightStatus(Color("blue")), 2.0, rate))
    rainbow.extend(lerpLightPattern(LightStatus(Color("blue")), LightStatus(Color(rgb=(1, 0, 1))), 2.0, rate))
    rainbow.extend(lerpLightPattern(LightStatus(Color(rgb=(1, 0, 1))), LightStatus(Color("red")), 2.0, rate))

    patterns["DRIVING"] = driving
    patterns["IDLE"] = driving
    patterns["TURNING_LEFT"] = turning_left
    patterns["TURNING_RIGHT"] = turning_right
    patterns["IDLE_LONG"] = rainbow

    print str(len(patterns)) + " CREATED"
    print patterns.keys()

    writePatterns(patterns)

    return patterns

def writePatterns(patterns):
    for key, value in patterns.iteritems():
        html = open(key + ".html", "w")
        html.write("<table>\n")
        for i in value:
            html.write("<tr>\n")
            for x in i.lights:
                html.write("<td bgcolor=\"" + str(x) + "\">_</td>")
            html.write("</tr>\n")
        html.write("</table>\n")
        html.close()

############################## LIGHT STATUS ##############################
def augmentLightStatus(newColour, originalStatus = None, set1 = [0,1,2,3,4,5,6,7], set2 = [0,1,2,3,4,5,6,7], set3 = [0,1,2,3,4,5,6,7]):
    if not originalStatus:
        originalStatus = LightStatus()

    indicies = []
    for i in range(len(originalStatus.lights)):
        if i in set1 and i in set2 and i in set3:
            indicies.append(i)

    for i in indicies:
        originalStatus.lights[i] = newColour

    return originalStatus

############################## LIGHT PATTERN ##############################
def lerpLightPattern(ls1, ls2, t, rate, name=None):
    lightPattern = []
    data = []

    for i in range(len(ls1.lights)):
        data.append(colourLerp(ls1.lights[i], ls2.lights[i], t, rate))

    for i in range(len(data[0])):
        newStatus = LightStatus()
        for l in range(8):
            newStatus.lights[l] = data[l][i]
        lightPattern.append(newStatus)

    data = []
    return lightPattern

############################## COLOUR ##############################
def colourLerp(c1, c2, t, rate):
    steps = int(round(t * rate))
    step_size = 1.0/steps

    rColour = []

    for i in range(steps + 1):
        newC = Color()
        newC.red = c1.red + ( c2.red - c1.red ) * ( i * step_size )
        newC.green = c1.green + ( c2.green - c1.green ) * ( i * step_size )
        newC.blue = c1.blue + ( c2.blue - c1.blue ) * ( i * step_size )
        rColour.append(newC)

    return rColour

############################## CLASSES ##############################
class LightStatus:
    def __init__(self, c = Color('black')):
        self.lights = []
        for i in range(8):
            self.lights.append(c)

    def copyLights(self, lsIn):
        self.lights = []
        for i in lsIn.lights:
            self.lights.append(i)
