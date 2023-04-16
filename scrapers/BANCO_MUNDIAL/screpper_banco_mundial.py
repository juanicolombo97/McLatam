# -------------------------------------- LIBRERIAS ----------------------------------------------------------------------
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

LISTA_PAISES_INVALIDOS = [
    'Brazil'
]

LISTA_IDIOMAS_VALIDOS = [
    'Spanish',
    'Castillan'
]


def main():
    url_pagina = 'https://projects.worldbank.org/en/projects-operations/procurement?lang=en&qterm=&showrecent=true&srce=notices'

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
    driver = webdriver.Chrome(executable_path='../chromedriver', options=options)

    # Abrimos la pagina
    driver.get(url_pagina)

    # Llamamos a la funcion que agrega los filtros
    # TODO
    # aplicar_filtros(driver)

    # Llamamos funcion obtiene los datos
    obtener_datos_tabla(driver)


# Funcion que aplica filtros a la tabla
def aplicar_filtros(driver):
    # Esperamos que cargue el filter
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//h4[text()='Filter']")))


# Funcion que obtiene los datos de la tabla
def obtener_datos_tabla(driver):
    print('Iniciando scrapeo')

    # Esperamos que cargue la tabla
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Description')]/../../../tbody")))

    # Obtenemos la tabla de la pagina
    tabla = driver.find_element(By.XPATH, "//th[contains(text(), 'Description')]/../../../tbody")

    # Obtenemos las filas de la tabla
    filas = tabla.find_elements(By.TAG_NAME, "tr")

    # Recorremos las filas
    for numero_fila in range(0, int(len(filas))):
        print('Fila actual: ' + str(numero_fila))
        # Iniciamos datos de la fila
        pais = ''
        idioma = ''
        fecha_publicacion = ''

        # Obtenemos los datos de la fila
        datos_fila = filas[numero_fila].find_elements(By.TAG_NAME, "td")

        # Obtenemos el pais de la fila
        pais = datos_fila[1].text
        print('pais: ' + pais)

        # Nos fijamos si el pais es valido
        if not elemento_valido(pais, LISTA_PAISES_INVALIDOS):
            print('Pais invalido')
            continue

        # Obtenemos el idioma
        idioma = datos_fila[4].text
        print('idioma: ' + idioma)

        # Nos fijamos si el idioma es valido
        if elemento_valido(idioma, LISTA_IDIOMAS_VALIDOS):
            print('Idioma invalido')
            continue

        # Obtenemos la fecha
        fecha = datos_fila[5].text.replace('\n', ' ')
        print('Fecha: ' + fecha)


# Funcion que se encarga de ver si un elemento es valido
# Devuelve True si es valido, False si no lo es
def elemento_valido(elemento, lista_invalida):
    # Hacemos for por cada elemento invalido
    for elemento_invalido in lista_invalida:
        if elemento_invalido in elemento:
            return False
    return True


if __name__ == '__main__':
    main()
