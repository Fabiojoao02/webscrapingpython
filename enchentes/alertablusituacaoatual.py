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
import json


def situacaatual_alertablu():

    CAMINHO_ORIGEM = Path(__file__).parent.parent

    arquivo = 'alertablusituacaoatual.json'
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
    # table = site.find('table', id='river-level-table')
    # Estrutura de dados para armazenar os resultados
    # Definindo dataframe
    dados_telemetria = []

    table = site.find_all(
        # 'table', attrs={'class': 'table table-condensed table-bordered'})
        'div', attrs={'class': 'widget side_situacaoatual'})

    header = site.find(
        'table', attrs={'class': 'table table-condensed table-bordered'})

    # print(header.prettify())
    vlr_nivel = header.find('th',
                            class_="text-center").text.strip()

    # print(table.prettify())
    side_situacaoatual = site.find(
        'div', attrs={'class': 'widget side_situacaoatual'})

    sit_publica = side_situacaoatual.find_all('p')

    df = pd.DataFrame(columns=['msg', 'Nome Rio', 'Nivel', 'Situacao Rio',
                      'Condições de Chuva', 'Condições de Deslizamento'])

    # for i in sit_publica:
    #   print('Publicado: ', i.text.strip())
    resultado = ' '.join([i.text.strip() for i in sit_publica])
    print(resultado)

    # df = pd.concat([df, pd.DataFrame.from_records([{'msg': i.text.strip()}])
    #                  ])

    print('Nivel Rio: ', vlr_nivel)
    # df = pd.concat([df, pd.DataFrame.from_records([{'Nome Rio': nome_rio, 'Nivel': vlr_nivel}])
    #               ])

    for row in table:

        columns = row.find_all('td')
        nome_rio = columns[0].text.strip()
        obs = columns[1].text.strip()
        # Condições de chuvas
        central_chuva = columns[2].text.strip()
        vlr_central_chuva = columns[3].text.strip()
        leste_chuva = columns[4].text.strip()
        vlr_leste_chuva = columns[5].text.strip()
        norte_chuva = columns[6].text.strip()
        vlr_norte_chuva = columns[7].text.strip()
        oeste_chuva = columns[8].text.strip()
        vlr_oeste_chuva = columns[9].text.strip()
        sul_chuva = columns[10].text.strip()
        vlr_sul_chuva = columns[11].text.strip()

        # Condições de deslizamentos
        central_deslizamento = columns[12].text.strip()
        vlr_central_deslizamento = columns[13].text.strip()
        leste_deslizamento = columns[14].text.strip()
        vlr_leste_deslizamento = columns[15].text.strip()
        norte_deslizamento = columns[16].text.strip()
        vlr_norte_deslizamento = columns[17].text.strip()
        oeste_deslizamento = columns[18].text.strip()
        vlr_oeste_deslizamento = columns[19].text.strip()
        sul_deslizamento = columns[20].text.strip()
        vlr_sul_deslizamento = columns[21].text.strip()

        # Criar estrutura de dicionário para condições de chuva
        chuva_dict = {
            'central_chuva': {'chuva': central_chuva, 'valor': vlr_central_chuva},
            'leste_chuva':   {'chuva': leste_chuva, 'valor': vlr_leste_chuva},
            'norte_chuva':   {'chuva': norte_chuva, 'valor': vlr_norte_chuva},
            'oeste_chuva':   {'chuva': oeste_chuva, 'valor': vlr_oeste_chuva},
            'sul_chuva':     {'chuva': sul_chuva, 'valor': vlr_sul_chuva},
        }

        # Criar estrutura de dicionário para condições de deslizamento
        deslizamento_dict = {
            'central_deslizamento': {'deslizamento': central_deslizamento, 'valor': vlr_central_deslizamento},
            'leste_deslizamento':   {'deslizamento': leste_deslizamento, 'valor': vlr_leste_deslizamento},
            'norte_deslizamento':   {'deslizamento': norte_deslizamento, 'valor': vlr_norte_deslizamento},
            'oeste_deslizamento':   {'deslizamento': oeste_deslizamento, 'valor': vlr_oeste_deslizamento},
            'sul_deslizamento':     {'deslizamento': sul_deslizamento, 'valor': vlr_sul_deslizamento},
        }

        # Transformar estruturas de dicionário em strings JSON
        chuva_json = json.dumps(chuva_dict)
        deslizamento_json = json.dumps(deslizamento_dict)

        # Adicionar colunas ao DataFrame
        # df['Condições de Chuva'] = chuva_json
        # df['Condições de Deslizamento'] = deslizamento_json

        df = pd.concat([df, pd.DataFrame.from_records([{'msg': resultado, 'Nome Rio': nome_rio, 'Nivel': vlr_nivel, 'Situacao Rio': obs,
                                                        'Condições de Chuva': chuva_json, 'Condições de Deslizamento': deslizamento_json
                                                        }])
                        ])

        print('Nome Rio: ', nome_rio)
        print('Observação: ', obs)
        print('Central: ', central_chuva)
        print('Valor central: ', vlr_central_chuva)
        print('Leste: ', leste_chuva)
        print('valor Leste: ', vlr_leste_chuva)
        print('Norte: ', norte_chuva)
        print('valor Norte: ', vlr_norte_chuva)
        print('Oeste: ', oeste_chuva)
        print('valor Oeste: ', vlr_oeste_chuva)
        print('Sul: ', sul_chuva)
        print('valor sul: ', vlr_sul_chuva)

        print('Central: ', central_deslizamento)
        print('Valor central: ', vlr_central_deslizamento)
        print('Leste: ', leste_deslizamento)
        print('valor Leste: ', vlr_leste_deslizamento)
        print('Norte: ', norte_deslizamento)
        print('valor Norte: ', vlr_norte_deslizamento)
        print('Oeste: ', oeste_deslizamento)
        print('valor Oeste: ', vlr_oeste_deslizamento)
        print('Sul: ', sul_deslizamento)
        print('valor sul: ', vlr_sul_deslizamento)

    # Serializar DataFrame para uma lista de dicionários
    data = df.to_dict(orient='records')
    # Salvar dados em um arquivo JSON usando a biblioteca json
    with open('alertablusituacaoatual.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    # Ler o arquivo JSON
    # with open('nome_do_arquivo.json', 'r', encoding='utf-8') as json_file:
    #   data = json.load(json_file)

    # print(df.head())
    # valor = df.at[0, 'Condições de Chuva']
    # print(valor)


situacaatual_alertablu()
