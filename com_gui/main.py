import sys
from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QProgressBar
from PySide2.QtGui import QIcon
from PySide2.QtCore import QFile, Slot, QTimer, QThread, SIGNAL
from inter_downanime import Ui_MainWindow
from downanime import DownAnime
import _thread
from threading import Thread, Event

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

		global down

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.icon = QIcon(sys._MEIPASS+"/downanime.ico")
		self.setWindowIcon(self.icon)
		#conecta o botão a função de pesquisa
		self.ui.botao_pesquisa.clicked.connect(self.pesquisar)
		self.barra = 0
		#armazena a label que foi clicada para trocar cor e pega links
		self.link_clicado = None
		#conecta o botão de baixar a função baixar
		self.ui.baixar_btn.clicked.connect(self.baixar)

	def baixando(self):
		
		global down

		if down.total < int(down.header_total_arquivo.headers["content-length"]):
			#calculo de porcentagem para pega progresso do download
			porcentagem = down.total/int(down.header_total_arquivo.headers["content-length"])
			#multiplica o valor obtido no calculo de porcentagem para pega um valor mais redondo
			porcentagem *= 100
			#altera o valor da barra de progresso
			self.ui.progressBar.setValue(porcentagem)

		else:
			#altera o valo da barra pra 100 quando o download ja foi feito
			self.ui.progressBar.setValue(100)
			#para um objeto QTimer que fica chamando essa função a cada 30s
			self.time_progress_bar.stop()
			#espera finalizar a thread de download
			self.t.join()

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
			
			#cria label com nomes do anime
			label = Label(text=resu["nome"][0])
			#pega o index para depois passa qual anime foi escolhido da lista
			label.escolha = resu["index"]
			#adiciona a função mostra do label ao mousepressevent
			label.mousePressEvent = label.mostra_anime_ep
			#atribui uma refencia a classe que lhe instanciou
			label.pai = self
			#adiciona o label a area de animes
			self.ui.area_animes_r.addWidget(label)


	def episodios(self):
		
		global down

		
		#limpa a area onde fica os animes/episódios
		for i in reversed(range(self.ui.area_animes_r.count())):

			self.ui.area_animes_r.itemAt(i).widget().deleteLater()
		
		#constroi a lista de episódios
		for ep in down.anime_episodios:
			
			#constroi label com nome dos episodios
			label = Label(text=ep.text)
			#pega o link do episodio
			label.link = ep.a["href"]
			#refencia a classe que lhe instanciou
			label.pai = self
			#atribui uma função sua ao mousepressevent
			label.mousePressEvent = label.baixar
			#adiciona o label a area de animes
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


	def baixar(self):
		"""		Esta função inicia o download do episodio em uma nova thread para que não atrapalhe o fluxo normal do programa.
		"""

		global down
		
		#inicia uma thread para baixar o anime
		self.t = Thread(target=down.baixar_ep, args=(self.link, self.nome))
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

