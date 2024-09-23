# FUNCIONA
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


# Configurar el controlador de Selenium
service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Iniciar contador de tiempo
start_time = time.time()

# Abrir el archivo CSV para escribir los datos
with open('../data/Prueba5.csv', mode='w', newline='', encoding="utf-8") as csv_file:
    fieldnames = ['Fecha','Local', 'Resultado',  'Visitante', 'Corners']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter = ";")

    # Escribir los encabezados en el archivo CSV
    writer.writeheader()

    # with open('../data/Analisis(14-03-2023).csv') as f:
    with open('../data/Analisis(13-03-2023).csv') as f:

        reader = csv.reader(f)
        next(reader) # Skip header row
        for row in reader:
            url = row[0]
            driver.get(url)

            try:
                partidos_container = driver.find_element(By.CSS_SELECTOR, "div.mainContent.main")
            except NoSuchElementException:
                print(f"No se encontró 'partidos_container' en la URL: {url}")
                continue
            
            # Obtener todos los elementos secundarios que contienen información de partidos
            partidos_local = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.homeAsHome.table--striped tbody tr")
            partidos_visitante = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.awayAsAway.table--striped tbody tr")
            
            for partido in partidos_local + partidos_visitante:
                fecha = partido.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
                local = partido.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
                resultado = partido.find_element(By.CSS_SELECTOR, "td.result").text
                visitante = partido.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
                corners = partido.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
                writer.writerow({'Local': local, 'Fecha': fecha, 'Visitante': visitante, 'Resultado': resultado, 'Corners': corners})

                
# Finalizar contador de tiempo y calcular tiempo total
end_time = time.time()
total_time = end_time - start_time

# Imprimir tiempo total
print(f"Tiempo total: {total_time} segundos")

# Cerrar
driver.quit()
