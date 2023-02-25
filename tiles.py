import math
from SVGDocument import SVGDocument as svg
from SVGDocument import SVGPath
import vector2D as vec
import colors

tileSize = 400.0

width = tileSize * 10
height = tileSize * 10

strokeWidth = tileSize / 20.0

# tuples of the form (vector, color)
debugPoints = []
debugPointSize = 5.0
showDebugPoints = True
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

fillBackground = True
background = black

doc = svg(width, height)

def addDebugPoint(point, color):
    global debugPoints
    debugPoints += [(point, color)]

def midpoint(u, v, t=0.5):
    (ux, uy) = u
    (vx, vy) = v

    return (
        (1 - t) * ux + t * vx,
        (1 - t) * uy + t * vy
    )

def tilePaths(offset, \
        tileSize=tileSize, \
        eccentricity=0.5, \
        widths=[1.0], \
        cross=True, \
        debug=False):
    (offsetX, offsetY) = offset

    tileUnit = tileSize / 4

    cornerA = (offsetX           , offsetY)
    cornerB = (offsetX + tileSize, offsetY)
    cornerC = (offsetX           , offsetY + tileSize)
    cornerD = (offsetX + tileSize, offsetY + tileSize)

    center = midpoint(cornerA, cornerD)

    # corners in clockwise order
    cwCorners = [
        cornerA,
        cornerB,
        cornerD,
        cornerC
    ]

    paths = []

    for i in range(len(cwCorners)):
        corner = cwCorners[i]
        nextCorner = cwCorners[(i+1)%len(cwCorners)]
        prevCorner = cwCorners[(i-1)%len(cwCorners)]

        flip = i%2 == 1

        if debug:
            addDebugPoint(corner, red)
            addDebugPoint(midpoint(corner, nextCorner), green)

        for width in widths:
            curve = curveInsideRect(
                midpoint(nextCorner, corner, 0.5 + width/2),
                center,
                eccentricity,
                flip=flip
            )
            crossCurve = curveInsideRect(
                midpoint(corner, prevCorner, width/2),
                midpoint(corner, nextCorner),
                eccentricity,
                flip=not flip
            )

            paths += [curve]
            if cross:
                paths += [crossCurve]

    return paths

def curveInsideRect(cornerA, cornerD, eccentricity=0.5, flip=False):
    # if the coners of the bounding box are oriented as:
    # A B
    # C D
    # Then only corners A and D are needed to specify the box.  However, we
    # still want to compute corners B and C to place the anchor points.

    (ax, ay) = cornerA
    (dx, dy) = cornerD

    cornerB = (dx, ay)
    cornerC = (ax, dy)

    beginAnchor = None
    endAnchor = None
    if flip:
        beginAnchor = midpoint(cornerA, cornerB, eccentricity)
        endAnchor = midpoint(cornerD, cornerC, eccentricity)
    else:
        beginAnchor = midpoint(cornerA, cornerC, eccentricity)
        endAnchor = midpoint(cornerD, cornerB, eccentricity)

    path = SVGPath()

    path.moveTo(cornerA)
    path.cubicBezier(
        beginAnchor,
        endAnchor,
        cornerD
    )

    return path

doc.setFillColor(*background)
if fillBackground:
    doc.addRect((0, 0), width, height)

rows = int(height / tileSize)
columns = int(width / tileSize)

doc.setStrokeWidth(strokeWidth)
doc.setFillOpacity(0.0)

widthCount = 25
curveWidths = [2.0 * x/widthCount  for x in range(widthCount)]

print(curveWidths)

for curveWidth in curveWidths:
    opacity = (1.0 - math.fabs(1.0 - curveWidth))
    stroke = 1.0 - opacity
    eccentricity = opacity
    doc.setStrokeWidth(stroke * strokeWidth)
    doc.setStrokeOpacity(opacity)
    doc.setStrokeColor(*colors.mixColors(blue, white, opacity))
    for col in range(-1, columns+1):
        for row in range(-1, rows+1):
            tilePosition = (tileSize * col, tileSize * row)
            tileCenter = vec.sum(tilePosition, (tileSize/2, tileSize/2))
            center = (width/2, height/2)
            # colorTheta = 2 * math.pi * vec.distance(tileCenter, center) / vec.magnitude(center)
            colorTheta = 0
            colorThetaOffset = 2 * math.pi * opacity
            for path in tilePaths(tilePosition, eccentricity=eccentricity, widths=[curveWidth], cross=True, debug=False):
                doc.addSVGPath(path, fill=False)

if showDebugPoints:
    for (vector, color) in debugPoints:
        doc.setStrokeOpacity(0.0)
        doc.setFillColor(*color)
        doc.setFillOpacity(1.0)
        doc.addCircle(vector, debugPointSize)

doc.write("tiles.svg")
