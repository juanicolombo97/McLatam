# -------------------------------------- LIBRERIAS --------------------------------------------------------------------
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from scrapers.firebase import agregar_datos_NUG, obtener_ids_NUG

PAISES_VALIDOS = ['Haiti', 'Ecuador', 'El Salvador', 'Colombia', 'República Dominicana',
                  'Perú', 'Argentina', 'México', 'Brasil', 'Panamá', 'Paraguay', 'Chile', 'Venezuela',
                  'Cuba', 'Varias localizaciones', 'España']


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
    driver = webdriver.Chrome(options=options)

    # Abrimos la pagina
    driver.get(url_pagina)

    # Llamamos funcion que inicia el scrapeo
    obtener_datos_tabla(driver)


# Funcion que obtiene los datos de la tabla
def obtener_datos_tabla(driver):
    print('Iniciando scrapeo NUG')

    # Obtenemos ids que ya se guardaron
    ids_referencia = obtener_ids_NUG()
    print(ids_referencia)

    try:
        popup = driver.find_element(By.XPATH, "//*[@id=\"languageSuggestionModal\"]/div[1]/div[1]/input[2]")
        popup.click()
    except Exception:
        print("Except")
        pass

    # Cambiar el idioma
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='wholePage']/header/ul/li[2]/button")))
    boton_idioma = driver.find_element(By.XPATH, "//*[@id='wholePage']/header/ul/li[2]/button")
    actions = ActionChains(driver)
    # Mover el mouse al elemento
    actions.move_to_element(boton_idioma).perform()
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='wholePage']/header/ul/li[2]/button")))
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

    # Obtenemos las filas visibles de la tabla
    filas = tabla.find_elements(By.XPATH, "div")

    # Obtenemos las filas totales a scrapear
    filas_totales = driver.find_element(By.ID, "noticeSearchTotal")
    print("Filas totales: " + filas_totales.text)

    filas_scrapeadas = 0
    fila_actual = filas_scrapeadas

    # Obtener la altura de una fila de la tabla
    altura_fila = driver.execute_script("return arguments[0].clientHeight;", filas[0]) * 2

    while filas_scrapeadas < int(filas_totales.text):
        print("FILA " + str(filas_scrapeadas))
        driver.execute_script("window.scrollBy(0, arguments[0]);", altura_fila)
        WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.ID, 'mainThrobber')))
        time.sleep(1)  # Esperar un segundo para que la tabla se actualice después del desplazamiento

        fila_actual += 1

        xpath = f"//*[@id='tblNotices']/div[2]/div[{fila_actual}]"
        fila_visible = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))

        filas_scrapeadas += 1

        columnas = fila_visible.find_elements(By.XPATH, "div[@role='cell']")
        referencia = columnas[6].text
        if ids_referencia is not None and referencia in ids_referencia:
            print("Ya existe")
            continue

        titulo = columnas[1].text
        fecha_limite = columnas[2].text
        publicado = columnas[3].text
        organismo_onu = columnas[4].text
        tipo_anuncio = columnas[5].text
        pais = columnas[7].text

        print("pais: " + pais)
        if pais not in PAISES_VALIDOS:
            print("Pais invalido")
            continue

        print("titulo: " + titulo)
        print("fecha: " + fecha_limite)
        print("publicado: " + publicado)
        print("org_onu: " + organismo_onu)
        print("anuncio: " + tipo_anuncio)
        print("ref: " + referencia)

        agregar_datos_NUG(titulo, fecha_limite, publicado, organismo_onu, tipo_anuncio, referencia, pais)


if __name__ == '__main__':
    main()
