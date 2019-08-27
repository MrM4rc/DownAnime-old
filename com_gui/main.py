import sys
from PySide2.QtWidgets import QMainWindow, QApplication,  QLabel
from PySide2.QtCore import QFile, Slot, QTime
from inter_downanime import Ui_MainWindow
from downanime import DownAnime
from threading import Thread

#instancia do DownAnime
down = DownAnime()

class Label(QLabel):

	def __init__(self, **kwargs):
		
		super(Label, self).__init__(**kwargs)

		self.setStyleSheet("""
				color: red;
				""")

	def mostra_anime_ep(self, obj):
		"""
		Esta função envia o index do anime escolhido para o DownAnime pesquisa pelos episódios
		"""
		global down
		down.escolha_anime = self.escolha
		down.episodios()
		self.pai.episodios()

	def baixar(self, obj):
		"""
		chama a função para baixar os episódios
		"""

		self.pai.baixar_ep(self.link, self.text())


class Janela_Principal(QMainWindow):

	def __init__(self):
		super(Janela_Principal, self).__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		#conecta o botão a função de pesquisa
		self.ui.botao_pesquisa.clicked.connect(self.pesquisar)
	
	@Slot()
	def pesquisar(self, pos):

		global down
		
		#abre o site para baixar animes
		down.abrir_site()
		#pesquisa os animes disponiveis 
		down.pesquisa(self.ui.barra_pesquisa.toPlainText())
		#limpa a area onde ficara os animes/episódios
		for i in reversed(range(self.ui.area_animes_r.count())):

			self.ui.area_animes_r.itemAt(i).widget().deleteLater()
		
		#coloca os resultados na tela
		for resu in down.resultados:
			
			label = Label(text=resu["nome"][0])
			label.escolha = resu["index"]
			label.mousePressEvent = label.mostra_anime_ep
			label.pai = self
			self.ui.area_animes_r.addWidget(label)


	def episodios(self):
		
		global down
		
		#limpa a area onde fica os animes/episódios
		for i in reversed(range(self.ui.area_animes_r.count())):

			self.ui.area_animes_r.itemAt(i).widget().deleteLater()
		
		#constroi a lista de episódios
		for ep in down.anime_episodios:
			
			label = Label(text=ep.text)
			label.link = ep.a["href"]
			label.pai = self
			label.mousePressEvent = label.baixar
			self.ui.area_animes_r.addWidget(label)

	def baixar_ep(self, link, nome):

		global down
		
		#inicia o download em uma thread
		t = Thread(target=down.baixar_ep, args=(link, nome))

		baixar = Baixando()
		t.start()

	def alterar(self):
		"""
		Esta função vai mostra um mansagem de carregando ate que o anime seja baixado
		"""
		carregando = "baixando"

		for c in range(0, 6):
			
			carregando += "."

			for i in reversed(range(self.ui.area_animes_r.count())):

				self.ui.area_animes_r.itemAt(i).widget().deleteLater()

			self.ui.area_animes_r.addWidget(Label(text=carregando))


if __name__ == "__main__":

	app = QApplication(sys.argv)
	janela = Janela_Principal()
	janela.show()
	sys.exit(app.exec_())

