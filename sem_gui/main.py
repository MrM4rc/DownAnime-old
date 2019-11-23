from downanime import DownAnime
from time import sleep
from threading import Thread

def barraDeProgresso(episodios):

	global down

	sleep(20)
	down.baixando()

down = DownAnime()
#pega o nome do anime para pesquisar
pesquisar = str(input("digite o nome do anime: "))
#chama a função de pesquisa
down.pesquisar(pesquisar)
#mostra os episodios encontrados
down.mostra_animes()
#escolha do anime
down.escolha_anime = int(input("escolha o index do anime: "))
#pequisa os episodios
down.episodios()
#mostra os episodios encontrados
down.mostra_episodios()
#variavel que guarda os episodios escolhidos pelo usuario
episodios = []

while True:

	ep = str(input("digite o index do ep(Q para sair.)"))

	if ep.isnumeric():

		episodios.append(down.anime_episodios[int(ep)])

	else:

		break

#chama a função para baixar o ep selecionado
thread = Thread(target=barraDeProgresso, args=(episodios))
thread.start()
down.baixar_ep(episodios)
