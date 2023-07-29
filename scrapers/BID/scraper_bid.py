# -------------------------------------- LIBRERIAS ----------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


LISTA_TITULOS_MALOS = [
    'LGTBI+'
]


def main():
    url_pagina = 'https://beo-procurement.iadb.org/home'

    # Opciones Chromedriver
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument("start-maximized")
    options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'plugins.always_open_pdf_externally': True  # Abrir PDF en lugar de descargar
    })

    # Obtenemos el driver
    driver = webdriver.Chrome(executable_path='scrapers/chromedriver', chrome_options=options)

    # Abrimos la pagina
    driver.get(url_pagina)

    # Llamamos funcion que inicia el scrapeo
    obtener_datos_tabla(driver)


# Funcion que obtiene los datos de la tabla
def obtener_datos_tabla(driver):
    print('Iniciando scrapeo')

    # Esperamos que cargue la tabla
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Title of Consultancy')]/../../../tbody")))

    # Obtenemos la tabla de la pagina
    tabla = driver.find_element(By.XPATH, "//th[contains(text(), 'Title of Consultancy')]/../../../tbody")

    # Obtenemos las filas de la tabla
    filas = tabla.find_elements(By.TAG_NAME, "tr")

    # Obtenemos el numero de filas
    num_filas = len(filas) / 2
    print('Numero de filas: ' + str(num_filas))

    # Hacemos for por cada fila, saltando de 2 en 2
    for numero_fila in range(0, len(filas), 2):
        print('Fila actual: ' + str(numero_fila))

        # Esperamos que cargue la tabla
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Title of Consultancy')]/../../../tbody")))

        # Iniciamos datos de la fila
        id_fila = ''
        titulo = ''
        fecha = ''
        url_id = ''
        costo = 0
        monto = 0
        fecha_aprobacion = ''
        sector_proyecto = ''
        pais = ''
        link_datos = ''
        tipo_proyecto = ''
        estado_proyecto = ''
        sub_sector = ''
        fund = ''
        fecha_publicacion = ''

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

        # Presionamos el boton de la fila para abrir la informacion
        datos_fila[0].click()
        print('Boton fila presionado')
        time.sleep(3)

        # Obtenemos los datos de la fila
        datos_fila = filas[numero_fila + 1]

        # Obtenemos los datos de la primer columna
        datos_apertura = datos_fila.find_element(By.TAG_NAME, "div")

        # Hacemosun split de los datos_apertura con un salto de linea
        lista_datos_apertura = datos_apertura.text.split('\n')

        # Obtenemos el sub-sector que es el primer item, apartir de los :
        sub_sector = lista_datos_apertura[0].split(':')[1].strip()
        print('Sub-sector: ', sub_sector)

        # Obtenemos la fecha de publicacion que es el segundo item, apartir de los :
        fecha_publicacion = lista_datos_apertura[1].split(':')[1].strip()
        print('Fecha publicacion: ', fecha_publicacion)

        # Obtenemos el pais que es el tercer item, apartir de los :
        pais = lista_datos_apertura[2].split(':')[1].strip()
        print('Pais: ', pais)

        # Obtenemos el funding source
        fund = lista_datos_apertura[3].split(':')[1].strip()
        print('Funding source: ', fund)

        # Obtenemos el link del a
        link_datos = datos_apertura.find_element(By.TAG_NAME, "a").get_attribute('href')
        print('Link a obtenido: ', link_datos)

        # Abrimos pagina del link en un nuevo tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link_datos)
        print('Pagina abierta')

        # Esperamos que cargue la pagina
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),  'Project Detail')]")))
        print('Pagina cargada')

        # Obtenemos el aproval date
        fecha_aprobacion = driver.find_element(By.XPATH, "//div[contains(text(),  ' Approval date')]/../span").text
        print('Fecha aprobacion: ' + fecha_aprobacion)

        # Obtenemos el sector del proyecto
        sector_proyecto = driver.find_element(By.XPATH, "//div[contains(text(),  ' Project Sector')]/../span").text
        print('Sector proyecto: ' + sector_proyecto)

        # Obtenemos el tipo de proyecto
        tipo_proyecto = driver.find_element(By.XPATH, "//div[contains(text(),  ' Project Type')]/../span").text
        print('Tipo proyecto: ' + tipo_proyecto)

        # Obtenemos el estado del proyecto
        estado_proyecto = driver.find_element(By.XPATH, "//div[contains(text(),  ' Project Status')]/../span").text
        print('Estado proyecto: ' + estado_proyecto)

        # Obtenemos el operation number para presionarlo
        operation_number = driver.find_element(By.XPATH, "//div[contains(text(),  ' Operation Number')]/../span")

        # Nos movemos al elemento con actions y lo presionamos
        actions = ActionChains(driver)
        actions.move_to_element(operation_number).click().perform()
        time.sleep(3)

        # Esperamos que cargue el fund
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),  'Fund')]/../span")))

        # Obtenemos el fund
        fund = driver.find_element(By.XPATH, "//div[contains(text(),  'Fund')]/../span").text
        print('Fund: ' + fund)

        # Obtenemos monto proyecto
        costo = driver.find_element(By.XPATH, "//div[contains(text(),  'Total Cost')]/../span").text
        print('Monto: ' + costo)

        # Obtenemos el Amount
        monto = driver.find_element(By.XPATH, "//div[contains(text(),  'Amount')]/../span").text
        print('Amount: ' + monto)

        # Cerramos el tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print('Tab cerrado')


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
