"""
Лабораторная работа "ассимметричное шифрование" (#4): 6 +- 2 мин
Лабораторная работа "электронная подпись"(#5): 4 +- 1 мин
Лабораторная работа "сжатие"(#6): 10 +- 5 мин
---------------------------------------------------------
№ | Время, мин. | описание 								|
---------------------------------------------------------
1 | 6+-2 мин.   | сдать 4-ю лабу 						|
2 | 4+-1 мин.  	| сдать 5-ю лабу 						|
3 | 10+-5 мин. 	| сдать 6-ю лабу 						|
4 | 10+-3 мин. 	| сдать 4-ю и 5-ю лабу 					|
5 | 14+-6 мин. 	| сдать 5-ю и 6-ю лабу 					|
6 | 20+-8 мин. 	| закрыть лабы 							|
---------------------------------------------------------
Преподаватель принимает принимает лабораторные 4,25 часа = 255 минут.
Осталось 3 сдачи до конца семестра.
Преподаватель не простаивает без работы.
Сколько студентов закроют лабы, а сколько будет плакать горькими слезами?
----
Моделировать будем трижды от 0 до 255 единиц времени.
"""
import random

class UniformDistribution:
	def __init__(self, base, err):
		self.lo = base - err
		self.hi = base + err

	def getTime(self):
		return random.randint(self.lo, self.hi)


class Professor:
	def __init__(self, bases, errs):
		self.ops = [UniformDistribution(bases[0], errs[0]),
					UniformDistribution(bases[1], errs[1]),
					UniformDistribution(bases[2], errs[2]),
					UniformDistribution(bases[3], errs[3]),
					UniformDistribution(bases[4], errs[4]),
					UniformDistribution(bases[5], errs[5])]


class Students:
	def __init__(self, bases, errs):
		self.students = [UniformDistribution(bases[0], errs[0]),
						 UniformDistribution(bases[1], errs[1]),
						 UniformDistribution(bases[2], errs[2]),
						 UniformDistribution(bases[3], errs[3]),
						 UniformDistribution(bases[4], errs[4]),
						 UniformDistribution(bases[5], errs[5])]


class QueueNetwork:
	def __init__(self):
		self.startTime = 0
		self.endTime = 255
		self.opps = [0, 0, 0, 0, 0, 0]
		self.jobs = list()
		self.professor = Professor([6, 4, 10, 10, 14, 20], [2, 1, 5, 3, 6, 8])
		self.students = Students([4, 3, 5, 7, 8, 12], [0, 0, 0, 0, 0, 0])

	def NextRound(self):
		self.startTime = 0
		self.endTime = 255
		self.jobs = list()

	def GetDayInfo(self):
		print(self.startTime)
		print(self.endTime)
		print(self.days)
		print(self.opps)
		print(self.jobs)

	def generateStudents(self):
		for i in range(6):
			t = 0
			while t < self.endTime:
				t += self.students.students[i].getTime()
				self.addJob([t, i])

	def modeling(self):
		self.generateStudents()
		i = 0
		while self.startTime < self.endTime and i < len(self.jobs):
			while self.startTime > self.jobs[i][0]:
				i += 1
			self.startTime = self.jobs[i][0]
			self.startTime += self.professor.ops[self.jobs[i][1]].getTime()
			if (self.startTime < self.endTime):
				self.opps[self.jobs[i][1]] += 1
			i += 1

	def get_result(self):
		s = 0
		for i in self.opps:
			s += i

		print("Студентов принято: ", s)
		print("Студенты, сдавшие одну лабораторную: ", self.opps[0] + self.opps[1] + self.opps[2])
		print("Студенты, сдавшие две лабораторные: ", self.opps[3] + self.opps[4])
		print("Студенты, закрывшие лабораторные по курсу: ", self.opps[5])

	def addJob(self, event: list):
		i = 0
		while i < len(self.jobs) and self.jobs[i][0] < event[0]:
			i += 1
		self.jobs.insert(i, event)


if __name__ == "__main__":
	model = QueueNetwork()
	model.modeling()
	model.NextRound()
	model.modeling()
	model.NextRound()
	model.modeling()
	model.get_result()
