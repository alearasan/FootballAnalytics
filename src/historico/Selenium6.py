# FUNCIONA
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://cornerprobet.com/")

start_time = time.time()

# boton = driver.find_element(By.CSS_SELECTOR, "#days > option:nth-child(7)")
# boton.click()

# Esperar a que la página se cargue completamente
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#day28")))
# Obtener los elementos con los selectores CSS especificados
elementos = driver.find_elements(By.CSS_SELECTOR, "div.game_info")
#day13#gqfels > div.game_info
# Recorrer los elementos y agregar solo aquellos que estén visibles al archivo CSV
with open("../data/Encuentros(28-03-2023).csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter = ";")
    writer.writerow(["Local", "Tiempo", "Visitante", "Analisis"])
    for elemento in elementos:
        # Verificar si el elemento está visible
        if elemento.is_displayed():
            local = elemento.find_element(By.CSS_SELECTOR, "div:nth-child(3) > a").text
            tiempo = elemento.find_element(By.CSS_SELECTOR, "div.cpa-flex-col > span").text
            visitante = elemento.find_element(By.CSS_SELECTOR, "div.cpa-flex-row.cpa-align-center.cpa-flex-row--collapse.cpa-flex-row--reverse > a").text
            url = elemento.find_element(By.CSS_SELECTOR, "div.links > a.link_analysis").get_attribute("href")
            writer.writerow([local, tiempo, visitante, url])
            # Imprimir la tupla en la consola (opcional)
            print((local, tiempo, visitante, url))

# Abrir el archivo original
with open("../data/Encuentros(28-03-2023).csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    header = next(reader)  # Leer la primera fila (encabezado)

    # Encontrar el índice de la columna "Analisis" en el encabezado
    analisis_index = header.index("Analisis")

    # Abrir el nuevo archivo CSV y escribir el encabezado
    with open("../data/Analisis(28-03-2023).csv", "w", newline="", encoding="utf-8") as fw:
        writer = csv.writer(fw)
        writer.writerow(["Analisis"])

        # Leer las filas del archivo original y escribir solo la columna "Analisis"
        for row in reader:
            analisis = row[analisis_index]
            writer.writerow([analisis])

driver.quit()

end_time = time.time()
total_time = end_time - start_time
print(f"Tiempo total: {total_time} segundos")