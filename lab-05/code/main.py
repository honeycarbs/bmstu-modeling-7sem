import random


class Generator:
    def __init__(self, base, err):
        self.low = base - err
        self.high = base + err

    def generationTime(self):
        return random.randint(self.low, self.high)


class Operator(Generator):
    def __init__(self, base, err):
        super().__init__(base, err)
        self.busy = False


class Computer:
    def __init__(self, time):
        self.generationTime = time
        self.busy = False


class QueueNetwork:
    def __init__(self, n):
        self.n = n
        self.jobs = list()
        self.clients = Generator(10, 2)
        self.operators = [Operator(20, 5), Operator(40, 10), Operator(40, 20)]
        self.computers = [Computer(15), Computer(30)]
        self.lines = [0, 0]
        self.processed = 0
        self.lost = 0

    def reset(self, n):
        self.n = n
        self.jobs = list()
        self.clients = Generator(10, 2)
        self.operators = [Operator(20, 5), Operator(40, 10), Operator(40, 20)]
        self.computers = [Computer(15), Computer(30)]
        self.lines = [0, 0]
        self.processed = 0
        self.lost = 0

    def model(self):
        self.AddJob([self.clients.generationTime(), 'client'])
        while self.processed + self.lost < self.n:
            job = self.jobs.pop(0)
            if job[1] == 'client':
                self.newClient(job[0])
            elif job[1] == 'operator':
                self.OperatorFinished(job)
            elif job[1] == 'pc':
                self.ComputerFinished(job)
        return self.lost

    def newClient(self, time):
        i = 0
        while i < 3 and self.operators[i].busy:
            i += 1
        if i == 3:
            self.lost += 1
        else:
            self.operators[i].busy = True
            self.AddJob(
                [time + self.operators[i].generationTime(), 'operator', i])
        self.AddJob([time + self.clients.generationTime(), 'client'])

    def OperatorFinished(self, job):
        self.operators[job[2]].busy = False
        if job[2] < 2:
            self.lines[0] += 1
            job[2] = 0
        else:
            self.lines[1] += 1
            job[2] = 1
        self.ComputerGetJob(job)

    def ComputerGetJob(self, job):
        cnum = job[2]
        if not self.computers[cnum].busy and self.lines[cnum] > 0:
            self.computers[cnum].busy = True
            self.AddJob(
                [job[0] + self.computers[cnum].generationTime, 'pc', cnum])
            self.lines[cnum] -= 1

    def ComputerFinished(self, job):
        self.computers[job[2]].busy = False
        self.processed += 1
        self.ComputerGetJob(job)

    def AddJob(self, job: list):
        i = 0
        while i < len(self.jobs) and self.jobs[i][0] < job[0]:
            i += 1
        self.jobs.insert(i, job)


if __name__ == "__main__":
    n = 300
    model = QueueNetwork(n)
    model.model()
    n0 = model.processed
    n1 = model.lost
    print("Processed:", n0, "\nLost:", n1,
          "\nLost percent:", 100 * n1 / (n0 + n1))

    print('\nУсредненная оценка после выполнения 100 раз')
    n0 = 0
    n1 = 0
    times = 1000
    for i in range(times):
        model.reset(n)
        model.model()
        n0 += model.processed
        n1 += model.lost
    n0 /= times
    n1 /= times
    print("Processed:", n0, "\nLost:", n1,
          "\nLost percent:", 100 * n1 / (n0 + n1))
