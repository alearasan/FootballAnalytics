from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.chrome.service import Service
import time

service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://cornerprobet.com/")
# Hacer clic en el botón
boton = driver.find_element(By.CSS_SELECTOR, "#app > div.page > section.filtered > div.cpa_section.filtered_games.all_games > div.header > div.cpa-flex-row.showFilters > button:nth-child(3)")
boton.click()

# Esperar a que los elementos estén presentes y visibles
wait = WebDriverWait(driver, 100)

elementos_locales = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#day10 > div:nth-child(1) > div.game_info > div:nth-child(3) > a")))
elementos_tiempos = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#day10 > div:nth-child(1) > div.game_info > div.cpa-flex-col > span")))
elementos_visitantes = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#day10 > div:nth-child(1) > div.game_info > div.cpa-flex-row.cpa-align-center.cpa-flex-row--collapse.cpa-flex-row--reverse > a")))
url_elements = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#day10 > div:nth-child(1) > div.game_info > div.links > a.link_analysis")))

# Crear una lista de tuplas con el texto de los elementos seleccionados
result = []
for i in range(len(elementos_locales)):
    result.append((elementos_locales[i].text, elementos_tiempos[i].text, elementos_visitantes[i].text, url_elements[i].get_attribute("href")))
    
print(result)
