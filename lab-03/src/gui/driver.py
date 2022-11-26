from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRegExp,  QEvent, Qt,  pyqtSlot as pyqtslot
from PyQt5.QtGui import QRegExpValidator

import random

from rand import congruential, table, randtest


class NumericDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = super(NumericDelegate, self).createEditor(
            parent, option, index)
        if isinstance(editor, QLineEdit):
            reg_ex = QRegExp("[0-9]+")
            validator = QRegExpValidator(reg_ex, editor)
            editor.setValidator(validator)
        return editor

# Main Window


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Лабораторная работа №3, Казаева Татьяна ИУ7-76Б'
        self.prettyRowHeight = 0
        self.prettyColumnWidth = 0
        # self.left = 0
        # self.top = 0

        self.setFixedWidth(1000)
        self.setFixedHeight(600)

        self.TABLE_SIZE = 10
        self.SEQUENCE_SIZE = 500
        self.TABLE_STEP = self.SEQUENCE_SIZE // self.TABLE_SIZE

        self.byHandNums = [0 for _ in range(self.TABLE_SIZE)]

        self.ByAlg = QTableWidget()
        self.BuildTable(self.ByAlg, self.TABLE_SIZE, 3, False)
        self.FillCongruentialTable(self.ByAlg)

        self.prettyRowHeight = self.ByAlg.rowHeight(0)
        self.prettyColumnWidth = self.ByAlg.columnWidth(0)

        self.ByHand = QTableWidget()
        self.BuildTable(self.ByHand, self.SEQUENCE_SIZE, 1, True)
        self.ByHand.setHorizontalHeaderItem(0, QTableWidgetItem("1, 2, 3"))

        for i in range(self.SEQUENCE_SIZE):
            self.ByHand.setRowHeight(i, self.prettyRowHeight)

        self.ByTable = QTableWidget()
        self.BuildTable(self.ByTable, self.TABLE_SIZE, 3, False)
        self.fillFromFile(self.ByTable)

        self.ByHandLabel = QLabel("Собственные значения")
        self.ByAlgLabel = QLabel("Алгоритмический метод")
        self.ByTableLabel = QLabel("Табличный метод")

        self.ByHandPValLabel = QLabel("P-value = ")
        self.ByAlgPValLabel = QLabel("P-values = ")
        self.ByTablePValLabel = QLabel("P-values = ")

        self.CalculateBttn = QPushButton("Рассчитать")
        self.RandomizeBttn = QPushButton("Сгенерировать")

        layout = QGridLayout()
        layout.setHorizontalSpacing(30)
        layout.setVerticalSpacing(10)

        layout.addWidget(self.ByHandLabel, 0, 0, 1, 1)
        layout.addWidget(self.ByAlgLabel, 0, 1, 1, 1)
        layout.addWidget(self.ByTableLabel, 0, 2, 1, 1)

        layout.addWidget(self.ByHand, 1, 0, 1, 1)
        layout.addWidget(self.ByAlg, 1, 1, 1, 1)
        layout.addWidget(self.ByTable, 1, 2, 1, 1)

        layout.addWidget(self.ByHandPValLabel, 3, 0, 1, 1)
        layout.addWidget(self.ByAlgPValLabel, 3, 1, 1, 1)
        layout.addWidget(self.ByTablePValLabel, 3, 2, 1, 1)

        layout.addWidget(self.RandomizeBttn, 4, 0, 1, 1)
        layout.addWidget(self.CalculateBttn, 4, 1, 1, 1)

        self.setLayout(layout)

        self.CalculateBttn.clicked.connect(self.CalculateWrapper)
        self.RandomizeBttn.clicked.connect(self.RandomizeByHand)

        self.show()

    def BuildTable(self, table, rowCount, columnCount, clickable):
        table.setRowCount(rowCount)

        table.setColumnCount(columnCount)

        if columnCount != 1:
            headers = [str(i) for i in range(0, 500, 50)]
        else:
            headers = [str(i) for i in range(500)]
        
        for i, header in enumerate(headers):
            table.setVerticalHeaderItem(i, QTableWidgetItem(header))

        table.setSelectionMode(QAbstractItemView.NoSelection)
        if not clickable:
            table.setEditTriggers(QTableWidget.NoEditTriggers)
        else:
            delegate = NumericDelegate(table)
            table.setItemDelegate(delegate)

        if columnCount != 1:
            table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def fillFromFile(self, tab):
        t = table.BuiltinTable()

        self.fromFileNums1 = t.Generate(1)
        # print(len(self.fromFileNums1))
        for i in range(self.TABLE_SIZE):
            tab.setItem(i, 0, QTableWidgetItem(str(self.fromFileNums1[i * self.TABLE_STEP])))

        self.fromFileNums2 = t.Generate(2)
        for i in range(self.TABLE_SIZE):
            tab.setItem(i, 1, QTableWidgetItem(str(self.fromFileNums2[i * self.TABLE_STEP])))

        self.fromFileNums3 = t.Generate(3)
        for i in range(self.TABLE_SIZE):
            tab.setItem(i, 2, QTableWidgetItem(str(self.fromFileNums3[i * self.TABLE_STEP])))

    def FillCongruentialTable(self, table):
        cong = congruential.Congruential()

        self.congruentialNums1 = cong.Generate()
        for i in range(self.TABLE_SIZE):
            table.setItem(i, 0, QTableWidgetItem(
                str(self.congruentialNums1[i * self.TABLE_STEP])))

        self.congruentialNums2 = cong.Generate(10, 99)
        for i in range(self.TABLE_SIZE):
            table.setItem(i, 1, QTableWidgetItem(
                str(self.congruentialNums2[i * self.TABLE_STEP])))

        self.congruentialNums3 = cong.Generate(100, 999)
        for i in range(self.TABLE_SIZE):
            table.setItem(i, 2, QTableWidgetItem(
                str(self.congruentialNums3[i * self.TABLE_STEP])))

    def RandomizeByHand(self):
        self.byHandNums = []
        for i in range(500):
            self.byHandNums.append(random.randint(0, 999))
        for i in range(self.SEQUENCE_SIZE):
            self.ByHand.setItem(
                i, 0, QTableWidgetItem(str(self.byHandNums[i])))

    def CollectData(self, table, col, array):
        for j in range(table.rowCount()):
            cell = table.item(j, col).text()
            try:
                float(cell)
            except ValueError:
                print("caught value error")
                return

            num = int(cell)
            array[j] = num
        return array

    def CalculateWrapper(self):
        self.byHandNums = self.CollectData(self.ByHand, 0, self.byHandNums)
        pByHand1 = randtest.randomnessTest(self.byHandNums)

        pCongruential1 = randtest.randomnessTest(self.congruentialNums1)

        pCongruential2 = randtest.randomnessTest(self.congruentialNums2)

        pCongruential3 = randtest.randomnessTest(self.congruentialNums3)

        pFromFile1 = randtest.randomnessTest(self.fromFileNums1)

        pFromFile2 = randtest.randomnessTest(self.fromFileNums2)

        pFromFile3 = randtest.randomnessTest(self.fromFileNums3)

        self.ByHandPValLabel.setText(
            "P-value = {:.2f}".format(pByHand1))
        self.ByAlgPValLabel.setText(
            "P-values = {:.2f}, {:.2f}, {:.2f}".format(pCongruential1, pCongruential2, pCongruential3))
        self.ByTablePValLabel.setText(
            "P-values = {:.2f}, {:.2f}, {:.2f}".format(pFromFile1, pFromFile2, pFromFile3))
