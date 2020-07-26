from src.browser import *
import time
import re


def clear(x): return re.sub('\s+', ' ', x.text.replace('\n', ' '))


def search(query, limit=False):
    if not limit:
        limit = float('inf')

    br = GLOBAL_BR
    # Realiza a busca
    br.get('https://search.folha.uol.com.br/?q={}&site=todos'.format(query.replace(' ', '+')))

    data = []

    i = 0
    c = 0
    while c < limit:
        i += 1
        c += 1

        # Tenta pegar a proxima noticia
        try:
            el = WAIT_GET(
                f'/html/body/main/div/div/form/div[2]/div/div/div[2]/ol/li[{i}]/div[3]/div/a')
        except:
            # Se nao tiver, tenta avancar para a proxima pagina
            try:
                pags = GET(
                    '//*[@id="conteudo"]/div/div/form/div[2]/div/div/div[2]/nav/ul').find_elements_by_tag_name('li')

                # Ve se ainda tem uma 'pagina seguinte'
                if pags[-1].text.strip() == '':
                    pags[-1].click()
                    i = 0
                    continue
                else:  # Senao chegou ao fim
                    break

            except:  # Nao tem pagina seguinte, eh so uma pagina de resultados
                break

        # Pega as informacoes do headline da noticia
        descr = clear(el)
        descr = descr[:descr.rindex('...')+3]

        link = el.get_attribute('href')
        title = clear(el.find_element_by_class_name('c-headline__title'))
        date = el.find_element_by_tag_name('time').get_attribute('datetime')

        # Cria o objeto da noticia no json
        data.append({
            'link': link,
            'title': title,
            'descr': descr,
            'date': date
        }
        )

    # Para cada notica, abre o artigo e puxa o conteudo
    for i in range(len(data)):
        link = data[i]['link']

        time.sleep(.5)
        br.get(link)

        try:
            content = WAIT_CLASS('c-news__body').text
        except:
            content = TXT('//*[@id="conteudo"]/div[3]')
        data[i]['content'] = content

    return data



if __name__ == '__main__':
	try:
		print(search('corona virus', 5))
	finally:
		END()

