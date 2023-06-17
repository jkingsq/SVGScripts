import math
from SVGDocument import SVGDocument as svg
from SVGDocument import SVGPath
import vector2D as vec
import colors

width = 1000
height = 600

doc = svg(width, height)
background = (0, 0, 0)

fillMode = 'gradient'

beginFillColor = (0, 0, 0)
endFillColor = (128, 255, 255)

strokes = 10
layers = 50

debug = False

def tile(cornerA, cornerD, strokeCount, transverseScale=1.0):
    (ax, ay) = cornerA
    (dx, dy) = cornerD

    center = vec.midpoint(cornerA, cornerD)

    cornerB = vec.midpoint(center, (dx, ay), transverseScale)
    cornerC = vec.midpoint(center, (ax, dy), transverseScale)

    tValues = [x/strokeCount for x in range(strokeCount)]

    # tValues = tValues + [2 * t for t in tValues]

    # tValues = [-1 * t for t in tValues] + tValues

    path = SVGPath()

    for t in tValues:
        beginAnchor = vec.midpoint(cornerB, cornerD, t)
        endAnchor = vec.midpoint(cornerC, cornerA, 1.0 - t)

        path.moveTo(cornerA)
        path.cubicBezier(
            beginAnchor,
            endAnchor,
            cornerD
        )

        path.cubicBezier(
            beginAnchor,
            endAnchor,
            cornerA
        )

    return path

viewportTile = ((0, 0), (width, height), strokes)

if debug:
    path = tile(*viewportTile)

    doc.setFillOpacity(0.0)
    doc.setStrokeOpacity(1.0)
    doc.setStrokeWidth(1)

    doc.addSVGPath(path, fill=False)
else:
    doc.setFillColor(*background)
    doc.setFillOpacity(1.0)
    doc.setStrokeOpacity(0.0)
    doc.addRect((0, 0), width, height)

    doc.setStrokeWidth(0.0)

    tValues = [layer / layers for layer in range(layers)]

    for t in reversed(tValues):
        colorT = 1.0 - (1.0-t)**8
        color = (255, 255, 255)

        if fillMode == 'wheel':
            colorTheta = 2 * math.pi * colorT
            color = colors.colorCycle(colorTheta)
        elif fillMode == 'gradient':
            color = colors.mixColors(beginFillColor, endFillColor, colorT)

        doc.setFillColor(*color)
        path = tile(*viewportTile, transverseScale = 1.0 - t)
        doc.addSVGPath(path, fill=True)

doc.write("taper.svg")
