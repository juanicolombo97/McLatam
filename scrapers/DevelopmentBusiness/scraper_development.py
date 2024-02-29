# -------------------------------------- LIBRERIAS --------------------------------------------------------------------
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from twocaptcha import TwoCaptcha
# Para que corra en AWS
# import sys
# sys.path.append('/home/ubuntu/McLatam')
from scrapers.firebase import agregar_datos_development, obtener_expediente

LISTA_PAISES_INVALIDOS = [
    'Afghanistan', 'Benin', 'Burundi', 'Chad', 'China', 'Côte d’Ivoire', 'Djibouti','Ethiopia', 'Georgia', 'India', 'Iraq', 'Malawi','Moldova', 'Nepal', 'Niger', 'Pakistan', 'Philippines', 'Senegal', 'Somalia', 'South Sudan', 'Tajikistan', 'Tunisia', 'Turkmenistan', 'Uganda', 'Ukraine', 'Vietnam', 'Zambia'
]

fecha_actual = datetime.now().date()

# Funcion que se encarga de correr el scraper
def main():
    url_pagina = 'https://devbusiness.un.org/content/site-search'

    # Opciones Chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("start-maximized")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--start-maximized")

    # Obtenemos el driver
    driver = webdriver.Chrome(options=options)

    # Abrimos la pagina
    driver.get(url_pagina)

    # Llamamos funcion que inicia el scrapeo
    iniciar_scrapeo(driver)


# Funcion que se encarga de la logica de scrapeo
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
    time.sleep(5)

    # Logueamos
    while True:
        resultado = login(driver)
        if resultado == True:
            break

    # Volvemos a la paigna inicial
    driver.get('https://devbusiness.un.org/content/site-search')
    print('Volvemos a la pagina inicial')

    # Esperamos que cargue la seccion de filtro
    WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((
            By.XPATH, "//aside[@class='main-sidebar col-md-3 search-results__filters filters--operational-summary']"
        ))
    )
    time.sleep(1)

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((
            By.XPATH, "//select[@data-drupal-facet-id='language']"
        ))
    )
    print("presence")
    block_language = driver.find_element(By.XPATH, "//div[@id='block-language']")
    driver.execute_script("arguments[0].scrollIntoView(true);", block_language)
    print('Scroll')
    time.sleep(2)

    selector = driver.find_element(By.XPATH, "//input[@placeholder='Select languages']/../..")
    selector.click()
    print("Click")
    time.sleep(1)

    spanish = driver.find_element(By.XPATH, "//li[contains(text(), 'Spanish')]")
    spanish.click()
    print("Click spanish")
    time.sleep(1)

    # Esperamos que cargue la seccion donde estan los datos
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((
            By.ID, "block-un-devbusiness-content"
        ))
    )
    print("Datos cargados")
    time.sleep(10)

    # Obtenemos div donde estan los datos
    div_datos = driver.find_element(By.XPATH, "//div[@class='view-content']")

    # Obtenemos los divs de dichos datos
    divs_datos = div_datos.find_elements(By.XPATH, "./div")
    print('Cantidad de datos: ', len(divs_datos))

    cantidad_datos = len(divs_datos)
    contador = 0
    pagina = 0

    # While mientras dejas scrolear y aparecen nuevos expedietes
    while True:

        try:
            # Obtenemos datos de los expedientes
            obtener_datos_expediente(driver, contador)

            # Aumentamos contador
            contador += 1
            print('Contador: ', contador)

            if contador >= cantidad_datos:
                pagina += 1
                xpath = f'//span[contains(text(), "Next page")]/..'
                print(xpath)
                print("Por clickear pagina siguiente")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((
                        By.XPATH, xpath
                    ))
                )
                actions = ActionChains(driver)
                next_page = driver.find_element(By.XPATH, xpath)
                actions.move_to_element(next_page).perform()
                time.sleep(1)
                next_page.click()
                print("Click next page")
                time.sleep(5)
                contador = 0

        # Si hubo error, scrolleamos para abajo asi aparecen mas expedientes
        except Exception as e:
            print('Error: ', e)
            # Scrolleamos para abajo hasta llegar al fondo y scrolleamos mas asi cargan nuevos expedinetes
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)


# Funcion que se encarga de obtener los datos de un expediente
def obtener_datos_expediente(driver, contador):
    pais = ''
    empresa = ''
    deadline = ''
    titulo = ''
    proyecto = ''
    url = ''

    # Obtenemos div donde estan los datos
    div_datos = driver.find_element(By.XPATH, "//div[@class='view-content']")

    # Obtenemos los divs del expediente y nos quedamos con el segundo
    expediente = div_datos.find_elements(By.XPATH, "./div")
    # //div[@class='view-content']/div
    print('Cantidad de expedientes: ', len(expediente))

    divs_expediente = expediente[contador].find_elements(By.XPATH, "./div/div/div")
    # //div[@class='view-content']/div/div/div/div
    print('Cantidad de divs del expediente: ', len(divs_expediente))
    div_expediente = divs_expediente[1]

    # Ahora obtenemos los 3 divs donde se encuentran los datos
    divs_datos_expediente = div_expediente.find_elements(By.XPATH, "./div")
    # //div[@class='view-content']/div/div/div/div/div
    print('Obtenemos los datos del expediente')

    # El primer div es el titulo, y obtenemos los spans dentro de el
    div_titulo = divs_datos_expediente[0]

    # El separador | divide el pais y la empresa, obtenemos cada dato
    try:
        pais = div_titulo.find_element(By.XPATH, "./div[@class='card__countries']/span").text
        empresa = div_titulo.find_element(By.XPATH, "./span[@class='card__institution']").text
        print('Pais: ', pais)
        if(pais in LISTA_PAISES_INVALIDOS):
            print('Pais invalido')
            return
        print('Empresa: ', empresa)
    except:
        print('No se pudo obtener pais y empresa')

    # Obtenemos el segundo div que es donde estan los demas divs, y obtenemos los 4 restantes
    div_descripcion = divs_datos_expediente[1].find_elements(By.XPATH, "./div")

    # Del primer div obtenemos los dos divs
    divs_primero = div_descripcion[0].find_elements(By.XPATH, "./div")
    print('Cantidad de divs del primero: ', len(divs_primero))

    # Obtenemos el url y el titulo
    try:
        url = divs_primero[0].find_element(By.TAG_NAME, "a").get_attribute('href')
        print('Url: ', url)
    except:
        url = ""
        print("No tiene url")
    titulo = divs_primero[0].find_element(By.TAG_NAME, "h3").text
    print('Titulo: ', titulo)

    try:
        # Del segundo div obtenemos el proyecto
        proyecto = divs_primero[1].text
        # Hacemos split y sacamos el proyecto y salto linea
        proyecto = proyecto.split('\n')[1].strip()
        print('Proyecto: ', proyecto)
    except:
        proyecto = ''
        print("No tiene proyecto")

    # Obtenemos del segundo div de descripcion para obtener la fecha
    divs_segundo = div_descripcion[1].text.split('\n')[1].strip()
    print('Fecha: ', divs_segundo)

    # Obtenemos el status
    status = div_descripcion[2].text.split('\n')[1].strip()
    print('Status: ', status)

    # obtenemos el expediente id
    expediente_id = div_descripcion[3].text.split('\n')[1].strip()
    print('Expediente id: ', expediente_id)

    if obtener_expediente(expediente_id):
        print("Ya existe")
        return

    # Obtenemos el tercero que es el del deadline
    try:
        div_deadline = divs_datos_expediente[2]
        deadline = div_deadline.text
        deadline = deadline.split('DEADLINE')[1].strip()
        deadline_date = datetime.strptime(deadline, "%d %b %Y").date()
        if deadline_date < fecha_actual:
            print("La fecha limite ya paso.")
            return
    except:
        print("No se pudo obtener el deadline")
    print('Deadline: ', deadline)
    agregar_datos_development(expediente_id, titulo, divs_segundo, pais, empresa, url, proyecto, status, deadline)


# Funcion que se encarga de loguearse a la pagina
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
        # ingresamos el captcha
        solver = TwoCaptcha('725b33267e77fe2aa1ec45d2f6be8210')
        result = solver.recaptcha(sitekey='6LdrPCcfAAAAAItDUROndz6RcAi0ngbTjYj4BKHB',
                                  url='https://devbusiness.un.org/user/login')
        print("Result from captcha: ")
        print(result)

        captcha = driver.find_element(By.XPATH, "//*[@id='g-recaptcha-response']")
        driver.execute_script('arguments[0].style.display = "block";', captcha)
        valor_code = result['code']
        captcha.send_keys(valor_code)
        time.sleep(1)

        # Obtenemos el botton de submit
        boton_submit = driver.find_element(By.XPATH, "//input[@id='edit-submit']")
        boton_submit.click()
        print('Presionamos boton de log in')

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
                        boton_cerrar_sesion = driver.find_element(By.XPATH, "//input[@id='edit-submit']")
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
