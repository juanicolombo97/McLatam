# -------------------------------------- LIBRERIAS ----------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

ANIO_INVALIDO = 2022


def main():
    url_pagina = 'https://oei.int/contrataciones'

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

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "status")))
    filtro_estado = driver.find_element(By.XPATH, "//*[@id=\"status\"]")
    Select(filtro_estado).select_by_visible_text("Abierto / En proceso")

    buscar = driver.find_element(By.XPATH, "//button[contains(text(), 'Buscar')]")
    buscar.click()
    index = 0
    pagina_siguiente = True

    while pagina_siguiente:
        # Esperamos que cargue la tabla
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "offerstable")))

        # Obtenemos la tabla de la pagina
        tabla = driver.find_element(By.XPATH, "//*[@id=\"offerstable\"]/tbody")

        # Obtenemos las filas de la tabla
        filas = tabla.find_elements(By.TAG_NAME, "tr")

        # Obtenemos el numero de filas
        num_filas = len(filas)
        print('Numero de filas: ' + str(num_filas))

        # Hacemos for por cada fila
        for numero_fila in range(0, int(num_filas)):
            print('Fila actual: ' + str(numero_fila))

            # Iniciamos datos de la fila
            oficina = ''
            referencia = ''
            titulo = ''
            fecha = ''
            estado = ''

            # Obtenemos las filas
            filas = tabla.find_elements(By.TAG_NAME, "tr")

            # Obtenemos la fila actual
            fila_actual = filas[numero_fila]

            # Obtenemos los datos de la fila
            datos_fila = fila_actual.find_elements(By.TAG_NAME, "td")

            # Obtenemos la oficina de la fila
            oficina = datos_fila[0].text
            print('Oficina: ' + oficina)

            # Obtenemos la referencia de la fila
            referencia = datos_fila[1].text
            print('Referencia: ' + referencia)

            # Obtenemos el titulo de la fila
            titulo = datos_fila[2].text
            print('Titulo: ' + titulo)

            # Obtenemos la fecha
            fecha = datos_fila[3].text
            anio = fecha.split('/')[2]
            if int(anio) < ANIO_INVALIDO:
                print('Fecha invalida')
                pass

            # Obtenemos el estado de la fila
            estado = datos_fila[4].text
            print('Estado: ' + estado)

            print('__________________')

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Rechazar')]")))
            rechazar = driver.find_element(By.XPATH, "//button[contains(text(), 'Rechazar')]")
            driver.execute_script("arguments[0].scrollIntoView();", rechazar)
            rechazar.click()
            print("click rechazar")
        except Exception:
            pass

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Siguiente')]")))
            siguiente = driver.find_element(By.XPATH, "//a[contains(text(), 'Siguiente')]")
        except Exception:
            pagina_siguiente = False
            print("Ultima pagina")
            break

        siguiente.click()
        print("click siguiente")
        time.sleep(7)
        index += 1


if __name__ == '__main__':
    main()