from probability.distribution.distribution import AbstractDistribution

import math
from scipy import special


class Gaussian(AbstractDistribution):
    __slots__ = ["mean",
                "deviation",
                "variance"]

    def __init__(self, mean, variance):
        if variance <= 0.0:
            raise ValueError("Variance can't non-positive")

        self.mean = mean
        self.variance = variance
        self.deviation = math.sqrt(variance)

    def CDF(self, x) -> float:
        return 0.5 * special.erfc(-(x-self.mean)/(self.deviation*math.sqrt(2)))

    def PDF(self, x) -> float:
        m = self.deviation * math.sqrt(2*math.pi)
        e = math.exp(-math.pow(x-self.mean, 2) / (2 * self.variance))
        return e / m
