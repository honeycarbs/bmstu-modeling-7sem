import random

def enqueueJob(jobs, job):
    i = 0
    while i < len(jobs) and jobs[i][0] < job[0]:
        i += 1
    if 0 < i < len(jobs):
        jobs.insert(i - 1, job)
    else:
        jobs.insert(i, job)


def EventSimulation(distribution, jobProcessor, jobsAmount=0, returnPercentage=0):
    processedJobs = 0
    currentQueueLen = 0
    maxQueueLen = 0

    jobs = [[distribution.GetRandomValue(), 'g']]

    free, isProcessed = True, False

    generatedJobs = 0
    returnedJobs = 0

    while processedJobs < jobsAmount + returnedJobs:

        job = jobs.pop(0)

        if job[1] == 'g' and generatedJobs <= jobsAmount:

            currentQueueLen += 1
            generatedJobs += 1

            if currentQueueLen > maxQueueLen:
                maxQueueLen = currentQueueLen

            enqueueJob(jobs, [job[0] + distribution.GetRandomValue(), 'g'])

            if free:
                isProcessed = True

        elif job[1] == 'p':

            processedJobs += 1

            if random.randint(1, 100) <= returnPercentage:
                returnedJobs += 1
                currentQueueLen += 1

            isProcessed = True

        if isProcessed:

            if currentQueueLen > 0:
                currentQueueLen -= 1
                t = jobProcessor.GetRandomValue()
                enqueueJob(jobs, [job[0] + t, 'p'])
                free = False
            else:
                free = True
            isProcessed = False

    return maxQueueLen, processedJobs, returnedJobs


def TimekeepingSimulation(distribution, jobProcessor, jobsAmount=0, returnPercentage=0, step=0.001):
    processedJobs = 0

    currentTime = step
    generationTime = distribution.GetRandomValue()
    processTime = 0

    currentQueueLen = maxQueueLen = 0
    generatedJobs = 0
    returnedJobs = 0

    while processedJobs < jobsAmount + returnedJobs:
        
        if currentTime > generationTime and generatedJobs <= jobsAmount:
            currentQueueLen += 1
            generatedJobs += 1
            if currentQueueLen > maxQueueLen:
                maxQueueLen = currentQueueLen
            generationTime += distribution.GetRandomValue()

        if currentTime > processTime:
            if currentQueueLen > 0:
                processedJobs += 1

                if random.randint(1, 100) <= returnPercentage:
                    returnedJobs += 1
                    currentQueueLen += 1

                currentQueueLen -= 1
                processTime += jobProcessor.GetRandomValue()
        currentTime += step

    return maxQueueLen, processedJobs, returnedJobs