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
				color: white;
				background-color: #606060;
				""")
		self.marcar = True

	def mostra_anime_ep(self, obj):
		"""
		Esta função envia o index do anime escolhido para o DownAnime pesquisa pelos episódios
		"""
		global down
		global janela
		
		down.escolha_anime = self.escolha
		down.episodios()
		janela.episodios()

	def baixar(self, obj):
		"""
		chama a função para baixar os episódios
		"""
		
		global janela
		
		self.setStyleSheet("""
				background-color: rgb(255, 255, 255);
				color:black;
				""")
        #verifica se algum label foi clicado, possibilitando o download
		janela.download_on = True
		janela.baixar_ep(self.link, self.text(), self)


class Janela_Principal(QMainWindow):

	def __init__(self):
		super(Janela_Principal, self).__init__()

		global down
		
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.icon = QIcon("./downanime.ico")
		#Adiciona icone a janela quando compilado com pyinstaller
		#self.icon = QIcon(sys._MEIPASS+"/downanime.ico")
		self.setWindowIcon(self.icon)
		#conecta o botão a função de pesquisa
		self.ui.botao_pesquisa.clicked.connect(self.pesquisar)
		self.barra = 0
		#armazena a label que foi clicada para trocar cor e pega links
		self.link_clicado = None
		#conecta o botão de baixar a função baixar
		self.ui.baixar_btn.clicked.connect(self.baixar)
		self.download_on = False

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
			#adiciona o label a area de animes
			self.ui.area_animes_r.addWidget(label)


	def episodios(self):
		
		global down

		
		#limpa a area onde fica os animes/episódios
		for i in reversed(range(self.ui.area_animes_r.count())):
			
			self.ui.area_animes_r.itemAt(i).widget().deleteLater()
			#evita bugs na hora refenciar esse atributo
			self.link_clicado = None
		
		#constroi a lista de episódios
		for ep in down.anime_episodios:
			
			#constroi label com nome dos episodios
			label = Label(text=ep.text)
			#pega o link do episodio
			label.link = ep.a["href"]
			#atribui uma função sua ao mousepressevent
			label.mousePressEvent = label.baixar
			#adiciona o label a area de animes
			self.ui.area_animes_r.addWidget(label)

	def baixar_ep(self, link, nome, obj):

		global down
		
		
		#verifica se a variavel ja contem algum label clicado
		if self.link_clicado == None:
			
			#atribui o label a essa variavel
			self.link_clicado = obj
			#variavel que indica se é pra marca o episodio para baixar ou não
			self.link_clicado.marcar = False
			
			#pega o link do video para baixar
			self.link = link
			#pega o nome do anime
			self.nome = nome
			
			
		#troca a cor do label clicado anteriomente
		elif self.link_clicado == obj and not self.link_clicado.marcar:
			
			self.link_clicado.marcar = True
			self.link_clicado.setStyleSheet("""
				background-color: #606060;
				color: white;
				""")
			self.link = self.nome = ""
			
		elif self.link_clicado == obj and self.link_clicado.marcar:
			
			self.link_clicado.marcar = False
			self.link_clicado.setStyleSheet("""
				background-color: rgb(255, 255, 255);
				color: black;
				""")
			
			self.link = link
			self.nome = nome
			
		else:

			self.link_clicado.setStyleSheet("""
				background-color: #606060;
				color: white;
				""")
			self.link_clicado = obj


	def baixar(self):
		"""		Esta função inicia o download do episodio em uma nova thread para que não atrapalhe o fluxo normal do programa.
		"""

		global down
		
		#verifica se um label foi clicado e se o down ja esta baixando alguma coisa.
		if self.download_on and not down.baixando:
			
			self.download_on = False
			
			#inicia uma thread para baixar o anime
			self.t = Thread(target=down.baixar_ep, args=(self.link, self.nome))
			self.t.start()
			
			#traz a cor da label do episódio ao normal
			self.link_clicado.setStyleSheet("""
					background-color: #606060;
					color: white;
					""")
			self.link_clicado.marcar = True
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

