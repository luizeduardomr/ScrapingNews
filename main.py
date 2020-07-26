import src.verify  ### Baixa os arquivos para o selenium


### Termos de pesquisa
query = 'corona virus'

### Escolhe os sites
sites = [
	'folha',
	#'estadao'
]

### Qtd max de resultados
amount = 5 ## 0 ou False para "o maximo possivel"




### Começa as pesquisas
results = []
for site in sites:

	### Carrega os scripts de cada site
	if 'folha' in site.lower():
		import src.folhasp as site_atual
	elif 'estadao' in site.lower():
		import src.estadao as site_atual
	else:
		raise ValueError('Site Invalido')

	### Realiza a pesquisa
	for search_result in site_atual.search(query=query, limit=amount):
		results.append(search_result)







### Salva os resultados
import json
## tmp
with open('dump.json', 'w') as outfile:
	outfile.write(json.dumps(results))
	## Por enquanto soh escreve um json tmp com uma
	#     lista de resultados, onde cada resultado
	#     tem as chaves
	#          - descr    ==> resumo da noticia
	#          - title    ==> titulo da noticia
	#          - link     ==> link do artigo da noticia
	#          - date     ==> data de publicacao
	#          - content  ==> corpo da noticia
	##