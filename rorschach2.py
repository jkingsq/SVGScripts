import math
from SVGDocument import SVGDocument as svg
import vector2D as vec
import colors
import random as rng

width = 400.0
height = 400.0

debug = False

startTheta=rng.uniform(0, math.pi*2)

symmetryAxes = 13

background = (32, 32, 32)

doc = svg(width, height)

center = (width/2, height/2)

maxRadius = min(width, height) / 2

maxComponent = math.sqrt((maxRadius**2)/2)

points = 4
vertices = []
pattern =[]

for i in range(points):
    t = i / float(points)
    r = rng.uniform(0, maxRadius)
    theta = i * 2.0 * math.pi / points
    pattern.append((r, theta))

for i in range(symmetryAxes):
    offset = i * 2.0 * math.pi / symmetryAxes + startTheta
    for r, theta in pattern:
        vertices.append(vec.sum(center, vec.fromPolar(r, offset + theta/symmetryAxes)))
    pattern.reverse()

r, g, b = background
doc.setFillColor(r, g, b)

doc.addRect((0, 0),  width, height)

r, g, b = colors.colorCycle(rng.uniform(0, 2*math.pi))
doc.setStrokeWidth(0)
doc.setFillColor(r, g, b)
doc.addPolygon(vertices)

doc.write("rorschach2.svg")
