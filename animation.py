from SVGDocument import SVGDocument as svg
import colors
import math

width = 128
height = 128

frames = 60

for i in range(60):
    doc = svg(width, height)
    doc.setStrokeWidth(0)
    theta = i * 2 * math.pi / float(frames)
    r, g, b = colors.colorCycle(theta)
    doc.setFillColor(r, g, b)
    doc.addRect((0,0), width,height)
    doc.write("animation/animation{:04d}.svg".format(i))

