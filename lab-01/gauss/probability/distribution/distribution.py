from abc import ABCMeta, abstractmethod

class AbstractDistribution(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def CDF(self, x):
        pass

    @abstractmethod
    def PDF(self, x):
        pass