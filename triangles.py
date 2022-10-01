import math
from SVGDocument import SVGDocument as svg

width = 1920.0
height = 1080.0
doc = svg(width, height)

totalRotation = 9.5 * math.pi

triangles = 400
sides = 3

def mixColors(colorA, colorB, t):
    aR, aG, aB = colorA
    bR, bG, bB = colorB
    r = math.sqrt((1.0-t)*(aR**2) + t*(bR**2))
    g = math.sqrt((1.0-t)*(aG**2) + t*(bG**2))
    b = math.sqrt((1.0-t)*(aB**2) + t*(bB**2))
    return (r, g, b)

def regularPolygon(center, vertices, radius, rotation):
    centerX, centerY = center
    result = []
    for i in range(vertices):
        theta = 2 * math.pi * i / vertices + rotation
        x = centerX + radius*math.cos(theta)
        y = centerY + radius*math.sin(theta)
        result.append((x,y))
    return result

xStart = 0
yStart = height
xEnd = width * 2/3
yEnd = height * 1/3
startColor = (63, 63, 63)
endColor = (105, 135, 105)
doc.setFillColor(63, 63, 63)


doc.setStrokeWidth(2)

for i in range(triangles):
    t = (i+1) / triangles
    r, g, b = mixColors(startColor, endColor, t)
    doc.setStrokeColor(r, g, b)
    x = (1.0-t)*xStart + t*xEnd
    y = (1.0 - t**2)*yStart + (t**2)*yEnd
    center = (x, y)
    radius = max(width, height) / (t * 10.0)
    rotation = t * totalRotation
    coords = regularPolygon(center, sides, radius, rotation)
    doc.addPolygon(coords)

doc.write("triangles.svg")
