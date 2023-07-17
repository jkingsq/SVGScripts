import colors
import math
import random as rng
import vector2D as vec
from SVGDocument import SVGDocument as svg
from SVGDocument import SVGPath

debug = False
debugPoints = []

width = 3840.0
height = 3840.0

startTheta = 0
symmetryAxes = int(rng.uniform(1, 16))

background = (16, 16, 16)
foreground = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

doc = svg(width, height)

center = (width/2, height/2)

maxRadius = max(width, height) / 2
maxComponent = math.sqrt((maxRadius**2)/2)

intersectionPoints = int(rng.uniform(5, 10))
minTileStrokes = 3
maxTileStrokes = 6
globalEccentricity = 3.0

def addDebugPoint(point, color=red):
    debugPoints.append((point, color))

def ortho(vec):
    (x, y) = vec

    return (-1 * y, x)

def interpolate(x, y, t):
    return (1 - t) * x + t * y

def tileCornersBC(cornerA, cornerD, eccentricity):
    tileCenter = vec.midpoint(cornerA, cornerD)
    halfTransverse = ortho(vec.diff(cornerD, tileCenter))

    cornerB = vec.sum(tileCenter, vec.scale(eccentricity, halfTransverse))
    cornerC = vec.sum(tileCenter, vec.scale(-1 * eccentricity, halfTransverse))

    return (cornerB, cornerC)

def tilePoints(cornerA, cornerD, strokeCount, eccentricity=1.0):
    tileCenter = vec.midpoint(cornerA, cornerD)
    (cornerB, cornerC) = tileCornersBC(cornerA, cornerD, eccentricity)

    pathQuadruples = []

    for n in range(strokeCount):
        start, end = None, None
        maxControlA, maxControlB = None, None
        if n % 2 == 0:
            start, end = cornerA, cornerD
            maxControlA, maxControlB = cornerB, cornerC
        else:
            start, end = cornerD, cornerA
            maxControlA, maxControlB = cornerC, cornerB

        eccentricityScale = (n + 1) / strokeCount

        controlA = vec.midpoint(tileCenter, maxControlA, eccentricityScale)
        controlB = vec.midpoint(tileCenter, maxControlB, eccentricityScale)

        pathQuadruples.append((start, controlA, controlB, end))

    return pathQuadruples

def pathEnd(pathQuadruples):
    # last point of last curve segment
    return pathQuadruples[len(pathQuadruples) - 1][3]

halfPathEndpoints = []

for i in range(int(intersectionPoints)):
    x = rng.uniform(0, width)
    y = rng.uniform(0, height)
    halfPathEndpoints.append((x, y))

halfTilePaths = []

lastCurveEndpoint = halfPathEndpoints[0]
for i in range(len(halfPathEndpoints)):
    if i == 0:
        continue

    cornerA = lastCurveEndpoint
    cornerD = halfPathEndpoints[i]
    strokes = rng.randint(minTileStrokes, maxTileStrokes)

    eccentricity = rng.random() * globalEccentricity

    tile = tilePoints(cornerA, cornerD, strokes, eccentricity=eccentricity)

    halfTilePaths += tile

    lastCurveEndpoint = pathEnd(tile)

tilePaths = halfTilePaths.copy()

for (start, controlA, controlB, end) in halfTilePaths:
    tilePaths.append((
        vec.midpoint(center, start, -1.0),
        vec.midpoint(center, controlA, -1.0),
        vec.midpoint(center, controlB, -1.0),
        vec.midpoint(center, end, -1.0)
    ))

curve = SVGPath()

for (start, controlA, controlB, end) in tilePaths:
    curve.moveTo(start)
    addDebugPoint([start, end], red)
    (halfCornerB, halfCornerC) = tileCornersBC(start, end, 0.5)
    (cornerB, cornerC) = tileCornersBC(start, end, 1.0)
    addDebugPoint(vec.midpoint(start, end))
    addDebugPoint([controlA, controlB], green)
    addDebugPoint([halfCornerB, cornerB], blue)
    addDebugPoint([halfCornerC, cornerC], blue)

    curve.cubicBezier(controlA, controlB, end)

# fill background
doc.setFillColor(*background)
doc.setFillOpacity(1.0)
doc.setStrokeOpacity(0.0)
doc.addRect((0, 0), width, height)

# draw path
doc.setStrokeWidth(0.0)
doc.setFillColor(*foreground)
doc.addSVGPath(curve, fill=True)

if debug:
    radius = max(width, height) / 200
    strokeWidth = radius / 2

    for (point_or_line, color) in debugPoints:
        if type(point_or_line[0]) == type(0.0):
            doc.setFillOpacity(1.0)
            doc.setFillColor(*color)
            doc.addCircle(point_or_line, radius)
            print("debug point " + str(point_or_line))
        elif type(point_or_line[0]) == type(()):
            doc.setFillOpacity(1.0)
            doc.setStrokeOpacity(1.0)
            doc.setStrokeColor(*color)
            doc.setStrokeWidth(strokeWidth)
            doc.addPolyLine(*point_or_line)
            print("debug line " + str(point_or_line))
        else:
            raise(point_or_line)

doc.write("whirl.svg")
