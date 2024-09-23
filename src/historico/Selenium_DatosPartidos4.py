# FUNCIONA
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Configurar el controlador de Selenium
service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Iniciar contador de tiempo
start_time = time.time()

# Abrir el archivo CSV para escribir los datos
with open('../data/Prueba4.csv', mode='w', newline='', encoding = "utf-8") as csv_file:
    fieldnames = ['Local', 'Fecha', 'Visitante', 'Resultado', 'Corners']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter = ";")

    # Escribir los encabezados en el archivo CSV
    writer.writeheader()

    with open('../data/asdf.csv') as f:
        reader = csv.reader(f)
        next(reader) # Skip header row
        for row in reader:
            url = row[0]
            driver.get(url)

            partidos_container = driver.find_element(By.CSS_SELECTOR, "div.mainContent.main")

            # Obtener todos los elementos secundarios que contienen información de partidos
            partidos_local = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.homeAsHome.table--striped tbody tr")

            # Iterar sobre cada partido y escribir los datos en el archivo CSV
            for partido in partidos_local:
                local = partido.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
                fecha = partido.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
                visitante = partido.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
                resultado = partido.find_element(By.CSS_SELECTOR, "td.result").text
                corners = partido.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
                writer.writerow({'Local': local, 'Fecha': fecha, 'Visitante': visitante, 'Resultado': resultado, 'Corners': corners})
            
            partidos_visitante = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.awayAsAway.table--striped tbody tr")

            for partido in partidos_visitante:
                local = partido.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
                fecha = partido.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
                visitante = partido.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
                resultado = partido.find_element(By.CSS_SELECTOR, "td.result").text
                corners = partido.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
                writer.writerow({'Local': local, 'Fecha': fecha, 'Visitante': visitante, 'Resultado': resultado, 'Corners': corners})
                
# Finalizar contador de tiempo y calcular tiempo total
end_time = time.time()
total_time = end_time - start_time

# Imprimir tiempo total
print(f"Tiempo total: {total_time} segundos")

# Cerrar el controlador de Selenium
driver.quit()
