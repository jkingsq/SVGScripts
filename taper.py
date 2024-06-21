import math
from SVGDocument import SVGDocument as svg
from SVGDocument import SVGPath
import vector2D as vec

width = 600
height = 600

doc = svg(width, height)
background = (255, 255, 255)
foreground = (0, 0, 0)

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

    # repeat final curve segment in reverse order

    return path

viewportTile = ((0, 0), (width, height), strokes)

if debug:
    path = tile(*viewportTile)

    # draw path
    doc.setFillOpacity(0.0)
    doc.setStrokeOpacity(1.0)
    doc.setStrokeWidth(1)
    doc.addSVGPath(path, fill=False)
else:
    # fill background
    doc.setFillColor(*background)
    doc.setFillOpacity(1.0)
    doc.setStrokeOpacity(0.0)
    doc.addRect((0, 0), width, height)

    # draw path
    doc.setStrokeWidth(0.0)
    doc.setFillColor(*foreground)
    path = tile(*viewportTile)
    doc.addSVGPath(path, fill=True)

doc.write("taper.svg")
