from PyQt5.QtWidgets import QApplication
import sys

from gui.driver import App

   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    app.setStyle('QtCurve')
    sys.exit(app.exec_())