from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Configuración del driver de Selenium
service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)

# Navegar a la página y esperar a que se cargue el contenido
driver.get("https://cornerprobet.com/analysis/Colon-Newells-Old-Boys/qdn2a")
wait = WebDriverWait(driver, 10)
partidos_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.mainContent.main")))

# Obtener todos los elementos secundarios que contienen información de partidos
partidos_local = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.homeAsHome.table--striped tbody tr")

# Iterar sobre todos los partidos y extraer la información
partidos_data = []
for partido in partidos_local:
    Local = partido.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
    Fecha = partido.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
    Visitante = partido.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
    Resultado = partido.find_element(By.CSS_SELECTOR, "td.result").text
    Corners = partido.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
    partidos_data.append((Local, Fecha, Visitante, Resultado, Corners))

partidos_visitante = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.awayAsAway.table--striped tbody tr")
for partido in partidos_visitante:
    Local = partido.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
    Fecha = partido.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
    Visitante = partido.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
    Resultado = partido.find_element(By.CSS_SELECTOR, "td.result").text
    Corners = partido.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
    partidos_data.append((Local, Fecha, Visitante, Resultado, Corners))

# Escribir los datos en un archivo CSV
with open('partidos_data.csv', 'w', newline='', encoding = "utf-8") as file:
    writer = csv.writer(file,delimiter = ";")
    writer.writerow(["Local", "Fecha", "Visitante", "Resultado", "Corners"])
    writer.writerows(partidos_data)

# Cerrar el navegador
driver.quit()
