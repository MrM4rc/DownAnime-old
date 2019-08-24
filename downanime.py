from robobrowser import RoboBrowser
import re, requests
from bs4 import BeautifulSoup as bs

class DownAnime():

	def __init__(self):

		#instancia o RoboBrowser, seta o parser como html.parser para que analise o html
		self.browser = RoboBrowser(history=True, parser="html.parser")
	

	#faz a requisição do site
	def abrir_site(self, link="https://animesbz.com/episodios-de-animes/"):
		
		self.link = link
		self.browser.open(self.link, method="get")

	#função para fazer pesquisa do anime
	def pesquisa(self, nome):
		
		#verifica qual o site pq a ideia e pesquisar em varios sites caso não ache o anime neste
		if self.link == "https://animesbz.com/episodios-de-animes/":

			"procura os animes disponiveis"
			self.animes = self.browser.find_all("em")
			"guarda os nomes dos animes"
			self.animes_nome = []
			"guarda o resultado da pesquisa do anime"
			self.resultados = []
			"tranforma o nome do anime em um padrão pro site"
			novo_nome = []
			for index, anime in enumerate(self.animes):
				"salvando os nomes dos animes"
				self.animes_nome.append({"nome":anime.text, "index": index})
				
			"modificar o nome para pesquisar o anime"
			for pos, cara in enumerate(nome):

				if pos == 0:
					novo_nome.append(cara.upper())

				else:

					novo_nome.append(cara)
			nome = ""
			for cara in novo_nome:
				
				nome += cara
			
			self.nome_anime = nome
			"pesquisa o anime na lista de nomes"
			for anime in self.animes_nome:

				if len(re.findall(f"{nome}[\w \-0-9.]*", anime["nome"])):
					
					self.resultados.append({"nome": re.findall(f"\w*{nome}[\w \-0-9.]*", anime["nome"]), "index":anime["index"]})
			

			"mostra os resultados"
			for anime in self.resultados:

				print(f"{anime['index']}--{anime['nome'][0]}")
			
			escolha_anime = int(input("digite o numero do anime>>"))
			self.nome_anime = self.animes[escolha_anime].text.split(" ")

			nome = ""

			for chave in self.nome_anime:

				if chave != "Dublado":

					nome += chave + " "

			self.nome_anime = nome
			print(self.nome_anime)

			self.browser.open(self.animes[escolha_anime].a["href"], method="get")


	def episodios(self):
		if self.link == "https://animesbz.com/episodios-de-animes/":

			anime_episodios = self.browser.find_all("li")
			self.anime_episodios = []
			for ep in anime_episodios:
				
				if re.findall(f"^{self.nome_anime}\w*-?\w*", ep.text):

					self.anime_episodios.append(ep)

			for index, ep in enumerate(self.anime_episodios):
					
				print(f"{index} -- {ep.text}")

			ep_index = int(input("escolha o index do ep: "))

			self.baixar_ep(self.anime_episodios[ep_index].a["href"], self.anime_episodios[ep_index].text)

	def baixar_ep(self, link, nome):

		baixar = RoboBrowser(history=True, parser="html.parser")
		baixar.open(link, method="get")
		video = baixar.find_all("video")
		baixar = requests.get(video[0].source["src"])
		arquivo = open(f"{nome}.mp4", "wb")
		arquivo.write(baixar.content)
		arquivo.close()

down = DownAnime()
down.abrir_site()
down.pesquisa("dr")
down.episodios()
