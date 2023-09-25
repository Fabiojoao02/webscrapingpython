
# > EXEMPLO
# - Obtendo produtos do Mercado Livre a partir de uma busca realizada pelo usuário

import requests
from bs4 import BeautifulSoup

url_base = 'https://lista.mercadolivre.com.br/'

produto_nome = input('Qual produto você deseja? ')

response = requests.get(url_base + produto_nome)

site = BeautifulSoup(response.text, 'html.parser')

produtos = site.findAll('div', attrs={
    'class': 'andes-card ui-search-result shops__cardStyles ui-search-result--core andes-card--flat andes-card--padding-16'})

for produto in produtos:
    titulo = site.find(
        'h2', attrs={'class': 'ui-search-item__title shops__item-title'})
    link = produto.find('a', attrs={
                        'class': 'ui-search-item__group__element shops__items-group-details ui-search-link'})

    real = produto.find(
        'span', attrs={'class': 'andes-money-amount__fraction'})

    centavos = produto.find('span', attrs={
                            'class': 'andes-money-amount__cents andes-money-amount__cents--superscript-16'})

    # print(produto.prettify())
    print('Titulo do produto:', titulo.text)
    if link:
        print('Link do produto:', link['href'])
    if real:
        if centavos:
            print('preço do produto: R$', real.text + ',' + centavos.text)
        else:
            print('preço do produto: R$', real.text + ',00')

    print('\n\n')
