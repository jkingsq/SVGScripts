import math
from SVGDocument import SVGDocument as svg

width = 400.0
height = 400.0

points = 3.0

doc = svg(width, height)

center = (width/2, height/2)
outline = 15
interiorAngle = math.pi - math.pi*(points-2)/points
maxOutline = outline / math.cos(interiorAngle)
radius = min(width, height)/2 - maxOutline

vertices = []

startTheta = 3 * math.pi / 2

for i in range(int(points)):
    theta = startTheta + 4 * math.pi / points * i
    x, y = center
    x += radius * math.cos(theta)
    y += radius * math.sin(theta)
    vertices.append((x, y))
vertices.append(vertices[0])

doc.setFillOpacity(0.0)
doc.setStrokeWidth(outline)
doc.addPolygon(vertices)

topX, topY = vertices[0]

doc.setStrokeColor(255, 0, 0)
doc.setStrokeWidth(1)
doc.addLine(vertices[0], (topX, topY-maxOutline))

doc.setStrokeColor(0, 0, 255)
doc.addLine((topX, topY+maxOutline), vertices[0])

doc.write("pentagram.svg")
