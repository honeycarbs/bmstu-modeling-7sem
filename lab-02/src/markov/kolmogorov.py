from os import times
import numpy as np
import numpy.typing as npt


TIME_DELTA = 1e-3
EPS = 1e-3

np.seterr(all='raise')

class Kolmogorov:
    def __init__(self, intensityMatrix: list[list[float]]):
        self.N: int = len(intensityMatrix[0])
        self.intensityMatrix: npt.NDArray = np.array(intensityMatrix, dtype=float)
        self.coefMatrix: npt.NDArray = self.InitCoefMatrix()

    def InitCoefMatrix(self) -> npt.NDArray:
        res: npt.NDArray = np.zeros((self.N, self.N), dtype=float)
        for i in range(self.N):
            for j in range(self.N):
                res[i, i] -= self.intensityMatrix[i, j]
                res[i, j] += self.intensityMatrix[j, i]
        return res

    def InitAugmMatrix(self) -> npt.NDArray:
        result: npt.NDArray = np.zeros(self.N, dtype=float)
        result[-1] = 1
        return result

    def computeStaionaryProbabilites(self) -> npt.NDArray:
        base: npt.NDArray = self.coefMatrix.copy()
        base[-1] = np.ones(self.N)
        augm: npt.NDArray = self.InitAugmMatrix()
        return np.linalg.solve(base, augm)

    def getProbIncrement(self, start_probabilities: npt.NDArray) -> npt.NDArray:
        result: npt.NDArray = np.zeros(self.N)
        for i, curr_prob in enumerate(start_probabilities):
            for j in range(self.N):
                if i == j:
                    result[i] += (-sum(self.intensityMatrix[i]) + self.intensityMatrix[i][j]) * curr_prob
                else:
                    result[i] += self.intensityMatrix[j][i] * start_probabilities[j]
        return result * TIME_DELTA

    def getLimitTimes(self, start_probabilities: npt.NDArray) -> npt.NDArray:
        limit_probabilities: npt.NDArray = self.computeStaionaryProbabilites()
        curProbs: npt.NDArray = start_probabilities.copy()
        times: npt.NDArray = np.zeros(self.N)
        cur = 0
        
        while not all(times):
            delta_p = self.getProbIncrement(curProbs)
            for i in range(self.N):
                if not times[i] and abs(curProbs[i] - limit_probabilities[i]) <= EPS:
                    times[i] = cur
                curProbs[i] += delta_p[i]
                cur += TIME_DELTA

        return times

