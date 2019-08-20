from robobrowser import RoboBrowser
import re

#instancia o RoboBrowser, seta o parser como html.parser para que analise o html
browser = RoboBrowser(history=True, parser="html.parser")
#faz a requisição do site
browser.open("https://animedir.com.br/", method="get")

#procura e envia o nome do anime que foi passado
form = browser.get_form(id="form-search-resp")
form['s'].value = "black clover"
browser.submit_form(form)

#procura a div que contem o anime
texto = browser.find_all("div", "title")

#pega o primeiro link resultado da busca.
link = texto[0].a["href"]

#abre o novo link, esse link leva pra pagina de episódios
browser.open(link, method="get")

