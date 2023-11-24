import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from datetime import datetime
import schedule
from pathlib import Path
import shutil
import os
import math
import re
from alertablusituacaoatual import situacaatual_alertablu

CAMINHO_ORIGEM = Path(__file__).parent.parent

arquivo = 'telemetriaAlertBlu.csv'
# origem
caminho_origem = CAMINHO_ORIGEM / arquivo

# print(CAMINHO_ORIGEM)

# remove arquivo
try:
    os.remove(caminho_origem)
except:
    print("no arquivo")

today = datetime.now()
print("data e hora: ", today)


# def telemetriablu():

today = datetime.now()
print("data e hora: ", today)

# Configuração inicial
url = 'https://alertablu.blumenau.sc.gov.br/d/nivel-do-rio'
headers = {
    'user-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}


# Aguarde alguns segundos para garantir que a página seja carregada
options = webdriver.ChromeOptions()
# options.headless = False
options.add_argument('--headless')
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=options)

driver.get(url)

sleep(2)

# Localiza o botão usando XPath
try:
    elemento = driver.find_element(
        By.XPATH, '//*[@id="alerta-modal"]/div/div/div[3]/button')
    elemento.click()
    print("alert accepted")
except:
    print("no alert")


site = BeautifulSoup(driver.page_source, 'html.parser')

# print(site.prettify())
# Procurando a tabela da página
# em html uma tabela é representada pela tag <table>
table = site.find('table', id='river-level-table')
# Estrutura de dados para armazenar os resultados
# Definindo dataframe
dados_telemetria = []

for row in table.tbody.find_all('tr'):

    columns = row.find_all('td')
    if (columns != []):
        posicao = row.find('i', attrs={'class': 'fa-arrow-up'})
        if posicao:
            posicao = 'SUBINDO'
        else:
            posicao = 'DESCENDO'

        leitura = columns[0].text.strip()
        nivel = columns[1].text.strip()
        variacao = columns[2].text.strip()
        if variacao == '0,00' or variacao == '-':
            posicao = 'NORMAL'
        dados_telemetria.append([
            leitura, nivel, variacao, posicao
        ])
        print('Leitura: ', leitura)
        print('nivel: ', nivel)
        print('variacao: ', variacao)
        print('posicao: ', posicao)
#    print(i)
# Se o arquivo já existe, leia-o primeiro
try:
    dados_existente = pd.read_csv('telemetriaAlertBlu.csv', sep=';')
except FileNotFoundError:
    dados_existente = pd.DataFrame()

# Adicione os novos dados ao DataFrame existente
novos_dados = pd.DataFrame(dados_telemetria, columns=[
                           'Leitura', 'Nivel', 'Variacao', 'Posicao'])
#    print(i)])

# implementado para evitar msg de wannnerde colunas vazias
novos_dados = novos_dados.dropna(axis=1, how='all')

dados_final = pd.concat([dados_existente, novos_dados], ignore_index=True)

# Salve o DataFrame atualizado de volta no arquivo CSV
dados_final.to_csv('telemetriaAlertBlu.csv', sep=';', index=False)

situacaatual_alertablu()
