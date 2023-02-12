from numpy.random import gamma, normal
import random

class GaussianDistributon:
    def __init__(self, mu: float, sigma: float):
        self.mu = mu
        self.sigma = sigma
    
    def GetRandomValue(self):
        return normal(self.mu, self.sigma)