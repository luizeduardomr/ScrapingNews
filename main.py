import os  # importa o sistema
import json
import csv  # importa o CSV para gerar arquivos
import src.verify  # Baixa os arquivos para o selenium
import re
import traceback
import json
from src.interface import Iniciar

"""
# Termos de pesquisa
query = 'corona virus'

# Escolhe os sites
sites = [
    'folha',
    # 'estadao'
]

# Nome do arquivo
arquivo = "teste"

# Qtd max de resultados
amount = 5  # 0 ou False para "o maximo possivel"
"""
nomearquivo, palavrachave, opcao, quantidade = Iniciar()


# Começa as pesquisas
results = []
"""
for site in sites:

    # Carrega os scripts de cada site
    if 'folha' in site.lower():
        import src.folhasp as site_atual
    elif 'estadao' in site.lower():
        import src.estadao as site_atual
    else:
        raise ValueError('Site Invalido')
"""

if opcao == 'folha':
	import src.folhasp as site_atual
elif opcao == 'esadao':
    import src.estadao as site_atual
else:
	raise ValueError('Site Invalido')


    # Realiza a pesquisa
for search_result in site_atual.search(query=palavrachave, limit=int(quantidade)):
	results.append(search_result)


# Faz a criação da pasta resultados
dir_path = os.path.join('./resultados', nomearquivo)
if not os.path.exists('./resultados'):
    os.makedirs('./resultados')

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

with open('{}.csv'.format(os.path.join(dir_path, "resultados_da_pesquisa")), 'w',  encoding='utf-8') as csv_file:
    for res in results:
        csv_file.write(res['title'] + '\t' + res['date'] + '\t' + res['link'])
        csv_file.write('\n')
        arquivotxt = re.sub('\W', '_', res['title'])
        with open('{}.txt'.format(os.path.join(dir_path, arquivotxt[:40])), 'w', encoding='utf-8') as text:
            try:
                content = res['content']
            except KeyError:
                content = "Algo deu errado"
            text.write(content)
with open('{}.txt'.format(os.path.join(dir_path, "Parâmetros_de_pesquisa")), 'w', encoding='utf-8') as text:
    text.write(
        f"Palavras Chaves: {palavrachave}\nNome do arquivo: {nomearquivo}\nSite: {opcao}\nNumero de pesquisas: {quantidade}\n")
		


# Salva os resultados
# tmp
"""
with open('dump.json', 'w') as outfile:
    outfile.write(json.dumps(results))
    # Por enquanto soh escreve um json tmp com uma
    #     lista de resultados, onde cada resultado
    #     tem as chaves
    #          - descr    ==> resumo da noticia
    #          - title    ==> titulo da noticia
    #          - link     ==> link do artigo da noticia
    #          - date     ==> data de publicacao
    #          - content  ==> corpo da noticia
    ##
"""
