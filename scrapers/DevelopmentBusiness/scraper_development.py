
#-------------------------------------- LIBRERIAS ----------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from datetime import date, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from twocaptcha import TwoCaptcha
import time
import os
import sys
import requests
from io import BytesIO
from PIL import Image
import pytesseract
import re
import cv2
from PIL import Image
import pytesseract
import re
import os
import cv2
import numpy as np


def main():

    url_pagina = 'https://devbusiness.un.org/content/site-search'

    # Opciones Chromedriver
    options = webdriver.ChromeOptions()
   # options.add_argument('headless')
    options.add_argument("start-maximized")


    # Obtenemos el driver
    driver = webdriver.Chrome(executable_path='scrapers/chromedriver',  options=options)

    # Abrimos la pagina
    driver.get(url_pagina)
    
    # Llamamos funcion que inicia el scrapeo
    iniciar_scrapeo(driver)

def iniciar_scrapeo(driver):
    print('Iniciando scrapeo')

    # Esperamos que cargue el boton de loguin y lo presionamos
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((
            By.XPATH, "//a[@href='/user/login']"
        ))
    )
    driver.find_element(By.XPATH, "//a[@href='/user/login']").click()
    print('Presionamos boton de loguin')

    # Logueamos
    while True:
        resultado = login(driver)
        if resultado == True:
            break



    # Volvemos a la paigna inicial
    driver.get('https://devbusiness.un.org/content/site-search')
    print('Volvemos a la pagina inicial')

    # Esperamos que cargue la seccion donde estan los datos
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((
            By.XPATH, "//div[@class='row views-row ']"
        ))
    )
    
    # Obtenemos div donde estan los datos
    div_datos = driver.find_element(By.XPATH, "//div[@class='search-results apachesolr_search-results']")
    
    # While mientras dejas scrolear y aparecen nuevos expedietes
    while True:

        # Obtenemos los divs de dichos datos
        divs_datos = div_datos.find_elements(By.XPATH, "./div")
        print('Cantidad de datos: ', len(divs_datos))

        # Recorremos los divs de los datos
        for expediente in divs_datos:

            pais = ''
            empresa = ''


            # Obtenemos los divs del expediente y nos quedamos con el segundo
            divs_expediente = expediente.find_elements(By.XPATH, "./div")
            div_expediente = divs_expediente[1]
            
            # Ahora obtenemos los 3 divs donde se encuentran los datos
            divs_datos_expediente = div_expediente.find_elements(By.XPATH, "./div")

            # El primer div es el titulo, y obtenemos los spans dentro de el
            div_titulo = divs_datos_expediente[0].find_elements(By.TAG_NAME, "span")
            
            # El separador | divide el pais y la empresa, obtenemos cada dato
            pais_empresa = div_titulo[1].text.split('|')
            pais = pais_empresa[0].strip()
            empresa = pais_empresa[1].strip()
            print('Pais: ', pais)
            print('Empresa: ', empresa)

            
            
            break
        break

def login(driver):
    try:
        # Esperamos que cargue el inpout email
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((
                By.XPATH, "//input[@id='edit-name']"
            ))
        )
        print('Cargamos input email')

        # Ingresamos el email
        input_email = driver.find_element(By.XPATH, "//input[@id='edit-name']")
        input_email.clear()
        input_email.send_keys('comercial@mclatam.com')
        print('Ingresamos email')
        time.sleep(2)

        # Obtenemos la contraseña
        input_password = driver.find_element(By.XPATH, "//input[@id='edit-pass']")
        input_password.clear()
        input_password.send_keys('mcLatam323**')
        print('Ingresamos contraseña')
        time.sleep(3)

        # ESPRAMOS PARA INGRESAR CAPTCHA
        time.sleep(15)

        # Obtenemos el botton de submit
        boton_submit = driver.find_element(By.XPATH, "//button[@id='edit-submit']")
        boton_submit.click()
        print('Presionamos boton de submit')

        try:
            # Esperamos que cargue pagina de logeado
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH, "//a[contains(text(), 'View Profile')]"
                ))
            )
        except:
            cantidad_usuarios = 0
            while True:
                try:
                    # Nos fijamos si carga la parte de muchos usuarios
                    cantidad_usuarios = driver.find_elements(By.XPATH, "//div[@id='edit-session-reference']//div")
                    print('Cantidad de usuarios: ', len(cantidad_usuarios))
                    if len(cantidad_usuarios) == 0:
                        break
                    
                    # Loopeamos los usuarios
                    for usuario in cantidad_usuarios:

                        # Nos fijamos que no sea el usuario que ya esta logueado
                        if 'Your current session.' in usuario.text:
                            continue

                        # Presionamos el elemento
                        usuario.click()
                        print('Presionamos el usuario')
                        time.sleep(2)

                        # Presionamos el boton de cerrar la sesion
                        boton_cerrar_sesion = driver.find_element(By.XPATH, "//button[@id='edit-submit']")
                        boton_cerrar_sesion.click()
                        time.sleep(2)
                
                except:
                    pass
                        
        return True
    except Exception as e:
        print('Error al loguear: ', e)
        return False

if __name__ == '__main__':
    main() 
