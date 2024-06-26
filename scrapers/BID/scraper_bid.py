# -------------------------------------- LIBRERIAS --------------------------------------------------------------------
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
# Para que corra en AWS
# import sys
# sys.path.append('/home/ubuntu/McLatam')
from scrapers.firebase import agregar_datos_BID, obtener_expediente

LISTA_TITULOS_MALOS = [
    'LGTBI+'
]


def main():
    url_pagina = 'https://beo-procurement.iadb.org/home'

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
    print('Iniciando scrapeo BID')

    # Esperamos que cargue la tabla
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Title of Consultancy')]/../../../tbody")))

    WebDriverWait(driver, 60).until(EC.invisibility_of_element((By.XPATH, "//div[@class='loading-container']")))

    # Obtenemos la tabla de la pagina
    tabla = driver.find_element(By.XPATH, "//th[contains(text(), 'Title of Consultancy')]/../../../tbody")

    # Obtenemos las filas de la tabla
    filas = tabla.find_elements(By.TAG_NAME, "tr")

    # Obtenemos el numero de filas
    num_filas = len(filas) / 2
    print('Numero de filas: ' + str(num_filas))
    una_semana_antes = datetime.now() - timedelta(days=7)

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
        print("datos fila len:")
        print(len(datos_fila))

        # Obtenemos el id de la fila
        id_fila = datos_fila[1].text
        if obtener_expediente(id_fila):
            print("Ya existe")
            continue
        print('ID: ' + id_fila)

        # Obtenemos el titulo de la fila
        titulo = datos_fila[2].text
        print('Titulo: ' + titulo)

        # Nos fijamos si el titulo es malo o no
        if not titulo_valido(titulo):
            print('Titulo invalido')
            continue

        # Obtenemos la fecha
        fecha = datos_fila[3].text.replace('\n', ' ').split(" ")[0]
        fecha_limite = datetime.strptime(fecha, '%d-%B-%Y').strftime('%d-%m-%Y')
        print('Fecha Limite: ' + fecha_limite)

        # Obtenemos el url del id
        url_id = datos_fila[1].find_element(By.TAG_NAME, "a").get_attribute('href')
        print('URL ID: ' + url_id)

        # Presionamos el boton de la fila para abrir la informacion
        actions = ActionChains(driver)
        boton_expandir = datos_fila[0]
        actions.move_to_element(boton_expandir).perform()
        time.sleep(10)
        boton_expandir.click()
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
        fecha_pub = datetime.strptime(fecha_publicacion, "%d-%B-%Y").strftime("%d-%m-%Y")
        fecha_publicacion_dt = datetime.strptime(fecha_publicacion, "%d-%B-%Y")
        if fecha_publicacion_dt < una_semana_antes:
            print(f"Fecha publicación {fecha_publicacion_dt} vieja")
            continue
        print('Fecha publicacion: ', fecha_pub)

        # Obtenemos el pais que es el tercer item, apartir de los :
        pais = lista_datos_apertura[2].split(':')[1].strip()
        print('Pais: ', pais)

        # Obtenemos el link del a
        link_datos = datos_apertura.find_element(By.TAG_NAME, "a").get_attribute('href')
        print('Link a obtenido: ', link_datos)

        # Abrimos pagina del link en un nuevo tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link_datos)
        print('Pagina abierta')

        # Esperamos que cargue la pagina
        time.sleep(2)
        try:
            close_popup = driver.find_element(By.XPATH, "//*[@id='onetrust-close-btn-container']/button")
            close_popup.click()
        except:
            print("No hay cookies")
        try:
            driver.find_element(By.XPATH, "//strong[contains(text(), 'File or directory not found.')]")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue
        except:
            print("Pagina valida")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(),  'Project Detail')]")))
        print('Pagina cargada')

        # Obtenemos el aproval date
        fecha_aprobacion = driver.find_element(By.XPATH, "//p[contains(text(),  ' Date')]/../p[2]").text
        fecha_aprobacion_dt = datetime.strptime(fecha_aprobacion, '%B %d, %Y').strftime('%d-%m-%Y')
        print('Fecha aprobacion: ' + fecha_aprobacion)

        # Obtenemos el sector del proyecto
        sector_proyecto = driver.find_element(By.XPATH, "//p[contains(text(),  'Sector')]/../p[2]").text
        print('Sector proyecto: ' + sector_proyecto)

        # Obtenemos el tipo de proyecto
        tipo_proyecto = driver.find_element(By.XPATH, "//p[contains(text(),  'Project Type')]/../p[2]").text
        print('Tipo proyecto: ' + tipo_proyecto)

        # Obtenemos el estado del proyecto
        estado_proyecto = driver.find_element(By.XPATH, "//p[contains(text(),  'Project Status')]/../p[2]").text
        print('Estado proyecto: ' + estado_proyecto)

        # Obtenemos monto proyecto
        costo = driver.find_element(By.XPATH, "//p[contains(text(),  'Total Cost')]/../p[2]").text
        print('Monto: ' + costo)

        # Obtenemos el Amount
        monto = driver.find_element(By.XPATH, "//p[contains(text(),  'Amount')]/../p[2]").text
        print('Amount: ' + monto)

        agregar_datos_BID(id_fila, titulo, fecha_limite, fecha_aprobacion_dt, fecha_pub, url_id, costo, monto, sector_proyecto, pais, link_datos,
                          tipo_proyecto, estado_proyecto, sub_sector)

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
