import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QProgressBar
from PySide2.QtCore import QFile, Slot, QTimer, QThread
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
				background-color: #606060;
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
		self.setStyleSheet("""
				background-color: rgb(255, 255, 255)
				""")
		self.pai.baixar_ep(self.link, self.text(), self)


class Janela_Principal(QMainWindow):

	def __init__(self):
		super(Janela_Principal, self).__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		#conecta o botão a função de pesquisa
		self.ui.botao_pesquisa.clicked.connect(self.pesquisar)
		self.barra = 0
		self.link_clicado = None
	
	def baixando(self):
		
		global down

		if not down.baixado:

			self.barra += 1
			self.ui.progressBar.setValue(self.barra)
			
			if self.barra == 100:
				
				self.barra = 0

		else:

			self.ui.progressBar.setValue(100)

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

	def baixar_ep(self, link, nome, obj):

		global down
		
		#inicia o download em uma thread
		self.link = link
		self.nome = nome

		if self.link_clicado == None:
			self.link_clicado = obj
		else:

			self.link_clicado.setStyleSheet("""
					background-color: #606060;
					color: red;
					""")
			self.link_clicado = obj

		self.ui.baixar_btn.clicked.connect(self.baixar)

	def baixar(self):
		"""
		Esta função vai mostra um mansagem de carregando ate que o anime seja baixado
		"""

		global down
		carregando = "baixando"

		t = Thread(target=down.baixar_ep, args=(self.link, self.nome))
		t.start()
		self.link_clicado.setStyleSheet("""
				background-color: #606060;
				color: red;
				""")

		time = QTimer(self)
		time.timeout.connect(self.baixando)
		time.start(500)

if __name__ == "__main__":

	app = QApplication(sys.argv)
	janela = Janela_Principal()
	janela.show()
	sys.exit(app.exec_())

