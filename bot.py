import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

##### Le realiza una consulta a copilot (la ia de microsoft) y devuelve la respuesta en un archivo txt ######

driver_path = r"C:\Users\branc\Escritorio\proyect-luca\chromedriver-win64\chromedriver.exe"

option = webdriver.ChromeOptions()

option.add_argument('--window-size=1920x1080')
option.add_argument("--start-maximized") 
option.add_argument('--charset=utf-8')
option.add_argument('--disable-gpu')
option.add_argument("--disable-notifications")
option.add_argument('--lang=es')  # Configura el idioma si es necesario
option.add_argument('--encoding=utf-8')  # Configura la codificación

# option.add_argument("--incognito") OPTIONAL
#option.add_argument("--headless") 
for i in range(10):
    def esperar_xpath(xpath): #espera a que aparezca el elemento y espera 1 segundo

        global driver

        try:
            element = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, xpath)) #espera a que cargue el xpath dado
                )
            
        finally:
            time.sleep(1)

    def respuesta_copilot():

        global driver

        ### Busca el texto dentro de todos los shadow-root ###
        contenedor00 = driver.find_element(By.CLASS_NAME, "cib-serp-main")

        shadow01 = contenedor00.shadow_root 

        shadow01.find_element(By.CSS_SELECTOR, "#cib-action-bar-main ")

        shadow02 = shadow01.find_element(By.CSS_SELECTOR, "#cib-conversation-main").shadow_root

        shadow03 = shadow02.find_element(By.CSS_SELECTOR, "#cib-chat-main > cib-chat-turn").shadow_root 
        
        shadow04= shadow03.find_element(By.CSS_SELECTOR, "cib-message-group.response-message-group").shadow_root 
        
        shadow05 = shadow04.find_element(By.CSS_SELECTOR, "cib-message:nth-child(2)").shadow_root
        ######

        print("Esperando a que termine...")

        try:
            element = WebDriverWait(shadow04, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "cib-message:nth-child(3)")) #espera a que termine el texto
                )
                
        finally:
            time.sleep(1)


        texto = shadow05.find_element(By.CSS_SELECTOR, "cib-shared").text #agarra el texto y lo copia
        
        with open('respuesta.txt', 'w', encoding='utf-8') as archivo: #crea un archivo .txt y guarda el texto en cuestion
            archivo.write(texto)

        return archivo 

    def consulta_copilot(consulta):

        global driver

        driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)

        url = 'https://copilot.microsoft.com/' 

        driver.get(url)

        print("Esperando a que cargue la pagina...")

        esperar_xpath("/html/body/div[1]")#espera a que cargue la pagina.

        ### Busca el input dentro de todos los shadow-roots ###
        contenedor = driver.find_element(By.CLASS_NAME, "cib-serp-main")

        shadow1 = contenedor.shadow_root 

        shadow1.find_element(By.CSS_SELECTOR, "#cib-action-bar-main ")

        shadow2 = shadow1.find_element(By.CSS_SELECTOR, "#cib-action-bar-main").shadow_root

        shadow3 = shadow2.find_element(By.CSS_SELECTOR, "div > div.main-container > div > div.input-row > cib-text-input").shadow_root 

        boton = shadow2.find_element(By.CSS_SELECTOR, "div > div.main-container > div > div.bottom-controls > div.bottom-right-controls > div.control.submit > button")

        entrada = shadow3.find_element(By.CSS_SELECTOR, "#searchboxform > label")
        ######
        entrada.send_keys(consulta) #le realiza la pregunta

        time.sleep(1)

        boton.click()

        print("Realizandole la consulta...")

        time.sleep(15)

        #comentarios

        respuesta_copilot() #ejecuta la funcion para copiar la respuesta

        print("FIN")


    pregunta = "Hola, contame un dato curioso"

    consulta_copilot(pregunta)