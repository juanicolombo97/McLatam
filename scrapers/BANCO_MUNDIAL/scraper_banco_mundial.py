# -------------------------------------- LIBRERIAS --------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

from scrapers.BANCO_MUNDIAL.firebase import agregar_datos

LISTA_PAISES_INVALIDOS = [
    'Brazil'
]

LISTA_IDIOMAS_VALIDOS = [
    'Spanish; Castilian', 'Spanish', 'Castillan'
]


def main():
    url_pagina = 'https://projects.worldbank.org/en/projects-operations/procurement?lang=en&qterm=&showrecent=true&srce=notices'

    # Opciones Chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("start-maximized")
    options.add_argument("--window-size=1920x1080")
    options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'plugins.always_open_pdf_externally': True  # Abrir PDF en lugar de descargar
    })

    # Obtenemos el driver
    driver = webdriver.Chrome(executable_path='scrapers/chromedriver', options=options)

    # Abrimos la pagina
    driver.get(url_pagina)

    # Llamamos a la funcion que agrega los filtros
    aplicar_filtros(driver)

    # Llamamos funcion obtiene los datos
    obtener_datos_tabla(driver)


# Funcion que aplica filtros a la tabla
def aplicar_filtros(driver):
    # Esperamos que cargue el filtro
    region = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Region']/..")))
    region.click()
    time.sleep(1)

    # Selecciono el filtro
    filtro_region = driver.find_element(By.XPATH, "//*[@id='sidebar-wrapper']/ul[2]/ul/li[4]/div/input")
    filtro_region.click()
    time.sleep(1)

    # Esperamos que cargue el segundo filtro y nos movemos por si no esta a la vista
    tipo_noticia = driver.find_element(By.XPATH, "//a[text()='Notice Type']")
    actions = ActionChains(driver)
    actions.move_to_element(tipo_noticia).perform()
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Notice Type']/..")))
    tipo_noticia.click()
    time.sleep(1)

    # Selecciono el filtro
    filtro_tipo_noticia = driver.find_element(By.XPATH, "//span[contains(text(),'Request for')]/..")
    actions = ActionChains(driver)
    actions.move_to_element(filtro_tipo_noticia).perform()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='sidebar-wrapper']/ul[4]/ul/li[2]/div/input")))
    filtro_tipo_noticia = driver.find_element(By.XPATH, "//*[@id='sidebar-wrapper']/ul[4]/ul/li[2]/div/input")
    filtro_tipo_noticia.click()
    time.sleep(2)


# Funcion que obtiene los datos de la tabla
def obtener_datos_tabla(driver):
    print('Iniciando scrapeo')

    fila_actual = 0
    # Obtengo la cantidad de filas totales a scrapear
    filas_totales = driver.find_element(By.XPATH, "//p[@class='blurb-text ng-star-inserted']").text
    filas_totales = filas_totales.split("of")[1].split()[0]
    cadena_sin_coma = filas_totales.replace(",", "")
    # Convertir la cadena sin coma en un número entero
    filas_totales = int(cadena_sin_coma)
    numero_pagina = 0

    while fila_actual < int(filas_totales):
        # Esperamos que cargue la tabla
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Description')]/../../../tbody")))

        # Obtenemos la tabla de la pagina
        tabla = driver.find_element(By.XPATH, "//th[contains(text(), 'Description')]/../../../tbody")

        # Obtenemos las filas de la tabla
        filas = tabla.find_elements(By.TAG_NAME, "tr")

        print("Numero de pagina: " + str(numero_pagina))

        # Recorremos las filas
        for numero_fila in range(0, int(len(filas))):
            print('FILA ACTUAL: ' + str(numero_fila))
            fila_actual += 1
            # Iniciamos datos de la fila
            descripcion = ''
            pais = ''
            idioma = ''
            fecha_publicacion = ''
            titulo = ''
            tipo_noticia = ''

            # Obtenemos los datos de la fila
            datos_fila = filas[numero_fila].find_elements(By.TAG_NAME, "td")

            # Obtenemos el pais de la fila
            pais = datos_fila[1].text

            # Nos fijamos si el pais es valido
            if not elemento_valido(pais, LISTA_PAISES_INVALIDOS):
                print('Pais invalido')
                continue

            # Obtenemos el idioma
            idioma = datos_fila[4].text

            # Nos fijamos si el idioma es valido
            if elemento_valido(idioma, LISTA_IDIOMAS_VALIDOS):
                print('Idioma invalido')
                continue

            # Obtenemos la descripcion
            descripcion = datos_fila[0].text

            # Obtenemos el titulo
            titulo = datos_fila[2].text

            # Obtenemos tipo noticia
            tipo_noticia = datos_fila[3].text

            # Obtenemos la fecha de publicacion
            fecha = datos_fila[5].text

            print('desc: ' + descripcion)
            print('pais: ' + pais)
            print('titulo: ' + titulo)
            print('tipo noticia: ' + tipo_noticia)
            print('idioma: ' + idioma)
            print('Fecha: ' + fecha)
            expediente_id = str(numero_pagina) + str(numero_fila)
            print('Expediente id: ' + expediente_id)
            # agregar_datos(expediente_id, descripcion, pais, titulo, tipo_noticia, idioma, fecha)

        siguiente = driver.find_elements(By.XPATH, "//ul[@class='pagination ng-star-inserted']/li")
        print("Cantidad siguiente: ", len(siguiente))

        actions = ActionChains(driver)
        actions.move_to_element(siguiente[-2]).perform()
        actions.click(siguiente[-2]).perform()
        print("click siguiente")

        numero_pagina += 1
        time.sleep(3)


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
