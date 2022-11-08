import math
import random as rng
from SVGDocument import SVGDocument as svg
import vector2D as vec
import colors

width = 2000.0
height = 2000.0

center = vec.scale(1/2, (width, height))

background = (16, 16, 16)

patterns = ["random", "star"]
pattern = "random"

minProportion = 1/25

crosslines = 11

minR = 75/2
maxR = 500

starPoints = 10
starMinR = 1/2
starMaxR = 1.0
if pattern == "random":
    rings = 3
elif pattern == "star":
    rings = int(starPoints - starPoints * (starMinR ** 2))

print((starPoints, rings))

crosslineWidth = 5

def drawParallelogram(doc, parallelogram, maxT=1.0):
    (point, u, v) = parallelogram

    outlinePoints = [
        point,
        vec.sum(point, u),
        vec.sum(point, vec.sum(u, v)),
        vec.sum(point, v)
    ]

    shortSide = vec.shorter(u, v)
    longSide = vec.longer(u, v)

    luminance = vec.magnitude(shortSide) / vec.magnitude(longSide)

    (sheenR, sheenG, sheenB) = \
        colors.colorCycle(math.atan2(*vec.sum(u, v)))

    sheen = (sheenR, sheenG, sheenB)

    doc.setStrokeOpacity(1.0)
    doc.setFillOpacity(1.0)

    doc.setFillColor(*background)

    # outlines off
    doc.setStrokeOpacity(0.0)

    doc.setStrokeColor(255, 255, 255)

    doc.addPolygon(outlinePoints)

    doc.setStrokeOpacity(1.0)

    doc.setStrokeColor(255, 255, 255)

    colorThetaOffset = rng.random() * 2 * math.pi

    for i in range(1, int((crosslines+1)*maxT)):
        drawCrossline(doc, parallelogram, i/(crosslines+1), colorThetaOffset)

def drawCrossline(doc, parallelogram, t, colorThetaOffset):
    (point, u, v) = parallelogram

    crossline = None
    if t <= 0.5:
        crossline = [
            vec.sum(point, vec.scale(t*2, u)),
            vec.sum(point, vec.scale(t*2, v))
        ]
    else:
        oppPoint = vec.sum(point, vec.sum(u, v))
        crossline = [
            vec.sum(oppPoint, vec.scale(-(1-t)*2, u)),
            vec.sum(oppPoint, vec.scale(-(1-t)*2, v))
        ]

    colorTheta = vec.magnitude(vec.diff(
        point,
        vec.scale(1/2, vec.sum(crossline[0], crossline[1]))
    )) / (2*maxR) + colorThetaOffset

    doc.setStrokeColor(*colors.colorCycle(colorTheta * 2 * math.pi))

    doc.setStrokeWidth(crosslineWidth)

    doc.addLine(*crossline)

def drawDebugPoint(doc, point):
    doc.setFillColor(255, 0, 0)
    doc.addCircle(point, 5)

def placementBonus(parallelogram):
    (point, _, _) = parallelogram
    (x, y) = vec.diff(point, center)
    theta = (math.sin(math.atan2(x, y)) + 1) / 2

def screenProportion(parallelogram):
    (_, u, v) = parallelogram

    screenArea = width * height
    plgArea = vec.magnitude(u) * vec.magnitude(v)
    return plgArea / screenArea

def subdivide(parallelogram):
    probability = placementBonus(parallelogram) * screenProportion(parallelogram)
    return rng.random() > probability

def extendToX(point, vector, x):
    (pointX, _) = point
    translatedX = x - pointX
    (vectorX, _) = vector
    return vec.scale(translatedX / pointX, vector)

def extendToY(point, vector, y):
    (_, pointY) = point
    translatedY = y - pointY
    (_, vectorY) = vector
    return vec.scale(translatedY / pointY, vector)

def extendToBoundary(offset, vector):
    (offsetX, offsetY) = offset
    (vX, vY) = vector

    scaleHoriz = math.inf
    if vX > 0:
        scaleHoriz = (width - offsetX) / vX
    elif vX < 0:
        scaleHoriz = -offsetX / vX

    scaleVert = math.inf
    if vY > 0:
        scaleVert = (height - offsetY) / vY
    elif vY < 0:
        scaleVert = -offsetY / vY

    return vec.shorter(
        vec.scale(scaleHoriz, vector),
        vec.scale(scaleVert, vector)
    )

doc = svg(width, height)

r, g, b = background
doc.setFillColor(r, g, b)
doc.addRect((0, 0), width, height)

# Picks a random point, then adds parallelograms surrounding that point, each
# with two vertices along the image's border.
def spiderweb(doc):
    basePoint = (rng.uniform(0, width), rng.uniform(0, height))

    offsetTheta = rng.uniform(0, 2 * math.pi)
    theta = 0
    thetaMinDelta = math.pi / 6
    thetaMaxDelta = math.pi / 2

    baseParallelograms = []

    while theta < 2 * math.pi:
        edgeA = extendToBoundary(basePoint, vec.fromPolar(1, theta + offsetTheta))
        theta += rng.uniform(thetaMinDelta, thetaMaxDelta)
        if theta > 2 * math.pi - thetaMinDelta:
            theta = 2 * math.pi

        edgeB = extendToBoundary(basePoint, vec.fromPolar(1, theta + offsetTheta))

        baseParallelograms.append((basePoint, edgeA, edgeB))

    for parallelogram in baseParallelograms:
        drawParallelogram(doc, parallelogram)

def initialRing(ringCenter):
    if pattern == "random":
        return randomRing(ringCenter)
    elif pattern == "star":
        return starRing(ringCenter)

def starRing(ringCenter, points=starPoints):
    parallelograms = []

    offsetTheta = - math.pi / points / 2 + (math.pi / 4)

    for i in range(points*2):
        prevTheta = (i-1) * math.pi / points + offsetTheta
        theta = i * math.pi / points + offsetTheta

        prevR = 0
        r = 0
        if i % 2 == 0:
            prevR, r = starMinR, starMaxR
        else:
            prevR, r = starMaxR, starMinR

        prevEdge = vec.fromPolar(prevR, prevTheta + offsetTheta)
        edge = vec.fromPolar(r, theta + offsetTheta)

        parallelograms.append((ringCenter, prevEdge, edge))

    return parallelograms

def randomRing(ringCenter):
    offsetTheta = rng.uniform(0, 2 * math.pi)
    theta = 0
    thetaMinDelta = math.pi / 6
    thetaMaxDelta = math.pi / 2 - thetaMinDelta

    parallelograms = []

    r = rng.uniform(minR, maxR)
    edge = vec.fromPolar(r, offsetTheta)
    firstEdge = edge

    while theta < 2 * math.pi:
        prevEdge = edge

        theta += rng.uniform(thetaMinDelta, thetaMaxDelta)
        if theta > 2 * math.pi - thetaMinDelta:
            theta = 2 * math.pi

        r = rng.uniform(minR, maxR)
        edge = vec.fromPolar(r, theta + offsetTheta)

        if theta == 2 * math.pi:
            edge = firstEdge

        parallelograms.append((ringCenter, prevEdge, edge))

    return parallelograms

def awayFromCenter(parallelogram, ringCenter):
    (nearPoint, edgeA, edgeB) = parallelogram

    farPoint = vec.sum(nearPoint, vec.sum(edgeA, edgeB))

    nearDist = vec.magnitude(vec.diff(nearPoint, ringCenter))
    farDist = vec.magnitude(vec.diff(farPoint, ringCenter))

    return farDist > nearDist

def isConcave(parallelogramA, parallelogramB):
    (pointA, edgeAA, edgeAB) = parallelogramA
    (pointB, edgeBA, edgeBB) = parallelogramB

    commonPoint = vec.sum(pointA, edgeAB)
    altCommonPoint = vec.sum(pointB, edgeBA)

    innerMidpoint = vec.scale(1/2, vec.sum(pointA, pointB))

    outerPointA = vec.sum(pointA, vec.sum(edgeAA, edgeAB))
    outerPointB = vec.sum(pointB, vec.sum(edgeBA, edgeBB))

    outerMidpoint = vec.scale(1/2, vec.sum(outerPointA, outerPointB))

    # doc.setStrokeColor(255, 0, 255)
    # doc.addLine(commonPoint, innerMidpoint)
    # doc.setStrokeColor(0, 255, 0)
    # doc.addLine(commonPoint, outerMidpoint)

    innerDirection = vec.diff(innerMidpoint, commonPoint)
    outerDirection = vec.diff(outerMidpoint, commonPoint)

    return vec.dot(innerDirection, outerDirection) < 0

def outerRing(ringCenter, innerRing):
    if len(innerRing) <= 1:
        return []

    parallelograms = []
    convexEdgeR = rng.uniform(minR, maxR)

    for i in range(len(innerRing)):
        parallelogramA = innerRing[i]
        parallelogramB = innerRing[(i+1) % len(innerRing)]

        (innerPoint, edgeA, pointOffset) = parallelogramA
        (innerPointB, _, edgeB) = parallelogramB

        point = vec.sum(innerPoint, pointOffset)

        if isConcave(parallelogramA, parallelogramB):
            parallelograms.append((point, edgeA, edgeB))
        else:
            print("convex")
            middleEdge = vec.scale(-1, vec.diff(vec.scale(1/2, vec.sum(innerPoint, innerPointB)), point))
            # parallelograms.append((point, edgeA, middleEdge))
            # parallelograms.append((point, edgeB, middleEdge))
            # drawDebugPoint(doc, point)

    return parallelograms

def isOutermost(ring):
    result = true
    for (innerPoint, edge, _) in ring:
        point = vec.sum(innerPoint, edge)
        result = result and vec.insideAABB(point, (0, 0), (width, height))

    return result

def positionParallelogram(parallelogram, translateBefore, scale, translateAfter):
    (point, u, v) = parallelogram

    point = vec.sum(
        vec.scale(
            scale,
            vec.sum(
                point,
                translateBefore
            )
        ),
        translateAfter
    )
    u = vec.scale(scale, u)
    v = vec.scale(scale, v)

    return (point, u, v)

innerRing = initialRing(center)

innerRings = initialRing(center)
ring = innerRings
for i in range(rings - 2):
    ring = outerRing(center, ring)
    innerRings += ring

outermostRing = outerRing(center, ring)

(centerX, centerY) = center

minX = math.inf
minY = math.inf
for (point, u, v) in innerRings:
    (x, y) = vec.sum(point, vec.sum(u, v))
    minX = min(minX, x)
    minY = min(minY, y)

maxX = 0
maxY = 0
for (point, u, v) in innerRings:
    (x, y) = vec.sum(point, vec.sum(u, v))
    maxX = max(maxX, x-minX)
    maxY = max(maxY, y-minY)

scale = min(width/maxX, height/maxY)

scaledFigureCenter = vec.scale(scale/2, vec.diff(
    (maxX, maxY),
    (minX, minY)
))

centerAdjustment = (0.0, 0.0)
if maxX > maxY:
    (_, bias) = scaledFigureCenter
    centerAdjustment = (0.0, centerY - bias)
elif maxY > maxX:
    (bias, _) = scaledFigureCenter
    centerAdjustment = (centerX - bias, 0.0)

offsetBefore = vec.scale(-1, (minX, minY))
offsetAfter = vec.scale(
    1/2,
    vec.diff((width, height), (maxX*scale, maxY*scale))
)

for parallelogram in innerRings:
    parallelogram = positionParallelogram(
        parallelogram,
        offsetBefore,
        scale,
        offsetAfter
    )
    drawParallelogram(doc, parallelogram)

for parallelogram in outermostRing:
    parallelogram = positionParallelogram(
        parallelogram,
        offsetBefore,
        scale,
        offsetAfter
    )
    drawParallelogram(doc, parallelogram, maxT=0.5)

doc.setStrokeColor(255, 0, 0)
doc.setFillOpacity(0.0)
# doc.addRect((minX, minY), maxX, maxY)

doc.setStrokeColor(0, 255, 255)
# doc.addRect((0, 0), maxX * scale, maxY * scale)

doc.write("grid_subdivide.svg")
