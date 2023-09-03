# -------------------------------------- LIBRERIAS ---------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By


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
    contenido_vacio = driver.find_element(By.XPATH,
                                          "//p[contains(text(), 'No se encontraron registros para los filtros seleccionados')]")
    if contenido_vacio is not None:
        print("Vacio")


if __name__ == '__main__':
    main()
