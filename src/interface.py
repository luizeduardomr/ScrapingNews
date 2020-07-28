import os
import PySimpleGUI as sg

sg.change_look_and_feel('DarkAmber')  # colour

# layout of window
layout = [
    [sg.Frame(layout=[
        [sg.Radio('1. Estadao', 1, default=False, key='estadao'),
         sg.Radio('2. Folha', 1,
                     default=False, key='folha'),
         sg.Radio('3. Uol Notícias', 1, default=False, key='uol')]],
        title='Selecione o site para a pesquisa', title_color='white',
        relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
    [sg.Text('Nome do arquivo:'), sg.InputText(key='nomearquivo')],
    [sg.Text('Palavras chaves:'), sg.InputText(key='palavrachave')],
    [sg.Text('Quantidade de resultados:'), sg.InputText(key='quantidade')],
    [sg.Submit('Pesquisar'), sg.Button('Cancelar')],
]

window = sg.Window('Mudanças Climáticas Search', layout)  # make the window

event, values = window.read()


def Iniciar():
    nomearquivo = values['nomearquivo']
    palavrachave = values['palavrachave']
    quantidade = values['quantidade']
    count = 0
    while count == 0:
        if event in (None, 'Cancelar'):
            count+=1
            return 'Cancelou o programa'
        elif values['estadao'] == True:
            opcao = 'estadao'
            count+=1
        elif values['folha'] == True:
            opcao = 'folha'
            count+=1
        elif values['uol'] == True:
            opcao = 'uol'
            count+=1
    return nomearquivo, palavrachave, opcao, quantidade
    window.close()