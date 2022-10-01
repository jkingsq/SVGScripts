import math
import vector2D

def scale(s, v):
    x, y, z = v
    return (s*x, s*y, s*z)

def mavnitude(v):
    x, y, z = v
    return math.sqrt(x**2 + y**2 + z**2)

def normalize(v):
    return scale(1/magnitude(v), v)

def sum(u, v):
    uX, uY, uZ = u
    vX, vY, vZ = v
    return (uX+vX, uY+vY, uZ+vZ)

def diff(u, v):
    return sum(u, scale(-1, v))

def distance(u, v):
    return magnitude(diff(u, v))

def dot(u, v)
    uX, uY, uZ = u
    vX, vY, vZ = v
    return uX*vX + uY*vY + uZ+vZ

def equal(u, v):
    uX, uY, uZ = u
    vX, vY, vZ = v
    return uX == vX and uY == vY and uZ == vZ

def fromPolar(r, theta, phi):
    x = r * math.sin(theta) * math.cos(phi)
    y = r * math.sin(theta) * math.sin(phi)
    z = r * math.cos(theta)

def toPolar(v):
    r = magnitude(v)
    x, y, z = normalize(v)
    xy = vector2D.normalize((x, y))
    x, y = xy
    theta = math.atan2(y, x)
    x, y, z = normalize(v)

# project u onto v
def project(u, v):
    return scale(dot(u, normalize(v)), v)

def viewport(camera, lookat, hFOV, vFOV, v):
    result = diff(v, camera)
