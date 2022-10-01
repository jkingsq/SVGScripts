import math
from SVGDocument import SVGDocument as svg
import vector2D as vec
import colors

width = 1920.0
height = 1920.0

center = (width/2.0, height/2.0)

doc = svg(width, height)

debug = True

background = (48, 48, 48)

r, g, b = background
doc.setFillColor(r, g, b)
doc.addRect((0, 0), width, height)

maxRadius = max(width,height)/2.0
minCircleRadius = maxRadius/100.0
maxCircleRadius = maxRadius/6.0
maxTheta = 6.0 * math.pi
thetaOffset = math.pi/2.0

rayPairs = 6
radii = 200

waveDepth = 2.0 * math.pi / rayPairs

def circleFill(t, theta):
    inner = (255, 255, 255)
    outer = colors.colorCycle(theta)
    return colors.mixColors(inner, outer, 1)

debugPoints = []

doc.setStrokeColor(0, 0, 0)

for i in range(radii):
    t = float(i) / float(radii)
    radius = t**3 * maxRadius
    waveTheta = t * maxTheta
    circleRadius = (1-t) * (maxCircleRadius-minCircleRadius) + minCircleRadius
    doc.setStrokeWidth(circleRadius/40.0)
    for j in range(rayPairs):
        theta = j * (2.0*math.pi) / rayPairs + thetaOffset +\
                math.sin(waveTheta)*waveDepth/2
        circle = vec.sum(center, vec.fromPolar(radius, theta))
        r, g, b = circleFill(t, theta)
        doc.setFillColor(r, g, b)
        doc.addCircle(circle, circleRadius)
    for j in range(rayPairs):
        theta = j * (2.0*math.pi) / rayPairs + thetaOffset -\
                math.sin(waveTheta)*waveDepth/2
        circle = vec.sum(center, vec.fromPolar(radius, theta))
        r, g, b = circleFill(t, theta)
        doc.setFillColor(r, g, b)
        doc.addCircle(circle, circleRadius)

doc.write("waveSun.svg")
