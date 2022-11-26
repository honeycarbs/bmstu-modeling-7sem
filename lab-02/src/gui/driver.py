from re import L
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel

from markov.kolmogorov import Kolmogorov

# Main Window


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Лабораторная работа №2, Казаева Татьяна ИУ7-76Б'
        self.left = 0
        self.top = 0
        self.width = 700
        self.height = 800

        self.INITIAL_TABLE_SIZE = 3

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout = QFormLayout()

        # ----------- TABLE SCALING OPS --------------
        self.sizeLabel = QLabel("Размер матрицы")
        self.sizeLineEdit = QLineEdit()
        self.sizeLineEdit.setText(str(self.INITIAL_TABLE_SIZE))

        self.SetSlzeBttn = QPushButton("Построить")

        self.ZerofyBttn = QPushButton("Обнулить")

        self.RandomizeButton = QPushButton("Заполнить случайными числами")

        self.CalculateBttn = QPushButton("Вычислить")

        self.CreateProbMatrix(self.INITIAL_TABLE_SIZE)
        self.Zerofy()

        self.CreateResultTable()

        # ----------------- LAYOUT ----------------------
        self.layout.addRow(self.sizeLabel, self.sizeLineEdit)

        self.layout.addRow(self.SetSlzeBttn)

        self.layout.addRow(self.RandomizeButton, self.ZerofyBttn)

        self.layout.addRow(self.CalculateBttn)

        self.probMatrixLabel = QLabel("Матрица")
        self.layout.addRow(self.probMatrixLabel)

        self.layout.addRow(self.ProbMatrix)

        self.resultTableLabel = QLabel("Результат")
        self.layout.addRow(self.resultTableLabel)
        self.layout.addRow(self.ResultTable)

        # --------------- BUTTONS ----------------------
        self.SetSlzeBttn.clicked.connect(self.updateLayout)
        self.ZerofyBttn.clicked.connect(self.Zerofy)
        self.RandomizeButton.clicked.connect(self.Randomize)
        self.CalculateBttn.clicked.connect(self.SolvingWrapper)

        # Show window
        self.setLayout(self.layout)
        self.show()

    def updateLayout(self):
        try:
            int(self.sizeLineEdit.text())
        except ValueError:
            print("caught value error")
            return

        size = int(self.sizeLineEdit.text())

        if self.ProbMatrix.rowCount() == size:
            return

        self.ProbMatrix.setRowCount(size)
        self.ProbMatrix.setColumnCount(size)

        self.Zerofy()

    def Zerofy(self):
        try:
            int(self.sizeLineEdit.text())
        except ValueError:
            print("caught value error")
            return

        tableSize = int(self.sizeLineEdit.text())

        for i in range(tableSize):
            for j in range(tableSize):
                self.ProbMatrix.setItem(i, j, QTableWidgetItem(str(float(0))))

        self.ProbMatrix.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ProbMatrix.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def Randomize(self):
        try:
            int(self.sizeLineEdit.text())
        except ValueError:
            print("caught value error")
            return

        tableSize = int(self.sizeLineEdit.text())

        for i in range(tableSize):
            for j in range(tableSize):
                if i != j:
                    self.ProbMatrix.setItem(i, j, QTableWidgetItem(
                        str(round(random.random(), 4))))
                else:
                    self.ProbMatrix.setItem(
                        i, j, QTableWidgetItem(str(float(0))))

        self.ProbMatrix.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ProbMatrix.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # Create table
    def CreateProbMatrix(self, size):
        self.ProbMatrix = QTableWidget()

        # Row count
        self.ProbMatrix.setRowCount(size)

        # Column count
        self.ProbMatrix.setColumnCount(size)

    def CreateResultTable(self):
        self.ResultTable = QTableWidget()

        # Row count
        self.ResultTable.setRowCount(1)
        self.ResultTable.setColumnCount(3)

        self.ResultTable.setItem(0, 0, QTableWidgetItem('Состояние'))
        self.ResultTable.setItem(
            0, 1, QTableWidgetItem('Предельная вероятность'))
        self.ResultTable.setItem(0, 2, QTableWidgetItem('Время'))

        self.ResultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def SolvingWrapper(self):
        tableSize = self.ProbMatrix.rowCount()
        self.ProbMatrix.clearSelection()

        ProbMatrixNumbers = [
            [0 for _ in range(tableSize)] for _ in range(tableSize)]
        for i in range(tableSize):
            for j in range(tableSize):
                cell = self.ProbMatrix.item(i, j).text()
                try:
                    float(cell)
                except ValueError:
                    print("caught value error")
                    return

                num = float(cell)
                if i == j and num != 0:
                    print("Переход в одно и то же состояние невозможен")
                    return

                ProbMatrixNumbers[i][j] = num
                
        kolm = Kolmogorov(ProbMatrixNumbers)
        stationaryProbs = kolm.computeStaionaryProbabilites()

        startProbs = [0] * len(ProbMatrixNumbers[0])
        startProbs[len(ProbMatrixNumbers[0]) - 1] = 1

        times = kolm.getLimitTimes(startProbs)

        print(stationaryProbs, sum(stationaryProbs))
        print(times)

        self.FillResultTable(stationaryProbs, times)

    def FillResultTable(self, probs, times):
        self.ResultTable.setRowCount(len(probs) + 1)
        self.ResultTable.setRowCount(len(probs) + 1)

        for i in range(len(probs)):
            self.ResultTable.setItem(i + 1, 0, QTableWidgetItem(str(i)))
            self.ResultTable.setItem(i + 1, 1, QTableWidgetItem(str(probs[i])))
            self.ResultTable.setItem(i + 1, 2, QTableWidgetItem(str(times[i])))
        
        self.ResultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ResultTable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)


