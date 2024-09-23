from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.chrome.service import Service
import time

service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# PATH = "C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe"
# driver = webdriver.Chrome(PATH)

driver.get("https://cornerprobet.com/")

time.sleep(5)
# elements = driver.find_elements(By.CSS_SELECTOR, "div.game_info > div.cpa-flex-row.cpa-align-center.cpa-flex-row--collapse.cpa-flex-row--reverse > a")
#
# #EQUIPO CASA ->  div.game_info > div:nth-child(3) > a
# #EQUIPO VISITANTE ->  div.game_info > div.cpa-flex-row.cpa-align-center.cpa-flex-row--collapse.cpa-flex-row--reverse > a
#
# for element in elements:
#     print(element.text)
#
# print(len(elements))

# Obtener los elementos con los selectores CSS especificados
copa = driver.find_elements(By.CSS_SELECTOR,"div.league_header > div.logo_name > p")
local = driver.find_elements(By.CSS_SELECTOR,"div.game_info > div:nth-child(3) > a")
tiempo = driver.find_elements(By.CSS_SELECTOR,"div.game_info > div.cpa-flex-col > span")
visitante = driver.find_elements(By.CSS_SELECTOR,"div.game_info > div.cpa-flex-row.cpa-align-center.cpa-flex-row--collapse.cpa-flex-row--reverse > a")
url_elements = driver.find_elements(By.CSS_SELECTOR,"div.game_info > div.links > a.link_analysis")
# # Crear una lista de tuplas con el texto de los elementos seleccionados

lista = []
for url in url_elements:
    lista.append(url.get_attribute("href"))
    
time.sleep(5)

result = [('Huracán', '2023-03-10 00:00', 'Sporting Cristal', 'https://cornerprobet.com/analysis/Huracan-Sporting-Cristal/qgo8j'), ('Deportes Tolima', '2023-03-10 00:00', 'Junior', 'https://cornerprobet.com/analysis/Deportes-Tolima-Junior/qf77r'), ('Emelec', '2023-03-10 00:00', 'Deportivo Cuenca', 'https://cornerprobet.com/analysis/Emelec-Deportivo-Cuenca/qf781'), ('SWA Sharks', '2023-03-10 00:00', 'Teachers', 'https://cornerprobet.com/analysis/SWA-Sharks-Teachers/qgsm5'), ('Fanalamanga', '2023-03-10 00:00', 'COSFA', 'https://cornerprobet.com/analysis/Fanalamanga-COSFA/qe03a'), ('Santos', '2023-03-10 00:30', 'Iguatu', 'https://cornerprobet.com/analysis/Santos-Iguatu/qgecm'), ('Diriangén', '2023-03-10 01:00', 'Matagalpa', 'https://cornerprobet.com/analysis/Diriangen-Matagalpa/qgrm0'), ('Real Estelí', '2023-03-10 01:00', 'Jalapa', 'https://cornerprobet.com/analysis/Real-Esteli-Jalapa/qgrls'), ('Alianza Petrolera', '2023-03-10 01:00', 'Deportivo Pasto', 'https://cornerprobet.com/analysis/Alianza-Petrolera-Deportivo-Pasto/qfomk')]
for i in range(len(local)):
    result.append((local[i].text, tiempo[i].text, visitante[i].text, lista[i]))
# print(len(copa))
print(result)

time.sleep(5)

# Guardar la lista de tuplas en un archivo CSV
with open("Encuentros(11-03-2023).csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Local", "Tiempo", "Visitante", "Analisis"])
    writer.writerows(result)


# Imprimir la lista de tuplas

# time.sleep(5)

driver.quit()
