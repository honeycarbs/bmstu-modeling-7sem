from numpy.random import gamma, normal
import random

class UniformDistributon:
    def __init__(self, lo: float, hi: float):
        self.lo = lo
        self.hi = hi
    
    def GetRandomValue(self):
        return self.lo + (self.hi - self.lo) * random.random()
