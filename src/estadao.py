from browser import *
import time

def search(query, limit=False):
	if not limit:
		limit = float('inf')

	br = GLOBAL_BR  
	### Realiza a busca
	br.get('https://busca.estadao.com.br/?tipo_conteudo=Notícias&quando=&q={}'.format(query.replace(' ', '+')))

	### Tenta ja expandir a primeira vez os resultados
	### O primeiro botao de "carregar mais" se comporta
	##     diferente dos demais
	try:
		CLICK('/html/body/section[4]/div/section[1]/div/section[2]/div/a')
	except:
		pass

	data = []

	i = 0
	while i < limit:
		i+=1

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
		date = TXT(f'/html/body/section[4]/div/section[1]/div/div/section[1]/div/div[2]/section[{i}]/span[2]')
		link  = el.get_attribute('href')
		title = el.get_attribute('title')

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

		br.get(link)
		time.sleep(.5)

		content = TXT('//*[@id="sw-wpn_41_253283"]/div/section/div/section[1]').replace('\n', ' ')
		data[i]['content'] = content

	return data
