from src.browser import *
import time

with open(os.path.join('src', 'main.js')) as infile:
	elimn_assin = infile.read()


def search(query, limit=False):
	if not limit:
		limit = float('inf')

	br = GLOBAL_BR  
	### Realiza a busca
	br.get('https://busca.estadao.com.br/?tipo_conteudo=Notícias&quando=&q={}'.format(query.replace(' ', '+')))
	br.execute_script(elimn_assin)

	### Tenta ja expandir a primeira vez os resultados
	### O primeiro botao de "carregar mais" se comporta
	##     diferente dos demais
	try:
		CLICK('/html/body/section[4]/div/section[1]/div/section[2]/div/a')
	except:
		pass

	data = []

	i = 0
	c = 0
	while c < limit:
		i+=1
		c+=1

		try:
			## Tenta pegar um 'clicavel' novo
			els = GET(f'/html/body/section[4]/div/section[1]/div/div/section[{i}]').find_elements_by_tag_name('a')
		except:
			## Se nao tiver, acabou todas as noticias
			break

		## Filtra o que eh relevante dentre um monte de 'clicaveis'
		#    para compartilhar a noticia
		el = [x for x in els if len(x.text.strip())][0]
		## Pega o texto que acompanha o 'clicavel'
		descr = el.text.replace('\n',' ')

		## Checa se o texto eh o do botao
		if descr == 'Carregar mais':
			i-=1
			el.click()
			continue

		## Pega as informacoes do headline da noticia
		link  = el.get_attribute('href')
		title = el.get_attribute('title')

		if 'emais.' in link:
			c -= 1
			continue

		try:
			date = TXT(f'/html/body/section[4]/div/section[1]/div/div/section[{i}]/div/div[2]')
		except:
			date = TXT(f'/html/body/section[4]/div/section[1]/div/div/section[{i}]/div/span[2]')

		## Cria o objeto da noticia no json
		data.append({
				'link'  : link,
				'title' : title,
				'descr' : descr,
				'date'  : date
			}
		)


	## Para cada notica, abre o artigo e puxa o conteudo
	for i in range(len(data)):
		link = data[i]['link']
		if 'emais.' in link:
			##  /html/body/div[1]/div[1]/div[2]/section/div/article/div[1]
			data[i]['content'] = 'IRRELEVANTE'
			continue

		br.get(link)
		time.sleep(1)


		try:
			content = WAIT_TXT('/html/body/section[3]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]').replace('\n', ' ')
		except:
			try:
				content = WAIT_TXT('/html/body/section[1]/section/div[2]/div[2]/section/div/div/div/section/div/section[1]').replace('\n', ' ')
			except:
				content = 'EXCLUSIVO'
		                    
		data[i]['content'] = content

	return data


if __name__ == '__main__':
	try:
		print(search('corona virus', 5))
	finally:
		END()