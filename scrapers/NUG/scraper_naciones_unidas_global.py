# -------------------------------------- LIBRERIAS ----------------------------------------------------------------------
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def main():
    url_pagina = 'https://www.ungm.org/Public/Notice'

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
    driver = webdriver.Chrome(executable_path='scrapers/chromedriver', options=options)

    # Abrimos la pagina
    driver.get(url_pagina)

    # Llamamos funcion que inicia el scrapeo
    obtener_datos_tabla(driver)


# Funcion que obtiene los datos de la tabla
def obtener_datos_tabla(driver):
    print('Iniciando scrapeo')

    try:
        popup = driver.find_element(By.XPATH, "//*[@id=\"languageSuggestionModal\"]/div[1]/div[1]/input[2]")
        popup.click()
    except Exception:
        pass

    # Esperamos que cargue la tabla
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='tblNotices']")))

    # Obtenemos la tabla de la pagina
    tabla = driver.find_element(By.XPATH, "//*[@id='tblNotices']/div[1]")

    # Obtenemos las filas de la tabla
    filas = tabla.find_elements(By.TAG_NAME, "div")

    # Obtenemos el numero de filas
    num_filas = len(filas)
    print('Numero de filas: ' + str(num_filas))

    # Hacemos for por cada fila
    for numero_fila in range(0, int(num_filas)):
        print('Fila actual: ' + str(numero_fila))

        # Iniciamos datos de la fila
        titulo = ''
        pais = ''

        # Obtenemos las filas
        filas = tabla.find_elements(By.TAG_NAME, "div")

        # Obtenemos la fila actual
        fila_actual = filas[numero_fila]

        # Obtenemos los datos de la fila
        datos_fila = fila_actual.find_elements(By.TAG_NAME, "div")
        print(datos_fila[0].text)
        time.sleep(10)

        # Obtenemos el titulo de la fila
        # titulo = datos_fila[1].text
        # print('Titulo: ' + titulo)


if __name__ == '__main__':
    main()
