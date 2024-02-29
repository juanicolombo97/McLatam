# -------------------------------------- LIBRERIAS ---------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import locale
# Para que corra en AWS
# import sys
# sys.path.append('/home/ubuntu/McLatam')
from scrapers.firebase import obtener_expediente, agregar_datos_CAF


def main():
    url_pagina = 'https://www.caf.com/es/actualidad/licitaciones/?bs=open&sd=&ed=&c=&reset=false'

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
    print('Iniciando scrapeo CAF')

    # Chequeamos que haya contenido
    try:
        driver.find_element(By.XPATH, "//p[contains(text(), 'No se encontraron registros para los filtros "
                                      "seleccionados')]")
    except:
        print("Obteniendo resultados")
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now().date()

        filas = driver.find_elements(By.XPATH, "//ul[@class='list-unstyled px-3 caf_list_agenda']/li")
        for fila in filas:
            div_resultados = fila.find_element(By.XPATH, "div")

            datos = div_resultados.find_elements(By.XPATH, "h5")
            titulo = datos[1].text  # tomamos al id como referencia
            if obtener_expediente(titulo):
                print("Ya existe")
                continue

            fecha_limite = div_resultados.find_element(By.XPATH, "p").text.split(":")[1]
            fecha_limite_date = datetime.strptime(fecha_limite, " %d de %B de %Y").date()
            print("Fecha limite: " + fecha_limite)

            if fecha_limite_date < fecha_actual:
                print("La fecha limite ya paso.")
                continue

            pais = datos[0].text
            url = datos[1].find_element(By.XPATH, "a").get_attribute('href')

            print("Pais: " + pais)
            print("Titulo: " + titulo)
            print("Url: " + url)

            agregar_datos_CAF(titulo, pais, url, fecha_limite)


if __name__ == '__main__':
    main()
