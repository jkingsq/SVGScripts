import math
from SVGDocument import SVGDocument as svg
import vector2D as vec
import colors

debug = False

width = 1920.0
height = 1080.0

foreground = (255, 255, 255)
background = (0, 0, 0)

center = (width/2, height/2)

padding = max(width, height)/1000.0

doc = svg(width, height)

startThetas = 3
thetas = startThetas
pencilWidth = padding / 2
globalThetaOffset = math.pi/2

x, y = center
maxRadius = vec.magnitude((max(x, width-x), min(y, height-y)))

radius = (padding) / math.sin(math.pi*2 / thetas)

def pencil(point, angle):
    radius = vec.distance(center, point)
    heading = vec.normalize(vec.diff(point, center))
    x, y = heading
    theta = math.atan2(y, x)
    side = (math.cos(theta+math.pi/2), math.sin(theta+math.pi/2))
    side = vec.scale(pencilWidth/2, side)

    taperedLength = (pencilWidth/2) / math.sin(angle/2)

    rightCorner = vec.sum(\
        vec.fromPolar(taperedLength, theta + angle/2),\
        point)

    leftCorner = vec.sum(\
        vec.fromPolar(taperedLength, theta - angle/2),\
        point)

    farRightCorner = vec.sum(\
        rightCorner,\
        vec.scale(maxRadius, heading))

    farLeftCorner = vec.sum(\
        leftCorner,\
        vec.scale(maxRadius, heading))

    # Draw the shape at this point
    doc.addPolygon([point, rightCorner, farRightCorner, farLeftCorner,\
        leftCorner])
    #doc.addPolygon([point, rightCorner, leftCorner])

def pencilRing(n, r, first=False):
    taperAngle = 2 * math.pi / n
    thetaOffset = globalThetaOffset
    if not first:
        thetaOffset += taperAngle / 2

    for i in range(n):
        theta = 2*math.pi * i / n + thetaOffset
        point = vec.sum(\
            center,\
            vec.fromPolar(r, theta))
        doc.setFillColor(\
            255.0 * (math.sin(theta)+1)/2,\
            255.0 * (math.sin(theta + 2*math.pi/3)+1)/2,\
            255.0 * (math.sin(theta + 4*math.pi/3)+1)/2)

        pencil(point, 2*math.pi / n)

    if debug:
        doc.setStrokeWidth(padding)
        doc.setStrokeColor(255, 0, 0)
        doc.addLine(center, vec.sum(center, vec.fromPolar(maxRadius, thetaOffset)))
        doc.setStrokeWidth(0)

doc.setStrokeWidth(0)

r, g, b = background
doc.setFillColor(r, g, b)
doc.addRect((0,0), width, height)

r, g, b = foreground
doc.setFillColor(r, g, b)

pencilRing(thetas, radius, first=True)
#for i in range(startThetas):
#    taperAngle = 2*math.pi / thetas
#    point = vec.sum(\
#        center,\
#        vec.fromPolar(radius, 2*math.pi * i / startThetas))
#    pencil(point, 2*math.pi / startThetas)
radius += (padding + pencilWidth/2) / math.sin(math.pi/thetas)

while radius < maxRadius:
    pencilRing(thetas, radius)
    taperAngle = 2*math.pi / thetas
    radius += (padding + pencilWidth/2) / math.sin(taperAngle/2)
    thetas *= 2

doc.write("pencils.svg")
