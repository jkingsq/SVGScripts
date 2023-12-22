import inspect
import math
import vector2D as vec

def ortho(vec):
    (x, y) = vec

    return (-1 * y, x)

def arity(f):
    signature = inspect.signature(f)

    len(signature.parameters)


# Standalone cornersBC functions

# Python does not allow multi-line lambdas, so the workaround here is to make
# as many types of callable objects as I need randomly-selectable functions
class UShape:
    def __call__(self, cornerA, cornerD, eccentricity):
        transversal = ortho(vec.diff(cornerA, cornerD))
        scaledTransversal = vec.scale(eccentricity, transversal)

        cornerB = vec.sum(cornerA, scaledTransversal)
        cornerC = vec.sum(cornerD, scaledTransversal)

        return (cornerB, cornerC)

class ZShape:
    def __call__(self, cornerA, cornerD, eccentricity):
        tileCenter = vec.midpoint(cornerA, cornerD)
        halfTransverse = ortho(vec.diff(cornerD, tileCenter))

        cornerB = vec.sum(tileCenter, vec.scale(eccentricity, halfTransverse))
        cornerC = vec.sum(tileCenter, vec.scale(-1 * eccentricity, halfTransverse))

        return (cornerB, cornerC)

class VSlant:
    def __call__(self, cornerA, cornerD, eccentricity):
        transversal = ortho(vec.diff(cornerA, cornerD))
        scaledTransversal = vec.scale(eccentricity, transversal)

        cornerB = vec.sum(cornerA, scaledTransversal)
        cornerC = vec.midpoint(scaledTransversal, cornerD, eccentricity)

        return (cornerB, cornerC)

class ZSlant:
    def __call__(self, cornerA, cornerD, eccentricity):
        transversal = ortho(vec.diff(cornerA, cornerD))

        maxCornerB = vec.sum(cornerD, transversal)
        maxCornerC = vec.diff(cornerA, transversal)

        cornerB = vec.midpoint(cornerA, maxCornerB, eccentricity)
        cornerC = vec.midpoint(cornerD, maxCornerC, eccentricity)

        return (cornerB, cornerC)

class Spike:
    def __call__(self, cornerA, cornerD, eccentricity):
        transversal = ortho(vec.diff(cornerA, cornerD))

        maxCornerB = vec.sum(cornerD, transversal)
        maxCornerC = vec.sum(cornerA, transversal)

        cornerB = vec.midpoint(cornerA, maxCornerB, eccentricity)
        cornerC = vec.midpoint(cornerD, maxCornerC, eccentricity)

        return (cornerB, cornerC)

class Loop:
    def __call__(self, cornerA, cornerD, eccentricity):
        tileCenter = vec.midpoint(cornerA, cornerD)
        axis = vec.diff(cornerA, cornerD)
        transversal = ortho(vec.diff(cornerA, cornerD))

        maxCornerB = vec.scale(
                # 1 / math.sqrt(2),
                1,
                vec.sum(
                    tileCenter,
                    transversal,
                    vec.scale(-1, axis)
                )
            )

        maxCornerC = vec.scale(
                # 1 / math.sqrt(2),
                1,
                vec.sum(
                    tileCenter,
                    transversal,
                    axis
                )
            )

        cornerB = vec.midpoint(tileCenter, maxCornerB, eccentricity)
        cornerC = vec.midpoint(tileCenter, maxCornerC, eccentricity)

        return (cornerB, cornerC)

# cornersBC modifiers and combinations
def splitAndMerge(pairA, pairB, fn):
    return (
        fn(pairA[0], pairB[0]),
        fn(pairA[1], pairB[1])
    )

class Plain:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, cornerA, cornerD, eccentricity):
        return fn(cornerA, cornerD, eccentricity)

class Ortho:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, cornerA, cornerD, eccentricity):
        center = vec.midpoint(cornerA, cornerD)

        cornerB, cornerC = fn(cornerA, cornerD, eccentricity)

        resultCornerB = vec.sum(
            ortho(vec.diff(cornerB, center)),
            center
        )

        resultCornerC = vec.sum(
            ortho(vec.diff(cornerC, center)),
            center
        )

        return (resultCornerB, resultCornerC)

class Sum:
    def __init__(self, fnA, fnB):
        self.fnA = fnA
        self.fnB = fnB

    def __call__(self, cornerA, cornerD, eccentricity):
        center = vec.midpoint(cornerA, cornerD)

        return splitAndMerge(
            self.fnA(cornerA, cornerD, eccentricity),
            self.fnB(cornerA, cornerD, eccentricity),
            lambda u, v: vec.sum(
                vec.diff(u, center),
                vec.diff(v, center),
                center
            )
        )
