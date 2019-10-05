from robobrowser import RoboBrowser
import re, requests, urllib3
from bs4 import BeautifulSoup as bs
import time, platform, threading, os

class DownAnime():

	def __init__(self):

		#instancia o RoboBrowser, seta o parser como html.parser para que analise o html
		self.browser = RoboBrowser(history=True, parser="html.parser")
		self.escolha_anime =  None
		self.completo = False
		self.link = "https://www.superanimes.org/busca?parametro="
		self.resultados = []
		self.anime_episodios = []
		self.sistema = platform.system()

	#função para fazer pesquisa do anime
	def pesquisar(self, nome):
		
		#verifica qual o site pq a ideia e pesquisar em varios sites caso não ache o anime neste
		if self.link == "https://www.superanimes.org/busca?parametro=":
			
			#tranforma os espaços em (+) para realizar a pesquisa
			nome = nome.replace(" ", "+")
			#pesquisa os animes com nome parecido
			self.conexao = requests.get(f"{self.link}{nome}")
			pesquisa = bs(self.conexao.text, "html.parser")
			#percorre pelos resultados
			for index, anime in enumerate(pesquisa.find_all("article")):
				#armazena os resultados
				self.resultados.append({"index": index, "nome": anime})
			
	def mostra_animes(self):


			#mostra os resultados
			for anime in self.resultados:

				print(f"{anime['index']}--{anime['nome'].h1.text}")

	#pega todos os episódios disponiveis
	def episodios(self):
		if self.link == "https://www.superanimes.org/busca?parametro=":

			#abre a pagina dos ep
			self.conexao = requests.get(self.resultados[self.escolha_anime]["nome"].h1.a["href"])
			#guarda o nome do anime
			self.nome_anime = self.resultados[self.escolha_anime]["nome"].h1.text
			#guarda o link do anime
			self.link_anime = self.conexao.url
			#parser para busca os eps
			pesquisa = bs(self.conexao.text, "html.parser")
			#pega as divs que contem os episodios
			numero_episodios = pesquisa.find("ul", "boxAnimeSobre")
			numero_episodios = re.findall("[\d]+", numero_episodios.find("div").find("li").text)[0]
			numero = int(numero_episodios)
			#constroi uma lista com todos os episodios disponiveis
			self.anime_episodios = [f"episodio-{episodio}" for episodio in range(1, numero+1)]
			

	def mostra_episodios(self):
		#mosta os episodios
		for index, ep in enumerate(self.anime_episodios):
				
			print(f"{index} -- Episodio-{ep}")

	
	def baixar_ep(self, eps=[]):
		try:

			for ep in eps:

				#requisita a pagina do episodio
				conexao = requests.get(f"{self.link_anime}/{ep}/")
				#pega o id do episodio
				id_anime = conexao.url.split("/")
				id_anime = id_anime[len(id_anime)-1]
				#requisita a pagina que contem o elemento video para baixar o ep
				conexao = requests.get("https://www.superanimes.org/player.php?file=ODIwNjQ5Mw==&type=2&thumb=https://4icdn.com/img/video/{id_anime}-medium.jpg")
				#parser para encontra o elemento video
				texto = bs(conexao.text, "html.parser")
				#pega o link do elemento video
				link = texto.find_all("video")
				link = link[0].source["src"]
				#requisita o video
				video = requests.get(link, stream=True)
				#escreve cada fatia em um arquivo
				with open(f"{self.nome_anime}-{ep}.mp4", "wb") as arquivo:

					for chunk in video.iter_content(chunk_size=1024):

						arquivo.write(chunk)
				
				
				if self.sistema == "Linux":

					os.system(f"mv {self.nome_anime}-{ep}.mp4 ~/Downloads/")
				
				
		except KeyboardInterrupt:

			self.completo = True
			print("programa parado")

	
	def baixando(self):
		
		self.sistema = platform.system()

		if self.sistema == "Linux":

			os.system("clear")

		elif self.sistema == "Windows":

			os.system("cls")

		while not self.completo:
			
			print("baixando", end="", flush=True)

			for c in [".",".",".","."]:

				print(c, end="", flush=True)
				time.sleep(1)
			print()

			if self.sistema == "Linux":

				os.system("clear")

			elif self.sistema == "Windows":

				os.system("cls")

down = DownAnime()
down.pesquisar("hunter")
down.mostra_animes()
down.escolha_anime = int(input("escolha o index: "))
down.episodios()
down.mostra_episodios()

eps = []

while True:

	ep = str(input("digite o index do ep(qualquer letra para cancelar): "))

	if ep.isnumeric():

		eps.append(down.anime_episodios[int(ep)])

	else:

		break

down.baixar_ep(eps)

