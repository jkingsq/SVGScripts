import math
from SVGDocument import SVGDocument as svg
import vector2D as vec
import colors
import random as rng

width = 3840.0
height = 3840.0

debug = False

startTheta = 0
symmetryAxes = int(rng.uniform(1, 16))

background = (16, 16, 16)

doc = svg(width, height)

center = (width/2, height/2)

maxRadius = max(width, height) / 2
maxComponent = math.sqrt((maxRadius**2)/2)

points = int(rng.uniform(10, 225))
vertices = []
pattern = []

for i in range(int(points/symmetryAxes)):
    pattern.append((rng.uniform(-1*maxComponent, maxComponent),
                    rng.uniform(-1*maxComponent, maxComponent)))

n = len(pattern)

for i in range(n):
    x, y  = pattern[n - 1 - i]
    pattern.append((x * -1, y))

for i in range(symmetryAxes):
    theta = startTheta + i*2*math.pi/symmetryAxes
    u = vec.fromPolar(1.0, theta)
    v = vec.fromPolar(1.0, theta + math.pi/2)
    for x, y in pattern:
        vertices.append(vec.sum(vec.sum(
            center,
            vec.scale(x, u)),
            vec.scale(y, v)))

r, g, b = background
doc.setFillColor(r, g, b)

doc.addRect((0, 0), width, height)

if debug:
    doc.setStrokeWidth(maxComponent/250)
    doc.setStrokeColor(128, 128, 128)
    for i in range(symmetryAxes):
        theta = startTheta + i*2*math.pi/symmetryAxes
        v = vec.fromPolar(maxRadius, theta)
        start = vec.sum(center, v)
        end = vec.sum(center, vec.scale(-1.0, v))
        doc.addLine(start, end)

doc.setStrokeWidth(0)

r, g, b = colors.colorCycle(rng.uniform(0, 2*math.pi))
doc.setFillColor(r, g, b)
doc.addPolygon(*vertices)

doc.write("rorschach.svg")
