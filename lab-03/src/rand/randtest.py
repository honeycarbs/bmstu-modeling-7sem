import math, numpy, random

def getDeltas(a):
    deltas = []
    for i in range(len(a) - 1):
        deltas.append(abs(a[i + 1] - a[i]))
    return deltas

def variance(data):
    n = len(data)
    mean = sum(data) / n
    deviations = [(x - mean) ** 2 for x in data]
    variance = sum(deviations) / n

    return variance

def randomnessTest(a):
    deltas = getDeltas(a)
    n = len(deltas)
    sample = 1 / n * sum(deltas)

    if sample == 0:
        return 0.0
        
    Vkoef = math.sqrt(variance(deltas)) / sample
    return Vkoef 

