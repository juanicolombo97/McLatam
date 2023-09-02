# ------------------------------------- LIBRERIAS ---------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

from scrapers.firebase import agregar_datos_comunidad_andina, obtener_ids_comunidad_andina


def main():
    url_pagina = 'https://www.comunidadandina.org/convocatorias/'

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
    driver = webdriver.Chrome(options=options)

    # Abrimos la pagina
    driver.get(url_pagina)

    # Llamamos funcion que inicia el scrapeo
    obtener_datos_tabla(driver)


# Funcion que obtiene los datos de la tabla
def obtener_datos_tabla(driver):
    print('Iniciando scrapeo Comunidad Andina')

    # Obtenemos ids que ya se guardaron
    expediente_ids = obtener_ids_comunidad_andina()
    print(expediente_ids)

    # Esperamos que cargue la tabla
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='page-content page-content-fullwidth']/div")))

    # Obtenemos la tabla de la pagina
    tabla = driver.find_element(By.XPATH, "//div[@class='page-content page-content-fullwidth']")

    filas = tabla.find_elements(By.XPATH, "//div[@class='wp-block-group block-head-texts-dotted']")
    filas_totales = len(filas)
    print("Filas totales: " + str(filas_totales))
    num_fila = 1
    num_doc = 1

    for fila in filas:
        print("Fila " + str(num_fila))
        datos_fila = fila.find_element(By.XPATH, "div[@class='wp-block-group__inner-container']")

        # Iniciamos datos de la fila
        nombre = ''
        fecha_limite = ''
        hora = ''
        contacto = ''
        documentos = ''

        nombre = datos_fila.find_element(By.XPATH, "h4[1]/strong[2]").text
        print(nombre)
        if expediente_ids is not None and nombre in expediente_ids:
            num_fila += 1
            num_doc += 2
            print("Ya existe")
            continue

        fecha_limite = datos_fila.find_element(By.XPATH, "h4[2]/strong[2]").text
        print(fecha_limite)

        hora = datos_fila.find_element(By.XPATH, "h4[3]/strong[2]").text
        print(hora)

        contacto = datos_fila.find_element(By.XPATH, "div").text
        print(contacto)

        documento = fila.find_element(By.XPATH, f"../div[@class='content-2col-grid '][{num_doc}]/div/div/div[@class='di-content']/h4/a").get_attribute("href")
        print(documento)

        agregar_datos_comunidad_andina(nombre, fecha_limite, hora, contacto, documento)

        time.sleep(.5)
        num_fila += 1
        num_doc += 2


if __name__ == '__main__':
    main()
