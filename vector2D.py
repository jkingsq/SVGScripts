import math

def scale(s, v):
    x, y = v
    return (s*x, s*y)

def magnitude(v):
    x, y = v
    return math.sqrt(x**2 + y**2)

def normalize(v):
    return scale(1/magnitude(v), v)

def sum(u, v):
    uX, uY = u
    vX, vY = v
    return (uX+vX, uY+vY)

def diff(u, v):
    return sum(u, scale(-1, v))

def distance(u, v):
    return magnitude(diff(u, v))

def dot(u, v):
    uX, uY = u
    vX, vY = v
    return uX*vX + uY*vY

def equal(u, v):
    uX, uY = u
    vX, vY = v
    return uX == vX and uY == vY

def fromPolar(r, theta):
    return (r*math.cos(theta), r*math.sin(theta))

# project u onto v
def project(u, v):
    return scale(dot(u, normalize(v)), v)

def shorter(u, v):
    if magnitude(u) > magnitude(v):
        return v
    return u

def longer(u, v):
    if magnitude(u) < magnitude(v):
        return v
    return u

def insideAABB(v, topLeft, bottomRight):
    (vx, vy) = v
    (xl, yt) = topLeft
    (xr, yb) = bottomRight

    return vx >= xl and vx <= xr and vy >= yt and vy <= yb
