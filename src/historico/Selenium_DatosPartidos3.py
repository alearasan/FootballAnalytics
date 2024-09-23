from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
driver = webdriver.Chrome(service=service)

with open('../data/Analisis(13-03-2023).csv') as f:
    reader = csv.reader(f)
    next(reader) # Skip header row
    for row in reader:
        url = row[0]
        driver.get(url)

        partidos_container = driver.find_element(By.CSS_SELECTOR, "div.mainContent.main")

        # Obtener todos los elementos secundarios que contienen información de partidos
        partidos_local = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.homeAsHome.table--striped tbody tr")

        # Iterar sobre todos los partidos y extraer la información
        for partido in partidos_local:
            Local = partido.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
            Fecha = partido.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
            Visitante = partido.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
            Resultado = partido.find_element(By.CSS_SELECTOR, "td.result").text
            Corners = partido.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text

            print((Local, Fecha, Visitante, Resultado, Corners))

        # Obtener todos los elementos secundarios que contienen información de partidos
        partidos_visitante = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.awayAsAway.table--striped tbody tr")

        # Iterar sobre todos los partidos y extraer la información
        for partido in partidos_visitante:
            Local = partido.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
            Fecha = partido.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
            Visitante = partido.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
            Resultado = partido.find_element(By.CSS_SELECTOR, "td.result").text
            Corners = partido.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
            # Escribir los datos en un archivo CSV o realizar cualquier otra tarea necesaria
            print((Local, Fecha, Visitante, Resultado, Corners))

driver.quit()
