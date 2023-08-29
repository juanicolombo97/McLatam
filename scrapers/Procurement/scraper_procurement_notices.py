# ------------------------------------- LIBRERIAS ---------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from scrapers.firebase import obtener_ids_PROCUREMENT, agregar_datos_PROCUREMENT

LISTA_PAISES_INVALIDOS = [
    'AFGHANISTAN', 'ALGERIA', 'BANGLADESH', 'BHUTAN', 'BOTSWANA', 'DJIBOUTI', 'EGYPT', 'FIJI', 'GABON', 'IRAQ',
    'JORDAN',
    'THAILAND', 'LAO PDR', 'LIBYA', 'MALAWI', 'MALI', 'NEPAL', 'SRI LANKA', 'KYRGYZSTAN', 'UZBEKISTAN', 'MADAGASCAR',
    'PAKISTAN', 'PHILIPPINES', 'SOMALIA', 'TUNISIA', 'TURKMENISTAN', 'UGANDA', 'UKRAINE', 'UNITED STATES OF AMERICA',
    'YEMEN'
]


def main():
    url_pagina = 'https://procurement-notices.undp.org/search.cfm'

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
    driver = webdriver.Chrome(executable_path='/Users/mickyconca/Desktop/McLatam/scrapers/chromedriver', options=options)

    # Abrimos la pagina
    driver.get(url_pagina)

    # Llamamos funcion que inicia el scrapeo
    obtener_datos_tabla(driver)


# Funcion que obtiene los datos de la tabla
def obtener_datos_tabla(driver):
    print('Iniciando scrapeo Procurement')

    # Obtenemos ids que ya se guardaron
    ids_referencia = obtener_ids_PROCUREMENT()
    print(ids_referencia)

    # Esperamos que cargue el buscador
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//form[@name='search_form']")))

    # Hacemos click sobre el select de los filtros
    filtros = driver.find_element(By.XPATH, "//select[@name='cur_sm_id']")
    filtros.click()
    time.sleep(.5)
    filtro_eoi = filtros.find_element(By.XPATH, "option[7]")
    filtro_eoi.click()

    boton_buscar = driver.find_element(By.XPATH, "//a[@class='adminbutton-blue']")
    boton_buscar.click()

    # Esperamos que cargue la tabla
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//table[@class='standard cellborder']")))

    # Obtenemos la tabla de la pagina
    tabla = driver.find_element(By.XPATH, "//table[@class='standard cellborder']/tbody")

    # Obtenemos las filas de la tabla
    filas = tabla.find_elements(By.TAG_NAME, "tr")

    # Obtenemos el numero de filas
    num_filas = len(filas)
    print('Numero de filas: ' + str(num_filas))

    # Hacemos for por cada fila
    for numero_fila in range(1, len(filas)):
        print('FILA ACTUAL: ' + str(numero_fila))

        # Esperamos que cargue la tabla
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//table[@class='standard cellborder']")))

        # Iniciamos datos de la fila
        numero_referencia = ''
        titulo = ''
        oficina = ''
        pais = ''
        proceso = ''
        fecha_hasta = ''
        fecha_publicacion = ''

        # Obtenemos las filas
        filas = tabla.find_elements(By.TAG_NAME, "tr")

        # Obtenemos la fila actual
        fila_actual = filas[numero_fila]

        # Obtenemos los datos de la fila
        datos_fila = fila_actual.find_elements(By.TAG_NAME, "td")

        # Obtenemos el numero_referencia de la fila
        numero_referencia = datos_fila[2].text
        print('Referencia: ' + numero_referencia)

        if ids_referencia is not None and numero_referencia in ids_referencia:
            print("Ya existe")
            continue

        # Obtenemos el titulo de la fila
        titulo = datos_fila[3].text
        print('Titulo: ' + titulo)

        # Obtenemos la oficina de la fila
        oficina = datos_fila[4].text
        print('Oficina: ' + oficina)

        # Obtenemos el pais de la fila
        pais = datos_fila[5].text
        print('Pais: ' + pais)

        # Nos fijamos si el titulo es malo o no
        if not pais_valido(pais):
            print('************* Pais invalido *************')
            continue

        # Obtenemos el proceso de la fila
        proceso = datos_fila[6].text
        print('Proceso: ' + proceso)

        # Obtenemos la fecha hasta de la fila
        fecha_hasta = datos_fila[7].text
        print('Fecha hasta: ' + fecha_hasta)

        # Obtenemos la fecha publicacion de la fila
        fecha_publicacion = datos_fila[8].text
        print('Fecha publicacion: ' + fecha_publicacion)

        agregar_datos_PROCUREMENT(numero_referencia, titulo, oficina, pais, proceso, fecha_hasta, fecha_publicacion)


def pais_valido(pais):
    # Hacemos for por cada titulo malo
    for pais_invalido in LISTA_PAISES_INVALIDOS:
        if pais_invalido in pais:
            return False

    return True


if __name__ == '__main__':
    main()
