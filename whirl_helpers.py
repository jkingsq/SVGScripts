import math
import random
import whirl_tile_effects as tileEffects

def randomKVPair(d):
    key = random.choice(list(d.keys()))

    return (key, d[key])

tExponent = 3

tDistributionDict = {
    "uniform": lambda t : t,
    "exponential": lambda t : t**tExponent,
    "root-exponential": lambda t : t**(1/tExponent),
    "inverted-exponential": lambda t : 1 - (1-t)**tExponent,
    "quarter-sine": lambda t : math.sin(t * math.pi / 2)
}

tDistributionName, tDistributionEffect = randomKVPair(tDistributionDict)

tRangeDict = {
    "0,1": lambda t: t,
    "0,-1": lambda t: -1 * t,
    "-1,0": lambda t: t - 1,
    "1,2": lambda t: t+1,
    "-1,1": lambda t: 2*t - 1
}

tRangeName, tRangeEffect = randomKVPair(tRangeDict)

tEffect = (
    tRangeName + " " + tDistributionName,
    lambda t: tRangeEffect(tDistributionEffect(t))
)
# tEffect = ("hardcoded inverted-exponential", tEffectsDict["inverted-exponential"])

tileEffectsDict = {
    "u-shape": tileEffects.UShape(),
    "z-shape": tileEffects.ZShape(),
    "v-slant": tileEffects.VSlant(),
    "z-slant": tileEffects.ZSlant(),
    "spike": tileEffects.Spike(),
    "loop": tileEffects.Loop()
}

tileEffect = randomKVPair(tileEffectsDict)
# tileEffect = ("hardcoded loop", tileEffects.Loop())

effectCombinationsDict = {
    "plain": tileEffects.Plain,
    "ortho": tileEffects.Ortho,
    "sum": tileEffects.Sum
}
