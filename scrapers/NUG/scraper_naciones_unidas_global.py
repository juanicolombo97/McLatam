# -------------------------------------- LIBRERIAS ----------------------------------------------------------------------
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def main():
    url_pagina = 'https://www.ungm.org/Public/Notice'

    # Opciones Chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920x1080")
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

    # Cambiar el idioma
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='wholePage']/header/ul/li[2]/button")))
    boton_idioma = driver.find_element(By.XPATH, "//*[@id='wholePage']/header/ul/li[2]/button")
    actions = ActionChains(driver)
    # Mover el mouse al elemento
    actions.move_to_element(boton_idioma).perform()
    boton_idioma.click()
    print("Click idioma")
    time.sleep(2)

    # Click sobre el idioma que queremos
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='wholePage']/header/ul/li[2]/button/../ul/li[2]/button")))

    # Ejecutar un código JavaScript para hacer click en el botón utilizando XPath
    boton_idioma_esp = driver.find_element(By.XPATH, "//*[@id='wholePage']/header/ul/li[2]/button/../ul/li[2]/button")
    driver.execute_script("arguments[0].click();", boton_idioma_esp)
    time.sleep(5)

    # Esperar que cargue
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.ID, 'mainThrobber')))

    # Clickear sobre la busqueda avanzada para poder ver los filtros
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='noticeFilter']/div[1]/div[2]/input")))
    busqueda_avanzada = driver.find_element(By.XPATH, "//*[@id='noticeFilter']/div[1]/div[2]/input")
    busqueda_avanzada.click()
    print("Click Mostrar Busqueda")

    # Seleccionar el filtro que quiero
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, 'RequestForEoi')))
    filtro = driver.find_element(By.ID, 'RequestForEoi')
    filtro.click()
    time.sleep(2)

    # Buscar
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, 'lnkSearch')))
    buscar = driver.find_element(By.ID, 'lnkSearch')
    buscar.click()

    # Esperar que cargue
    time.sleep(1)
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.ID, 'mainThrobber')))

    # Esperamos que cargue la tabla
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='tblNotices']")))
    # Obtenemos la tabla de la pagina
    tabla = driver.find_element(By.XPATH, "//*[@id='tblNotices']/div[2]")

    # Obtenemos las filas de la tabla
    filas = tabla.find_elements(By.XPATH, "div")

    # Obtenemos el numero de filas
    num_filas = len(filas)
    print('Numero de filas: ' + str(num_filas))


    # Definir las columnas que se quiere obtener datos
    columnas_deseadas = [6, 7, 8, 9, 10]
    # Hacemos for por cada fila
    for fila in filas:
        print("FILA")
        # Obtener las columnas
        columnas = fila.find_elements(By.XPATH, "div[@role='cell']")
        for col in columnas:
            try:
                print('col: ', col.text)
                span = col.find_element(By.XPATH,  'span')
                print('span: ', span.text)
                time.sleep(3)
            except Exception as e:
                pass
        return


    time.sleep(10)

if __name__ == '__main__':
    main()
