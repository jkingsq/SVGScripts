from SVGDocument import SVGDocument as svg
import vector2D as vec
import colors

width = 1920.0
height = 1080.0

patternWidth = min(width, height)
patternHeight = patternWidth
offset = (width - patternWidth, height-patternHeight)

bits = 8

debug = True

startColor = (0, 0, 0)
endColor = (255, 255, 255)
rows = 2**bits
maxBlend = rows-1
blend = lambda x : colors.mixColors(startColor, endColor, float(x)/maxBlend)

doc = svg(width, height)
doc.setStrokeWidth(0)

r, g, b = startColor
doc.setFillColor(r, g, b)
doc.addRect((0,0), width, height)

cornerX = lambda x : x * patternWidth/rows
cornerY = lambda y : y * patternHeight/rows
for x in range(rows):
    cellX = cornerX(x)
    cellWidth = cornerX(x+1) - cellX
    for y in range(rows):
        cellY = cornerY(y)
        cellHeight = cornerY(y+1) - cellY
        blendValue = int(x) & int(y)
        r, g, b = blend(blendValue)
        doc.setFillColor(r, g, b)
        cellCorner = vec.sum(offset, (cellX, cellY))
        doc.addRect(cellCorner, cellWidth, cellHeight)

if debug:
    print(blendValue)

doc.write("bitwiseGrid.svg")
