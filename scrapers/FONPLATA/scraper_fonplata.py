# -------------------------------------- LIBRERIAS --------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from scrapers.firebase import agregar_datos_fonplata, obtener_expediente


def main():
    url_pagina = 'https://www.fonplata.org/es/adquisiciones-en-proyectos'

    # Opciones Chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("start-maximized")
    options.add_argument(f"--window-size=1200,800")
    options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'plugins.always_open_pdf_externally': True  # Abrir PDF en lugar de descargar
    })

    driver = webdriver.Chrome(options=options)

    # Abrimos la pagina
    driver.get(url_pagina)

    # Llamamos funcion que inicia el scrapeo
    obtener_datos_tabla(driver)


# Funcion que obtiene los datos de la tabla
def obtener_datos_tabla(driver):
    print('Iniciando scrapeo FONPLATA')

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//ul[@class='nav nav-tabs']/li")))
    paises = driver.find_elements(By.XPATH, "//ul[@class='nav nav-tabs']/li")
    datos_paises = driver.find_elements(By.XPATH, "//div[@class='tab-content']/div")

    print(len(paises))

    # Recorro cada pais
    for index in range(0, len(paises)):
        print("Recorriendo paises")
        # Selecciono el pais
        pais = paises[index]
        pais.click()
        pais = pais.text
        print("pais " + pais)
        # Obtengo la clase que indica si el pais tiene contenido para mostrar
        clase = datos_paises[index].find_element(By.XPATH, "div/div/div")
        contenido = clase.get_attribute("class")
        # Chequeo que haya contenido
        if "content" in contenido:
            # Esperamos que cargue la tabla
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Modalidad')]/../../../tbody")))
            # Obtenemos la tabla de la pagina
            tabla = driver.find_element(By.XPATH, "//th[contains(text(), 'Modalidad')]/../../../tbody")

            # Obtenemos las filas de la tabla
            filas = tabla.find_elements(By.TAG_NAME, "tr")

            # Recorremos las filas
            for numero_fila in range(0, int(len(filas))):
                print('FILA ACTUAL: ' + str(numero_fila))
                # Iniciamos datos de la fila
                prestamo = ''
                modalidad = ''
                objeto = ''
                descripcion = ''
                presupuesto = ''
                fecha_publicacion = ''
                fecha_presentacion = ''

                # Obtenemos los datos de la fila
                datos_fila = filas[numero_fila].find_elements(By.TAG_NAME, "td")

                prestamo = datos_fila[0].text
                if obtener_expediente(prestamo):
                    print("Ya existe")
                    continue

                modalidad = datos_fila[1].text
                objeto = datos_fila[2].text
                descripcion = datos_fila[3].text
                presupuesto = datos_fila[4].text
                fecha_publicacion = datos_fila[5].text
                fecha_presentacion = datos_fila[6].text
                print("Prestamo " + prestamo)
                print("Modalidad " + modalidad)
                print("Objeto " + objeto)
                print("descripcion " + descripcion)
                print("presupuesto " + presupuesto)
                print("fecha_publicacion " + fecha_publicacion)
                print("fecha_presentacion " + fecha_presentacion)

                agregar_datos_fonplata(prestamo, modalidad, objeto, descripcion, presupuesto, fecha_publicacion, fecha_presentacion, pais)

        time.sleep(0.5)


if __name__ == '__main__':
    main()
