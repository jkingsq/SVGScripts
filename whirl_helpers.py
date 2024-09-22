import math
import random
import whirl_tile_effects as tileEffects
import whirl_symmetry_effects as symmetryEffects
import inspect

def randomKVPair(d):
    key = random.choice(list(d.keys()))

    return (key, d[key])

def arity(f):
    return len(inspect.signature(f).parameters)

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

tileEffectsDict = {
    "u-shape": tileEffects.UShape(),
    "z-shape": tileEffects.ZShape(),
    "v-slant": tileEffects.VSlant(),
    "z-slant": tileEffects.ZSlant(),
    "spike": tileEffects.Spike(),
    "loop": tileEffects.Loop()
}

symmetryEffectsDict = {
    # "lateral": symmetryEffects.Lateral(),
    # "rotational": symmetryEffects.Rotational(),
    # "translational": symmetryEffects.Translational(),
    "translational with reflections": symmetryEffects.TranslationalWithReflections()
}

symmetryName, symmetryEffectFn = randomKVPair(symmetryEffectsDict)

effectCombinationsDict = {
    "ortho": tileEffects.Ortho,
    "centeredSum": tileEffects.CenteredSum,
    "compose": tileEffects.Compose,
    "avg": tileEffects.Average,
    "sum": tileEffects.Sum,
    "swap": tileEffects.Swap,
    "reflect-b": tileEffects.ReflectB,
    "reflect-c": tileEffects.ReflectC
}

def randomCombinationEffect(plainChance=0.1):
    choice = random.random()
    name, function = (None, None)

    if choice <= plainChance:
        (name, function) = randomKVPair(tileEffectsDict)
    else:
        (comboName, comboClass) = randomKVPair(effectCombinationsDict)

        # chance of recursing further decreases by one third
        nextPlainChance = 1.0 - 2.0 * (1.0 - plainChance) / 3.0

        effects = [randomCombinationEffect(plainChance=nextPlainChance) for n in range(arity(comboClass))]

        # blursed unzip idiom I love python
        [effectNames, effectFunctions] = list(zip(*effects))

        effectNamesStr = ", ".join(effectNames)
        name = comboName + "(" + effectNamesStr + ")"
        function = comboClass(*effectFunctions)

    return (name, function)

tEffect = (
    tRangeName + " " + tDistributionName,
    lambda t: tRangeEffect(tDistributionEffect(t))
)

symmetryEffect = (
    symmetryName, symmetryEffectFn
)

tileEffect = randomCombinationEffect()
