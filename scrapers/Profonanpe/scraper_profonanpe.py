# ------------------------------------- LIBRERIAS ---------------------------------------------------------------------
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def main():
    url_pagina = 'https://convocatoriasprofonanpe.vform.pe/'

    # Opciones Chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("start-maximized")
    options.add_argument("window-size=1200x600")
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
        EC.presence_of_element_located((By.ID, "home-sign-in")))

    iniciar_sesion = driver.find_element(By.ID, "home-sign-in")
    iniciar_sesion.click()

    # Esperamos que cargue el inpout email
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "applicant_email")))

    input_email = driver.find_element(By.ID, "applicant_email")
    input_email.clear()
    input_email.send_keys('comercial@mclatam.com')

    input_password = driver.find_element(By.ID, "applicant_password")
    input_password.clear()
    input_password.send_keys("Adquisiciones2023")

    boton_ingresar = driver.find_element(By.XPATH, "//button[@class='btn btn-block btn-institution']")
    boton_ingresar.click()
    time.sleep(.5)

    # Buscamos el boton para filtrar por procesos abiertos
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//li[@class='open-templates-postulations hidden-xs nav-wrapper']")))
    procesos_abiertos = driver.find_element(By.XPATH,
                                            "//li[@class='open-templates-postulations hidden-xs nav-wrapper']")
    procesos_abiertos.click()


if __name__ == '__main__':
    main()
