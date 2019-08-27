from robobrowser import RoboBrowser
import re, requests
from bs4 import BeautifulSoup as bs

class DownAnime():

	def __init__(self):

		#instancia o RoboBrowser, seta o parser como html.parser para que analise o html
		self.browser = RoboBrowser(history=True, parser="html.parser")
		self.escolha_anime =  None

		self.baixado = False

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
			#tranforma o nome do anime em um padrão pro site
			novo_nome = []
			for index, anime in enumerate(self.animes):
				#salvando os nomes dos animes
				self.animes_nome.append({"nome":anime.text, "index": index})
				
			#modificar o nome para pesquisar o anime
			for pos, cara in enumerate(nome):

				if pos == 0:
					novo_nome.append(cara.upper())

				else:

					novo_nome.append(cara)
			
			nome = ""
			for cara in novo_nome:
				
				nome += cara
			
			self.nome_anime = nome
			
			#pesquisa o anime na lista de nomes
			for anime in self.animes_nome:

				if len(re.findall(f"{nome}[\w \-0-9.]*", anime["nome"])) > 0:

					self.resultados.append({"nome": re.findall(f"\w*{nome}[\w \-0-9.]*", anime["nome"]), "index":anime["index"]})
			
	def mostra_animes(self):


			#mostra os resultados
			for anime in self.resultados:

				print(f"{anime['index']}--{anime['nome'][0]}")

	#pega todos os episódios disponiveis
	def episodios(self):
		if self.link == "https://animesbz.com/episodios-de-animes/":

			#abre a pagina dos ep
			self.browser.open(self.animes[self.escolha_anime].a["href"], method="get")

			#pega o nome do anime escolhido
			self.nome_anime = self.animes[self.escolha_anime].text.split(" ")

			nome = ""
			#modifica o nome do anime para pega os eps
			for chave in self.nome_anime:

				if chave != "Dublado":

					nome += chave + " "
			
			self.nome_anime = nome	


			#procura todos os campos de listas
			anime_episodios = self.browser.find_all("li")
			#lista que vai guarda os ep
			self.anime_episodios = []
			#procura os episodios do anime
			for ep in anime_episodios:
				
				if re.findall(f"^{self.nome_anime}\w*-?\w*", ep.text):

					self.anime_episodios.append(ep)

	def mostra_episodios(self):
		#mosta os episodios
		for index, ep in enumerate(self.anime_episodios):
				
			print(f"{index} -- {ep.text}")

	
	def baixar_ep(self, link, nome):

		#intancia do robobrowser para pega o link do video
		baixar = RoboBrowser(history=True, parser="html.parser")
		print("baixando")
		baixar.open(link, method="get")
		#pega o elemento com tag de video
		video = baixar.find_all("video")
		#faz a requisão do video
		baixar = requests.get(video[0].source["src"])
		self.baixado = True
		#abre o arquivo com formato mp4 para salva o video
		arquivo = open(f"{nome}.mp4", "wb")
		#escreve os bits no arquivo
		arquivo.write(baixar.content)
		#fecha o arquivo
		arquivo.close()

