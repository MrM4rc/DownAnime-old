import sys
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtCore import QFile
from inter_downanime import Ui_MainWindow

class Janela_Principal(QMainWindow):

	def __init__(self):
		super(Janela_Principal, self).__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

if __name__ == "__main__":

	app = QApplication(sys.argv)
	janela = Janela_Principal()
	janela.show()

	sys.exit(app.exec_())

