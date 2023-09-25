import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys
import pandas as pd

options = Options()
# options.add_argument('--headless') # navegador não abre
options.add_argument('window-size=400,800')

navegador = webdriver.Chrome(options=options)
# navegador = webdriver.Chrome()

navegador.get('https://www.airbnb.com')

sleep(2)

# input_place = navegador.find_element_by_tag_name('input')
input_place = navegador.find_element('xpath',
                                     #                                    '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/div/div/div/header/div/div[2]/div[1]/div/span[2]/button[1]/div')
                                     '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/div/div/div/header/div/div[2]/div[1]/div/span[2]/button[1]'
                                     '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/div/div/div/header/div/div[2]/div[1]/div/span[2]/button[1]/div'

                                     # '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/div/div/div/header/div/div[2]/div[1]/div/span[2]/button[1]'
                                     )
input_place.send_keys('São Paulo')
sleep(0.5)
input_place.send_keys(Keys.ENTER)
# input_place.submit()


sleep(0.5)

button_stay = navegador.find_element_by_css_selector('button > img')
button_stay.click()

sleep(0.5)

nextButton = navegador.find_elements_by_tag_name('button')[-1]
nextButton.click()

sleep(0.5)

# Definindo dois adultos
adultButton = navegador.find_elements_by_css_selector(
    'button > span > svg > path[d="m2 16h28m-14-14v28"]')[0]
adultButton.click()
sleep(1)
adultButton.click()
sleep(1)


searchButton = navegador.find_elements_by_tag_name('button')[-1]
searchButton.click()

sleep(4)

page_content = navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')

dados_hospedagens = []

hosptedagens = site.findall('div', attrs={'itemprop': 'itemListElement'})

for hosptedagem in hosptedagens:

    # print(hosptedagem.prettify())

    hosptedagem_descricao = hosptedagem.find(
        'meta',  attrs={'itemprop': 'name'})
    hosptedagem_url = hosptedagem.find('meta',  attrs={'itemprop': 'url'})

    hosptedagem_descricao = hosptedagem_descricao['content']
    hosptedagem_url = hosptedagem_url['content']

    print('Descrição: ', hosptedagem_descricao)
    print('URL: ', hosptedagem_url)

    hosptedagem_detalhes = hosptedagem.find(
        'div',  attrs={'style': 'margin-bottom: 2px;'}).find_all('li')

    hosptedagem_detalhes = ''.join(
        [detalhe.text for detalhe in hosptedagem_detalhes])

    print('Detalhes da hopedagem: ', hosptedagem_detalhes)

    preco = hosptedagem.findall('span')[-1].text

    print('preço da hopedagem: ', preco)

    print()

    dados_hospedagens.append([
        hosptedagem_descricao, hosptedagem_url, hosptedagem_detalhes, preco
    ])

print(pd.DataFrame(dados_hospedagens, columns=[
      'Descricao', 'URL', 'Detalhes', 'Preço']))

dados = pd.DataFrame(dados_hospedagens, columns=[
    'Descricao', 'URL', 'Detalhes', 'Preço'])

dados.to_csv('hospedagens.csv', index=False)
