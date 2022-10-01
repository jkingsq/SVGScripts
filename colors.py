import math

def mixColors(colorA, colorB, t):
    aR, aG, aB = colorA
    bR, bG, bB = colorB
    r = math.sqrt((1.0-t)*(aR**2) + t*(bR**2))
    g = math.sqrt((1.0-t)*(aG**2) + t*(bG**2))
    b = math.sqrt((1.0-t)*(aB**2) + t*(bB**2))
    return (r, g, b)

def colorCycle(theta):
    r = 255.0 * (math.sin(theta)+1)/2
    g = 255.0 * (math.sin(theta + 2*math.pi/3)+1)/2
    b = 255.0 * (math.sin(theta + 4*math.pi/3)+1)/2
    return (r, g, b)
