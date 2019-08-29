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

		if down.total < int(down.header_total_arquivo.headers["content-length"]):

			porcentagem = down.total/int(down.header_total_arquivo.headers["content-length"])
			porcentagem *= 100
			self.ui.progressBar.setValue(porcentagem)

		else:

			self.ui.progressBar.setValue(100)
			self.time_progress_bar.stop()

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
		
		#pega o link do video para baixar
		self.link = link
		#pega o nome do anime
		self.nome = nome

		#verifica se a variavel ja contem algum label clicado
		if self.link_clicado == None:
			self.link_clicado = obj
		#troca a cor do label clicado anteriomente
		else:

			self.link_clicado.setStyleSheet("""
					background-color: #606060;
					color: red;
					""")
			self.link_clicado = obj

		#conecta o botão de baixar a função baixar
		self.ui.baixar_btn.clicked.connect(self.baixar)

	def baixar(self):
		"""		Esta função inicia o download do episodio em uma nova thread para que não atrapalhe o fluxo normal do programa.
		"""

		global down
		
		#inicia uma thread para baixar o arquivo
		self.t = Thread(target=down.baixar_ep, args=(self.link, self.nome))
		#da um start na thread
		self.t.start()
		#traz a cor da label do episódio ao normal
		self.link_clicado.setStyleSheet("""
				background-color: #606060;
				color: red;
				""")
		#instancia do objeto QTimer para agenda um evento a cada 500 milissegundos
		self.time_progress_bar = QTimer(self)
		#conecta esse QTimer a função baixando da classe
		self.time_progress_bar.timeout.connect(self.baixando)
		#inicia a contagem
		self.time_progress_bar.start(30000)

if __name__ == "__main__":

	app = QApplication(sys.argv)
	janela = Janela_Principal()
	janela.show()
	sys.exit(app.exec_())

