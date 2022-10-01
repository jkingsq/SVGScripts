import math
from SVGDocument import SVGDocument as svg
import vector2D as vec
import colors

width = 1920.0
height = 1080.0

center = (width/2.0, height/2.0)

doc = svg(width, height)

debug = True

background = (32, 32, 32)

r, g, b = background
doc.setFillColor(r, g, b)
doc.addRect((0, 0), width, height)

maxRadius = max(width,height)/2.0

#outerColor = (128, 0, 192)
outerColor = (48, 48, 48)
innerColor = (128, 128, 128)
def addEclipse(doc, center, outerR, innerR, v):
    doc.setStrokeWidth(0)
    doc.setFillColor(*outerColor)
    doc.addCircle(center, outerR)

    scaleBy = outerR - innerR
    innerCenter = vec.sum(vec.scale(scaleBy, v), center)

    doc.setFillColor(*innerColor)
    doc.addCircle(innerCenter, innerR)

spacing = max(width, height) / 40
columns = math.ceil(width / spacing)
rows = math.ceil(height / spacing)

# make sure numbers are odd so that circles fall along the center axes
columns += columns%2
rows += rows%2

patternWidth = spacing * columns
patternHeight = spacing * rows

outerRadius = spacing * 0.5
innerRadius = spacing * 0.25

for i in range(columns):
    tX = i/columns - 1/2
    for j in range(rows):
        tY = j/rows - 1/2
        cX, cY = center
        x = cX + tX * patternWidth
        y = cY + tY * patternHeight

        point = (x, y)
        v = vec.fromPolar(1.0, 4*math.pi*vec.magnitude(vec.diff(point, center))/maxRadius)

        addEclipse(doc, point, outerRadius, innerRadius, v)

doc.write("eclipses.svg")
