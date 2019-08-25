from downanime import DownAnime

down = DownAnime()
#abre o site para baixar os animes
down.abrir_site()
#pega o nome do anime para pesquisar
pesquisar = str(input("digite o nome do anime: "))
#chama a função de pesquisa
down.pesquisa(pesquisar)
#mostra os episodios encontrados
down.mostra_animes()
#escolha do anime
down.escolha_anime = int(input("escolha o index do anime: "))
#pequisa os episodios
down.episodios()
#mostra os episodios encontrados
down.mostra_episodios()
#escolha do index do ep
ep_index = int(input("escolha o index do ep: "))

#chama a função para baixar o ep selecionado
down.baixar_ep(down.anime_episodios[ep_index].a["href"], down.anime_episodios[ep_index].text)

