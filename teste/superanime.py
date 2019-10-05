import requests
from bs4 import BeautifulSoup as bs

nome_anime = str(input("digite o nome do anime: ")).replace(" ", "+")

conexao = requests.get(f"https://www.superanimes.org/busca?parametro={nome_anime}")
texto = bs(conexao.text, "html.parser")
link = texto.find_all("article")[0].h1.a["href"]
conexao = requests.get(link)
texto = bs(conexao.text, "html.parser")
print(texto.find_all("div", "epsBox"))

