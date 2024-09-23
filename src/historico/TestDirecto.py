'''
Created on 30 mar 2023

@author: aleja
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
# import re
#
# def extract_text_from_selector(selector):
#     regex = re.compile(r'^#o_\d{7}_1$')
#     if not regex.match(selector):
#         return
#
#     element = document.querySelector(selector)
#     if not element:
#         return
#
#     if element.innerText != '-':
#         numero = re.search(r'o_(\d+)_\d+', element.id).group(1)
#         resultado = f'#r_{numero}'
#         local = document.querySelector(f'{resultado} td.text-right.text-truncate > a').innerText
#         visitante = document.querySelector(f'{resultado} td:nth-child(5) > a').innerText
#         corners = element.innerText
#
#         print([local, visitante, corners])
#
# selectors = [el.id for el in document.querySelectorAll('*') if el.id and extract_text_from_selector(f'#{el.id}')]

if __name__ == '__main__':


# Esperar una pausa aleatoria de entre 1 y 5 segundos
    pausa = random.randint(1, 5)
    time.sleep(pausa)

# Configurar el controlador de Chrome
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    driver.get("https://betsapi.com/")
    pausa = random.randint(1, 5)
    time.sleep(pausa)
    
    
    boton0 = driver.find_element(By.CSS_SELECTOR, "body > div.fc-consent-root > div.fc-dialog-container > div.fc-dialog.fc-choice-dialog > div.fc-footer-buttons-container > div.fc-footer-buttons > button.fc-button.fc-cta-consent.fc-primary-button > p")
    boton0.click()
    boton1 = driver.find_element(By.CSS_SELECTOR, "body > div.page > div.page-main > div.my-3.my-md-5 > div > div.card > div > a:nth-child(3)")
    boton1.click()
    pausa = random.randint(1, 5)
    time.sleep(pausa)
    boton2 = driver.find_element(By.CSS_SELECTOR, "body > div.page > div.page-main > div.my-3.my-md-5 > div > div.row.justify-content-md-center > div > a:nth-child(4)")
    boton2.click()
    
    
# Esperar a que se cargue el elemento deseado
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id^='o_'][id$='_1']")))

# Obtener el texto del elemento deseado
    text = element.text

# Modificar el selector y obtener el texto del otro elemento deseado
    modified_selector = "#r_" + element.get_attribute("id")[2:9]
    modified_element = driver.find_element(By.CSS_SELECTOR, modified_selector + " td.text-right.text-truncate > a")
    modified_text = modified_element.text

# Imprimir los resultados por consola
    print(text)
    print(modified_text)

# Cerrar el navegador
    driver.quit()
