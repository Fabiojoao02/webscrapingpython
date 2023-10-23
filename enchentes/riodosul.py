import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from datetime import datetime
import schedule
# import time

today = datetime.now()
print("data e hora: ", today)



def telemetria():

    today = datetime.now()
    print("data e hora: ", today)

    options = webdriver.ChromeOptions()
    options.headless = True
    # options.add_argument('--headless')

    navegador = webdriver.Chrome(options=options)
    navegador.get('https://telemetria.riodosul.sc.gov.br/home')
    sleep(6)

    itens_menu = navegador.find_elements(By.XPATH, '//*[@id="gmimap8"]/area') + \
        navegador.find_elements(By.XPATH, '//*[@id="gmimap10"]/area') + \
        navegador.find_elements(By.XPATH, '//*[@id="gmimap9"]/area')
    sleep(5)

    dados_telemetria = []

    for lista in itens_menu:
        lista.click()
        sleep(7)
        page_content = navegador.page_source
        site = BeautifulSoup(page_content, 'html.parser')
        dash_rio = site.find('div', attrs={'class': 'panel panel-info'})

        # print(dash_rio.prettify())
        nome_rio = dash_rio.find(
            'h3', attrs={'class': 'panel-title pull-left'})
        print(nome_rio.text)

        # nivel rio
        nivel_rio = dash_rio.find('div', attrs={'class': 'sensor_title'})
        print('Nivel Rio: ', nivel_rio.text)
        if nivel_rio:
            vlr_nivel_rio = dash_rio.find(
                'span', style='font-size: 30px; font-weight: bold; line-height: 56px;')
            print('valor Nivel Rio: ', vlr_nivel_rio.text)
            uni_nivel_rio = dash_rio.find('span', style='font-size:12px')
            print('Unidade de medida: ', uni_nivel_rio.text)
        # chuva
        chuva_total = dash_rio.find('div',  {'name': 'total'})
        if chuva_total:
            chuva_total = 'Chuva'
            vlr_chuva = dash_rio.find(
                'span', style='font-weight: bold;display: inline-block;width: 45px;text-align: right;font-size: 18px;padding-top: 6px;')
            print('Valor chuva: ', vlr_chuva.text)
            uni_chuva = 'mm'
            print('Unidade ', uni_chuva)

        # Temperatura
        temperatura = dash_rio.find('div',  {'name': 'temperature'})
        if temperatura:
            temperatura = 'Temperatura'
            vlr_temp = dash_rio.find(
                'div', style="font-size: 30px; font-weight: bold; padding-right: 4px; vertical-align: middle; line-height: 56px;")
            print('Temperatura: ', vlr_temp.text)
            uni_temp = 'Graus'

        # Umidade
        vlr_umidade = dash_rio.find('div',  {'name': 'humidity'})
        if vlr_umidade:
            umidade = 'Umidade'
            print('Umidade: ', vlr_umidade.text)
            uni_umidade = '%'

        # Pressão Atmosférica
        pressao = dash_rio.find('div',  {'name': 'pressure'})
        if pressao:
            pressao = 'Pressão Atmosférica'
            vlr_pressao = dash_rio.find(
                'span', style="font-weight: bold;display: inline-block;width: 60px;text-align: right;font-size: 18px;padding-top: 6px;")
            print('Pressão : ', vlr_pressao.text)
            uni_pressao = 'hPa'
            status = dash_rio.find('div', {'name': 'status'})
            print('Status: ', status.text)

        # Vento
        vento = dash_rio.find('div',  {'name': 'wind'})
        if vento:
            vento = 'Vento'
            vlr_vento = dash_rio.find(
                'span', style="font-weight: bold;display: inline-block;width: 50px;text-align: right;font-size: 18px;padding-top: 6px;")
            print('Vento: ', vlr_vento.text)
            uni_vento = 'km/h'
            direcao = dash_rio.find(
                'div', style="text-align:right;padding-right: 4px;font-weight:bold")
            print('Vento direção: ', direcao.text)

        # data e hora da leitura
        leitura = dash_rio.find('div',  attrs={'class': 'panel-footer'})

        dados_telemetria.append([
            nome_rio.text.strip(), nivel_rio.text.strip(
            ), vlr_nivel_rio.text.strip(), uni_nivel_rio.text.strip(),
            chuva_total, vlr_chuva.text.strip(), uni_chuva, temperatura,
            vlr_temp.text.strip(), uni_temp, umidade, vlr_umidade.text.strip(), uni_umidade, pressao,
            vlr_pressao.text.strip(), uni_pressao, status.text.strip(), vento, vlr_vento.text.strip(),
            uni_vento, direcao.text.strip(), leitura.text.strip()
        ])

    # Se o arquivo já existe, leia-o primeiro
    try:
        dados_existente = pd.read_csv('telemetriaRSUL.csv', sep=';')
    except FileNotFoundError:
        dados_existente = pd.DataFrame()

    # Adicione os novos dados ao DataFrame existente
    novos_dados = pd.DataFrame(dados_telemetria, columns=[
        'nome_rio', 'nivel_rio', 'vlr_nivel_rio', 'uni_nivel_rio', 'chuva_total',
        'vlr_chuva', 'uni_chuva', 'temperatura', 'vlr_temp', 'uni_temp', 'umidade',
        'vlr_umidade', 'uni_umidade', 'pressao', 'vlr_pressao', 'uni_pressao', 'status',
        'vento', 'vlr_vento', 'uni_vento', 'direcao', 'leitura'])

    dados_final = pd.concat([dados_existente, novos_dados], ignore_index=True)

    # Salve o DataFrame atualizado de volta no arquivo CSV
    dados_final.to_csv('telemetriaRSUL.csv', sep=';', index=False)



telemetria()
# Agende a tarefa para ser executada a cada 2 minutos
schedule.every(50).minutes.do(telemetria)

while True:
    schedule.run_pending()
    sleep(1)
