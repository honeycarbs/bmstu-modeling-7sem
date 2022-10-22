from probability.distribution.distribution import AbstractDistribution

import math

class Uniform(AbstractDistribution):
    __slots__ = ["min",
                "max"]

    def __init__(self, min, max):
        self.min = min
        self.max = max
        

    def CDF(self, x) -> float:
        if x < self.min:
            return 0
        if x > self.max:
            return 1
	
        return (x - self.min) / (self.max - self.min)

    def PDF(self, x) -> float:
        if x < self.min:
            return 0
        if x > self.max:
            return 0
        
        return 1 / (self.max - self.min)
