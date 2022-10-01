import math
from SVGDocument import SVGDocument as svg

width = 1920.0
height = 1080.0
doc = svg(width, height)

bgcircles = 200
xStart = 0
yStart = height
xEnd = width * 2/3
yEnd = height * 1/3
sizeEnd = 40

for i in range(bgcircles):
    t = (i+1) / bgcircles
    x = (1.0-t)*xStart + t*xEnd
    y = (1.0-t)*yStart + t*yEnd
    center = (x, y)
    radius = sizeEnd / t
    doc.setStrokeWidth(radius/40)
    brightness = 32 + t*(255-32)
    doc.setFillColor(brightness, brightness, brightness)
    doc.addCircle(center, radius)

doc.write("ripples.svg")
