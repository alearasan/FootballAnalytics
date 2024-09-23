# FUNCIONA
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
# driver = webdriver.Chrome(service=service)
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

driver.get("https://cornerprobet.com/analysis/Comunicaciones-Santa-Lucia/qf7ch")

# Esperar a que la página se cargue completamente
wait = WebDriverWait(driver, 10)

start_time = time.time()

boton = driver.find_element(By.CSS_SELECTOR, 'div.mainContent.live.analysis_live > div.side > div > div:nth-child(1) > div.header.cpa-flex-col > div.events_toggle > button:nth-child(3)')
boton.click()

# Encontrar los elementos
elementos = driver.find_elements(By.CSS_SELECTOR, "div.mainContent.live.analysis_live")
corners_wrapper = driver.find_element(By.CSS_SELECTOR, 'div.mainContent.live.analysis_live > div.side > div > div:nth-child(1) > div.content.events_wrapper > div:nth-child(3)')
corners = corners_wrapper.find_elements(By.CSS_SELECTOR, 'div:nth-child(n)')

home_elementos = []
away_elementos = []

# Recorrer los elementos y agregar solo aquellos que estén visibles al archivo CSV
with open("../data/Prueba.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter = ";")
    writer.writerow(['Fecha','Local', 'Visitante', 'CornersLocal','CornersVisitante'])
    for elemento in elementos:
        if elemento.is_displayed():
            fecha = elemento.find_element(By.CSS_SELECTOR, "div.middle > p.match_date").text.split(" ")[2]
            local = elemento.find_element(By.CSS_SELECTOR, "div.home > p.homeName").text
            visitante = elemento.find_element(By.CSS_SELECTOR, "div.away > p.awayName").text
            for corner in corners:
                corner_text = corner.text
                corner_number = corner_text.split('\n')[0]
                if 'event-item-home' in corner.get_attribute('class'):
                    home_elementos.append(corner_number)
                elif 'event-item-away' in corner.get_attribute('class'):
                    away_elementos.append(corner_number)

            writer.writerow([fecha, local, visitante, home_elementos,away_elementos])
            print((fecha, local, visitante))
            print(home_elementos)
            print(away_elementos)
driver.quit()

end_time = time.time()
total_time = end_time - start_time
print(f"Tiempo total: {total_time} segundos")