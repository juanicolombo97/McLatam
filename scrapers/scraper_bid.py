
#-------------------------------------- LIBRERIAS ----------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from datetime import date, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from twocaptcha import TwoCaptcha
import time
import os
import sys


LISTA_TITULOS_MALOS = [
    'LGTBI+'
]

def main():

    url_pagina = 'https://beo-procurement.iadb.org/home'

    # Opciones Chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("start-maximized")
    options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'plugins.always_open_pdf_externally': True  # Abrir PDF en lugar de descargar
    })


    # Obtenemos el driver
    driver = webdriver.Chrome(executable_path='chromedriver',  chrome_options=options)

    # Abrimos la pagina
    driver.get(url_pagina)

    # Llamamos funcion que inicia el scrapeo
    obtener_datos_tabla(driver) 


# Funcion que obtiene los datos de la tabla
def obtener_datos_tabla(driver):
    print('Iniciando scrapeo')

    # Esperamos que cargue la tabla
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Title of Consultancy')]/../../../tbody")))

    # Obtenemos la tabla de la pagina
    tabla = driver.find_element(By.XPATH, "//th[contains(text(), 'Title of Consultancy')]/../../../tbody")
                    
    # Obtenemos las filas de la tabla
    filas = tabla.find_elements(By.TAG_NAME, "tr")

    # Obtenemos el numero de filas
    num_filas = len(filas) / 2
    print('Numero de filas: ' + str(num_filas))

    # Hacemos for por cada fila, saltando de 2 en 2
    for numero_fila in range(0, int(num_filas), 2):
        print('Fila actual: ' + str(numero_fila))

        # Iniciamos datos de la fila
        id_fila = ''
        titulo = ''
        fecha = ''
        url_id = ''


        # Obtenemos las filas
        filas = tabla.find_elements(By.TAG_NAME, "tr")

        # Obtenemos la fila actual
        fila_actual = filas[numero_fila]

        # Obtenemos los datos de la fila
        datos_fila = fila_actual.find_elements(By.TAG_NAME, "td")

        # Obtenemos el id de la fila
        id_fila = datos_fila[1].text
        print('ID: ' + id_fila)

        # Obtenemos el titulo de la fila
        titulo = datos_fila[2].text
        print('Titulo: ' + titulo)

        # Nos fijamos si el titulo es malo o no
        if not titulo_valido(titulo):
            print('Titulo invalido')
            continue

        # Obtenemos la fecha
        fecha = datos_fila[3].text.replace('\n', ' ')
        print('Fecha: ' + fecha)

        # Obtenemos el url del id
        url_id = datos_fila[1].find_element(By.TAG_NAME, "a").get_attribute('href')
        print('URL ID: ' + url_id)


# Funcion que se encarga de ver si el titulo es valido
# Devuelve True si es valido, False si no lo es
def titulo_valido(titulo):
    
    # Hacemos for por cada titulo malo
    for titulo_malo in LISTA_TITULOS_MALOS:
        if titulo_malo in titulo:
            return False

    return True 

    

 

    
    
 
if __name__ == '__main__':
    main() 
