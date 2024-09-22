import colors
import math
import random as rng
import vector2D as vec
import whirl_helpers as helpers
import whirl_symmetry_effects as symmetryEffects
from SVGDocument import SVGDocument as svg
from SVGDocument import SVGPath

debug = False
debugPoints = []

width = 3840.0
height = 3840.0

startTheta = 0

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
minTileStrokes = 1
print("minTileStrokes", minTileStrokes)
maxTileStrokes = 6
print("maxTileStrokes", maxTileStrokes)
globalEccentricity = 1.0

(tileEffectName, tileEffect) = helpers.tileEffect
print("Tile effect:", tileEffectName)

(symmetryName, symmetryEffect) = helpers.symmetryEffect
symmetryDegree = rng.randint(1, 10)
print("Symmetry effect: {}({})".format(symmetryName, symmetryDegree))

def addDebugPoint(point, color=red):
    debugPoints.append((point, color))

def ortho(vec):
    (x, y) = vec

    return (-1 * y, x)

def interpolate(x, y, t):
    return (1 - t) * x + t * y

# Scale a vector within [-1, -1], [1, 1] to the rectangle of the screen
def scaleAndCenter(v):
    return vec.sum(vec.scale(maxRadius, v), center)

def tileCornersBC(cornerA, cornerD, eccentricity):
    return tileEffect(cornerA, cornerD, eccentricity)

(tEffectName, tEffect) = helpers.tEffect
print("t effect:", tEffectName)

def tilePoints(cornerA, cornerD, strokeCount, eccentricity=1.0):
    tileCenter = vec.midpoint(cornerA, cornerD)
    (cornerB, cornerC) = tileCornersBC(cornerA, cornerD, eccentricity)

    pathQuadruples = []

    for n in range(strokeCount):
        eccentricityScale = tEffect((n + 1) / strokeCount)

        (controlA, controlB) = tileCornersBC(cornerA, cornerD, eccentricityScale)

        if n % 2 == 0:
            pathQuadruples.append((cornerA, controlA, controlB, cornerD))
        else:
            pathQuadruples.append((cornerD, controlB, controlA, cornerA))

    return pathQuadruples

def pathEnd(pathQuadruples):
    # last point of last curve segment
    return pathQuadruples[len(pathQuadruples) - 1][3]

halfPathEndpoints = []

for i in range(int(intersectionPoints * 2)):
    x = rng.uniform(-1.0, 1.0)
    y = rng.uniform(-1.0, 1.0)
    halfPathEndpoints.append((x, y))

tilePaths = []

for i in range(0, len(halfPathEndpoints), 2):
    cornerA = halfPathEndpoints[i]
    cornerD = halfPathEndpoints[i+1]
    strokes = 2 * rng.randint(
        math.ceil(minTileStrokes / 2),
        math.floor(maxTileStrokes / 2)
    )

    eccentricity = rng.random() * globalEccentricity

    baseTile = tilePoints(cornerA, cornerD, strokes, eccentricity=eccentricity)

    tilePaths += symmetryEffects.applySymmetry(baseTile, symmetryEffect, symmetryDegree)

# Transcribe each tile into a curve object
curve = SVGPath()

for (start, controlA, controlB, end) in tilePaths:
    start = scaleAndCenter(start)
    controlA = scaleAndCenter(controlA)
    controlB = scaleAndCenter(controlB)
    end = scaleAndCenter(end)

    curve.moveTo(start)
    addDebugPoint([start, end], red)
    (halfCornerB, halfCornerC) = tileCornersBC(start, end, 0.5)
    (cornerB, cornerC) = tileCornersBC(start, end, 1.0)
    addDebugPoint(vec.midpoint(start, end))
    addDebugPoint([controlA, controlB], green)
    addDebugPoint([halfCornerB, cornerB], blue)
    addDebugPoint([halfCornerC, cornerC], blue)

    curve.cubicBezier(controlA, controlB, end)
    curve.moveTo((0.0, 0.0))

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
