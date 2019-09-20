from robobrowser import RoboBrowser
import re, requests
from bs4 import BeautifulSoup as bs
import time, platform, threading, os

class DownAnime():

	def __init__(self):

		#instancia o RoboBrowser, seta o parser como html.parser para que analise o html
		self.browser = RoboBrowser(history=True, parser="html.parser")
		self.escolha_anime =  None
		self.completo = False

	#faz a requisição do site
	def abrir_site(self, link="https://animesbz.com/episodios-de-animes/"):
		
		self.link = link
		self.browser.open(self.link, method="get")

	#função para fazer pesquisa do anime
	def pesquisa(self, nome):
		
		#verifica qual o site pq a ideia e pesquisar em varios sites caso não ache o anime neste
		if self.link == "https://animesbz.com/episodios-de-animes/":

			#procura os animes disponiveis
			self.animes = self.browser.find_all("em")
			#guarda os nomes dos animes
			self.animes_nome = []
			#guarda o resultado da pesquisa do anime
			self.resultados = []
			for index, anime in enumerate(self.animes):
				#salvando os nomes dos animes
				self.animes_nome.append({"nome":anime.text, "index": index})
				
			#pesquisa o anime na lista de nomes
			for anime in self.animes_nome:

				if len(re.findall(f"{nome}[\w /\\\+\.\-\*\: 0-9 A-z]*", anime["nome"], flags=re.I)) > 0:

					self.resultados.append({"nome": re.findall(f"{nome}[\w /\\\+\.\-\*\: 0-9 A-z]*", anime["nome"], flags=re.I), "index":anime["index"]})
			
	def mostra_animes(self):


			#mostra os resultados
			for anime in self.resultados:

				print(f"{anime['index']}--{anime['nome'][0]}")

	#pega todos os episódios disponiveis
	def episodios(self):
		if self.link == "https://animesbz.com/episodios-de-animes/":

			#abre a pagina dos ep
			self.browser.open(self.animes[self.escolha_anime].a["href"], method="get")

			busca = self.browser.find_all("ul")
			
			self.anime_episodios = []
			
			for li in busca[3]:
				
				self.anime_episodios.append(li)

	def mostra_episodios(self):
		#mosta os episodios
		for index, ep in enumerate(self.anime_episodios):
				
			print(f"{index} -- {ep.text}")

	
	def baixar_ep(self, link, nome):
		try:
			#intancia do robobrowser para pega o link do video
			baixar = RoboBrowser(history=True, parser="html.parser")
			baixar.open(link, method="get")
			#pega o elemento com tag de video
			video = baixar.find_all("video")
			#inicia um thread para fazer uma barra de carregamento
			thread = threading.Thread(target=self.baixando)
			thread.start()
			#faz a requisão do video
			baixar = requests.get(video[0].source["src"])
			#abre o arquivo com formato mp4 para salva o video
			arquivo = open(f"{nome}.mp4", "wb")
			#escreve os bits no arquivo
			arquivo.write(baixar.content)
			self.completo = True
			#fecha o arquivo
			arquivo.close()

			if self.sistema == "Linux":

				os.system(f"mv {nome}.mp4 ~/Downloads/")

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



