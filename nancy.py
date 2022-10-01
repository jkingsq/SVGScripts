import math
from SVGDocument import SVGDocument as svg
from SVGDocument import SVGPath
import vector2D as vec
import colors

width = 800.0
height = 800.0

background = (192, 0, 0)
foreground = (255, 255, 255)

center = (width/2, height/2)

doc = svg(width, height)

thetas = 12
radii = 6

maxRadius = vec.scale(2/3, vec.magnitude((width, height)))

def ring(radius, path):
    for i in range(thetas):
        
