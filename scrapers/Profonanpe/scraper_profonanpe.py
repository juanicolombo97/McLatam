# ------------------------------------- LIBRERIAS ---------------------------------------------------------------------
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
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
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("window-size=1200x600")
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
    print('Iniciando scrapeo Profonanpe')

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "home-sign-in")))

    iniciar_sesion = driver.find_element(By.ID, "home-sign-in")
    iniciar_sesion.click()

    # Esperamos que cargue el input email
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "applicant_email")))

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "inputPassword")))

    input_email = driver.find_element(By.ID, "applicant_email")
    input_email.clear()
    input_email.send_keys('comercial@mclatam.com')

    input_password = driver.find_element(By.ID, "inputPassword")
    input_password.clear()
    input_password.send_keys("Adquisiciones2023")
    print("Inputs llenos")

    botones_inicio_sesion = driver.find_elements(By.XPATH, "//i[contains(text(),'login')]/..")
    print(len(botones_inicio_sesion))
    for boton in botones_inicio_sesion:
        try:
            actions = ActionChains(driver)
            actions.move_to_element(boton).perform()
            boton.click()
            print("Click")
        except:
            print("no me pude mover")
    print("Inicio de sesion")
    time.sleep(1)

    # Buscamos el boton para filtrar por procesos abiertos
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//li[@class='open-templates-postulations hidden-xs nav-wrapper']")))
    procesos_abiertos = driver.find_element(By.XPATH,
                                            "//li[@class='open-templates-postulations hidden-xs nav-wrapper']")
    procesos_abiertos.click()
    print("Click procesos abiertos")

    # Hacemos click sobre los filtros
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='form-group grouped_select optional filters_web_tags']")))
    boton_filtros = driver.find_element(By.XPATH, "//div[@class='form-group grouped_select optional filters_web_tags']")
    boton_filtros.click()
    print("Click filtros")

    # Elegimos el filtro
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='form-group grouped_select optional filters_web_tags']/div/div")))
    filtro = boton_filtros.find_element(By.XPATH, "div/div/div[@class='inner open']/ul/li[3]")
    filtro.click()
    print("Seleccionamos filtro")

    # Esperamos que cargue el contenido
    time.sleep(5)

    # Chequeamos que haya contenido
    try:
        driver.find_element(By.XPATH, "//i[@class='fa fa-exclamation-triangle']")
        print("Vacio")
    except NoSuchElementException:
        print("Hay contenido")

    time.sleep(4)


if __name__ == '__main__':
    main()
