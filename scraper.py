# Importamos las dependencias que necesitaremos

import requests
import lxml.html as html 
import os 
import datetime

# Creamos constantes
HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//div/a[contains(@class, "kicker")]/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/a/text()'
XPATH_AUTHOR = '//div[@class = "autorArticle"]/p/text()'
XPATH_SUMMARY = '//div[@class= "lead"]/p/text()'
XPATH_BODY = '//div[@class= "html-content"]/p[not(@class)]/text()'

def parse_notice(link, today):
	try:
		response = requests.get(link)
		if response.status_code == 200:
			notice = response.content.decode('utf-8')
			parsed = html.fromstring(notice)

			try:
				title = parsed.xpath(XPATH_TITLE)[0] # El elemento 0 será el title. Esto puede retornar una lsita de varios elementos
				title = title.replace('\"','')
				title = title.replace('#','')
				title = title.replace('|','')

				summary = parsed.xpath(XPATH_SUMMARY)[0]
				body = parsed.xpath(XPATH_BODY)
				author = parsed.xpath(XPATH_AUTHOR)[0]
				
			except IndexError: # Hay noticias que no tienen summary. Dara index Error
				return

			with open(f'{today}/{title}.txt','w',encoding='utf-8') as f:
				f.write(title)
				f.write("\n\n")
				f.write(author)
				f.write("\n\n")
				f.write(summary)
				f.write("\n\n")
				for p in body:
					f.write(p)
					f.write('\n')

		else:
			raise ValueError(f'Error: {response.status_code}')

	except ValueError as ve:
		print(ve)


def parse_home():
	# Haremos un try except para manejar los errores
	try: 
		# request.get nos devolvera el documento html
		response = requests.get(HOME_URL) 
		# el status_code 200 quiere decir que todo salio bien
		if response.status_code == 200:
			# En el documento html de la respuesta, transformaremos
			# todos los caracteres especiales en algo que python puede leer perfectamente
			home = response.content.decode('utf-8')
			parsed = html.fromstring(home) # Toma el contenido html dentro de home en texto y lo transforma en un doc especial
										   # donde puedo hacer XPATH
			links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE) # Obtenemos el resultado de aplicar xpath (Una lista de links)
			#For debug
			#print(links_to_notices)
			#print(len(links_to_notices))

			#Obtenemos la fecha de hoy y le asignamos un formato en string como deseamos: dia-mes-año
			today = datetime.date.today().strftime('%d-%m-%Y')
			if not os.path.isdir(today):
				os.mkdir(today)




			for link in links_to_notices:
				parse_notice(link, today)

			
		else: 
			# Si el codigo es otro, tuvimos un problema. lo 
			# manejaremos con el except haciendo que salga un
			# ValueError que nos diga el codigo del error
			raise ValueError(f'Error: {response.status_code} ')
	except ValueError as ve:
		print(ve)

def run():
	parse_home()


if __name__ == '__main__':
	run()
