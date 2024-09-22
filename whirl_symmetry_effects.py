import math
import vector2D as vec

# Assumed to be a unit vector
reflectAxis = (1.0, 0.0)

def reflect(v):
    projection = vec.scale(
        vec.dot(v, reflectAxis),
        reflectAxis
    )

    return vec.midpoint(projection, v, -1.0)

class Rotational:
    def __call__(self, point, degree):
        (r, theta) = vec.toPolar(point)
        thetaIncrement = 2 * math.pi / degree

        result = []
        for i in range(degree):
            result.append(
                vec.fromPolar(r, theta + i * thetaIncrement)
            )

        return result

class Lateral:
    def __call__(self, point, degree):
        rotateFn = Rotational()

        return rotateFn(point, degree) + rotateFn(reflect(point), degree)

class Translational:
    def __call__(self, point, degree):
        # TODO remove when points and tiles are made less complex for high
        # degrees of symmetry
        degree = math.ceil(degree / 2)

        if degree == 1:
            return [point]

        result = []

        scaledPoint = vec.scale(4 / (3 * degree), point)

        for x in range(-1, degree + 1):
            for y in range(-1, degree + 1):
                offset = (
                    2 * x / (degree - 1) - 1.0,
                    2 * y / (degree - 1) - 1.0
                )

                result.append(vec.sum(scaledPoint, offset))

        return result

class TranslationalWithReflections:
    def __call__(self, point, degree):
        if degree == 1:
            return [point]

        result = []

        scaledPoint = vec.scale(4 / (3 * degree), point)

        for x in range(-1, degree + 1):
            for y in range(-1, degree + 1):
                (scaledX, scaledY) = scaledPoint

                reflectedPoint = (
                    scaledX * (-1)**x,
                    scaledY * (-1)**y
                )

                offset = (
                    2 * x / (degree - 1) - 1.0,
                    2 * y / (degree - 1) - 1.0
                )

                result.append(vec.sum(reflectedPoint, offset))

        return result

# Given one tile, return a list of tiles according to a symmetry effect
def applySymmetry(tile, symmetryFn, symmetryDegree):
    unzippedTiles = []
    for curve in tile:
        unzippedTiles.append(list(zip(*[symmetryFn(point, symmetryDegree) for point in curve])))

    # return [list(tile) for tile in zip(*unzippedTiles)]
    return [curve for tile in zip(*unzippedTiles) for curve in tile]
