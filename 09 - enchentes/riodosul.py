import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

navegador = webdriver.Chrome()
navegador.get('https://telemetria.riodosul.sc.gov.br/home')
sleep(6)

#rio1 = navegador.find_element('xpath','//*[@id="gmimap12"]/area')
#rio2 = navegador.find_element('xpath','//*[@id="gmimap12"]/area')

#rio1.click()

#//*[@id="dropdownMenu"]

#//*[@id="dropdownMenu"]
#mapa = navegador.find_element('xpath', '//*[@id="stationUL"]')
#mapa = navegador.find_element('xpath', '//*[@id="dropdownMenu"]')
#sleep(8)
#mapa.click()

#print(mapa)


#print(itens_menu)
#for i in range(2, len(itens_menu)):
#    while True:
#        try:
#            elemento_menu = navegador.find_element(By.XPATH, f'//*[@id="stationUL"]/li[{i}]/a')
#            print(elemento_menu.text)
#            #elemento_menu.click()
#
#            # Coloque o código para lidar com o conteúdo após clicar no item do menu aqui
#
#            sleep(2)
#            i += 1  # Avança para o próximo índice
#        except NoSuchElementException:
#            break  # Sai do loop while quando não houver mais elementos no menu

# Encontre todos os itens do menu
#itens_menu = mapa.find_elements(By.TAG_NAME, 'li')

itens_menu = navegador.find_elements(By.XPATH, '//*[@id="gmimap8"]/area') + \
    navegador.find_elements(By.XPATH, '//*[@id="gmimap10"]/area') + \
    navegador.find_elements(By.XPATH, '//*[@id="gmimap9"]/area')
                                                                                                    
#print(itens_menu)
sleep(5)

for lista in itens_menu:
    #print(lista.get_attribute("outerHTML"))
    #print(elemento_menu.text)
    lista.click()
    sleep(15)
    page_content = navegador.page_source

    site = BeautifulSoup(page_content, 'html.parser')

    dash_rio = site.find('div', attrs={'class': 'panel panel-info'})

    #print(dash_rio.prettify())

    nome_rio = dash_rio.find('h3', attrs={'class': 'panel-title pull-left'})
    print(nome_rio.text)
    #nivel rio
    nivel_rio = dash_rio.find('div', attrs={'class': 'sensor_title'})
    print('Nivel Rio: ',nivel_rio.text)
    vlr_nivel_rio = dash_rio.find('span', style='font-size: 30px; font-weight: bold; line-height: 56px;')
    print('valor Nivel Rio: ',vlr_nivel_rio.text)
    uni_nivel_rio = dash_rio.find('span', style='font-size:12px')
    print('Unidade de medida: ', uni_nivel_rio.text)

 #name="total" style="width: 95px; display: block;

    #chuva
    chuva_total = 'Chuva'
    vlr_chuva = dash_rio.find('span', style='font-weight: bold;display: inline-block;width: 45px;text-align: right;font-size: 18px;padding-top: 6px;')
    print('Valor chuva: ',vlr_chuva.text)
    uni_chuva = 'mm'
    print('Unidade ',uni_chuva)

    #Temperatura
    temp = 'Temperatura'
    vlr_temp = dash_rio.find('div', style="font-size: 30px; font-weight: bold; padding-right: 4px; vertical-align: middle; line-height: 56px;" )
    print('Temperatura: ',vlr_temp.text)
    uni = 'Graus'

    #Umidade
    temp = 'Umidade'
    vlr_umidade = dash_rio.find('div',  {'name': 'humidity'})
    print('Umidade: ',vlr_umidade.text)
    uni = '%'


    #Pressão Atmosférica
    temp = 'Pressão Atmosférica'
    vlr_pressao= dash_rio.find('span', style="font-weight: bold;display: inline-block;width: 60px;text-align: right;font-size: 18px;padding-top: 6px;")
    print('Pressão : ',vlr_pressao.text)
    uni = 'hPa'
    status= dash_rio.find('div', {'name': 'status'})
    print('Status: ',status.text)
    

    #Vento
    temp = 'Vento'
    vlr_vento = dash_rio.find('span', style="font-weight: bold;display: inline-block;width: 50px;text-align: right;font-size: 18px;padding-top: 6px;" )
    print('Vento: ',vlr_vento.text)
    unidade =  'km/h'
    direcao= dash_rio.find('div', style="text-align:right;padding-right: 4px;font-weight:bold")
    print('Vento direção: ',direcao.text)



#print(nome_rio.text)




#for ocorrencia in dash_rio:
 #   print(ocorrencia)

#'''
#texto_chuva = site.find('div', attrs={'class': 'sensor_title'})

#volume_chuva = site.find('span', style="font-weight: bold;display: inline-block;width: 45px;text-align: right;font-size: 18px;padding-top: 6px;")

#vlr_vento = site.find('span', style="font-weight:bold")
#print(vlr_vento.text)

'''

#dash_rio = site.find('div', attrs={'class': 'panel panel-info'})

#print(dash_rio.prettify())

#nome_rio = dash_rio.findall('h3', attrs={'class': 'panel-title pull-left'})
#print(nome_rio.text)

#chuva = dash_rio.find('div', attrs={'class': 'sensor_title'})
#print(chuva.text)

#chuva_vlr = dash_rio.find('span', style='font-weight: bold;display: inline-block;width: 45px;text-align: right;font-size: 18px;padding-top: 6px;')
#print(chuva_vlr.text)

#chuva_vlr = dash_rio.find('span', style='font-weight: bold;display: inline-block;width: 45px;text-align: right;font-size: 18px;padding-top: 6px;')
#print(chuva_vlr.text)




#print(nome_rio.text)

#dropdwon = navegador.find_element('xpath','//*[@id="dropdownMenu"]')

#dropdwon.click()
#sleep(5)


# HTML da notícia
#noticias = site.findAll('li', href='trocarNome(event)')

#print(site.prettify())


# # input_place = navegador.find_element_by_tag_name('input')
#                                      '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/div/div/div/header/div/div[2]/div[1]/div/span[2]/button[1]'
#                                      '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/div/div/div/header/div/div[2]/div[1]/div/span[2]/button[1]/div'

#                                      # '/html/body/div[5]/div/div/div[1]/div/div[2]/div[1]/div/div/div/header/div/div[2]/div[1]/div/span[2]/button[1]'
#                                      )
# input_place.send_keys('São Paulo')
# sleep(0.5)
# input_place.send_keys(Keys.ENTER)
# # input_place.submit()


# sleep(0.5)

# button_stay = navegador.find_element_by_css_selector('button > img')
# button_stay.click()

# sleep(0.5)

# nextButton = navegador.find_elements_by_tag_name('button')[-1]
# nextButton.click()

# sleep(0.5)

# # Definindo dois adultos
# adultButton = navegador.find_elements_by_css_selector(
#     'button > span > svg > path[d="m2 16h28m-14-14v28"]')[0]
# adultButton.click()
# sleep(1)
# adultButton.click()
# sleep(1)


# searchButton = navegador.find_elements_by_tag_name('button')[-1]
# searchButton.click()

# sleep(4)

# page_content = navegador.page_source

# site = BeautifulSoup(page_content, 'html.parser')

# print(site.prettify())
'''
