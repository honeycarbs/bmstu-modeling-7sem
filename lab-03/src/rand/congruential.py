class Congruential():
    def __init__(self):
        self.cur = 10
        self.m = 36261
        self.a = 66037
        self.c = 312500

    def Generate(self, lo=0, hi=9, n=500):
        res = []
        for i in range(n):
            self.cur = (self.a * self.cur + self.c) % self.m
            num = int(lo + self.cur % (hi - lo))
            res.append(num)
        return res
