import math
from SVGDocument import SVGDocument as svg
import vector2D as vec
import colors

debug = False

width = 1920.0
height = 1080.0
padding = 15
edgeAngle = math.pi / 10
startTheta = edgeAngle/2 + math.atan2(height, width) + math.pi

startColor = (255, 128, 0)
endColor = (0, 128, 255)
backgroundColor = (0, 96, 192)
# number from 0-1 affecting color transition
# closer to 0 will bias toward endColor, closer to 1 will bias toward startColor
blendExponent = 3/8

doc = svg(width, height)

# center of the pattern, presumed to be within the rectangle of the image
center = (width*2/3, height*2/3)

r, g, b = backgroundColor
doc.setStrokeWidth(0)
doc.setFillColor(r, g, b)
doc.addRect((0,0), width, height)

doc.setStrokeWidth(0)

point = vec.sum(center, vec.fromPolar(min(width, height)/padding, startTheta))

minRadius = vec.magnitude(vec.diff(point, center))
# distance to furthest corner
x, y = center
maxRadius = vec.magnitude((max(x, width-x), min(y, height-y)))
radius = minRadius

x, y = vec.diff(point, center)
theta = math.atan2(y, x) - edgeAngle

debugLine = []

while radius < maxRadius:
    t = ((radius - minRadius) / (maxRadius - minRadius))**blendExponent

    debugLine.append(point)

    vertices = [point]
    vertices.append(vec.sum(point, vec.fromPolar(2*maxRadius, theta)))

    theta += edgeAngle

    vertices.append(vec.sum(point, vec.fromPolar(2*maxRadius, theta)))

    x, y = vec.diff(point, center)
    padAngle = theta+math.pi/2
    spiralAngle = math.atan2(y, x) + math.pi/2

    pointDelta = vec.fromPolar(padding/math.cos(padAngle-spiralAngle), spiralAngle)

    point = vec.sum(point, pointDelta)
    radius = vec.magnitude(vec.diff(point, center))

    #point = vec.sum(point, vec.fromPolar(0.2*(maxRadius - vec.magnitude(vec.diff(point, center))), theta))
    #point = vec.sum(point, vec.fromPolar(padding, theta+math.pi/2))

    r, g, b = colors.mixColors(startColor, endColor, t)
    doc.setFillColor(r, g, b)

    doc.addPolygon(vertices)
if debug:
    doc.setStrokeWidth(5)
    doc.setStrokeColor(255, 255, 255)
    doc.setFillOpacity(0)

    doc.addPolyLine(debugLine)

    doc.setStrokeWidth(0)
    doc.setFillColor(255, 0, 0)
    doc.setFillOpacity(1.0)

    for p in debugLine:
        doc.addCircle(p, 5)

    doc.setStrokeColor(0,0,0)
    doc.setStrokeWidth(1)
    for i in range(len(debugLine)-1):
        doc.addLine((0, i), (vec.magnitude(vec.diff(debugLine[i], center)), i))
        doc.addLine(center, debugLine[i])

    doc.setFillColor(0, 255, 0)
    doc.addCircle(center, 10)

doc.write("shards.svg")
