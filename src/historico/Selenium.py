from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.chrome.service import Service
import time

service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://cornerprobet.com/")

# time.sleep(2)
#
# boton = driver.find_element(By.CSS_SELECTOR, "#app > div.page > section.filtered > div.cpa_section.filtered_games.all_games > div.header > div.cpa-flex-row.showFilters > button:nth-child(3)")
# boton.click()

time.sleep(5)

# Obtener los elementos con los selectores CSS especificados
local = driver.find_elements(By.CSS_SELECTOR," div.game_info > div:nth-child(3) > a") #gq628a > div.game_info > div:nth-child(3) > a
tiempo = driver.find_elements(By.CSS_SELECTOR," div.game_info > div.cpa-flex-col > span") #gq628a > div.game_info > div.cpa-flex-row.cpa-align-center.cpa-flex-row--collapse.cpa-flex-row--reverse > a
visitante = driver.find_elements(By.CSS_SELECTOR," div.game_info > div.cpa-flex-row.cpa-align-center.cpa-flex-row--collapse.cpa-flex-row--reverse > a")
url_elements = driver.find_elements(By.CSS_SELECTOR," div.game_info > div.links > a.link_analysis")#gq628a > div.game_info > div.links > a.link_analysis

time.sleep(2)

# Crear una lista de tuplas con el texto de los elementos seleccionados
lista = []
for url in url_elements:
    lista.append(url.get_attribute("href"))
    
result = []
for i in range(len(local)):
    result.append((local[i].text, tiempo[i].text, visitante[i].text, lista[i]))
    print(result)

time.sleep(2)

# Guardar la lista de tuplas en un archivo CSV
with open("Encuentros(11-03-2023).csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Local", "Tiempo", "Visitante", "Analisis"])
    writer.writerows(result)
#
time.sleep(2)

driver.quit()