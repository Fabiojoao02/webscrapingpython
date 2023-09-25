from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

navegador = webdriver.Chrome()

navegador.get('https://www.walissonsilva.com/blog')

sleep(3)

# elemento = navegador.find_element_by_tag_name('input')
elemento = navegador.find_element(
    'xpath', '//*[@id="__next"]/div/div/div[1]/div/input')

elemento.send_keys('data')
# Envie a tecla Enter
# elemento.send_keys(Keys.ENTER)

sleep(3)
