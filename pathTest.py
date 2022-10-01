import math
from SVGDocument import SVGDocument as svg
from SVGDocument import SVGPath
import vector2D as vec
import colors

width = 1920.0
height = 1080.0

doc = svg(width, height)

background = (0, 0, 0)

r, g, b = background
doc.setFillColor(r, g, b)
doc.addRect((0, 0), width, height)

path = SVGPath()

n = 21

step = width / n
maxMagnitude = height

path.moveTo((width/n / 2.0, height/2.0))
path.quadraticBezierRelative((step/2.0, 0), (step, 0))
for i in range(n-2):
    scale = -0.5*math.cos(2*math.pi / (n-2) * (i + 1)) + 0.5
    if i % 2 == 1:
        scale *= -1
    path.quadraticBezierRelative((step/2, scale*maxMagnitude), (step, 0))

doc.setStrokeColor(255, 255, 255)
doc.setFillColor(255, 0, 0)
doc.setStrokeWidth(maxMagnitude/100)
doc.addSVGPath(path, fill=True)

doc.write("pathTest.svg")
