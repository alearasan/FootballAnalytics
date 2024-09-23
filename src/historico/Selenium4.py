from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://cornerprobet.com/")

boton = driver.find_element(By.CSS_SELECTOR, "#app > div.page > section.filtered > div.cpa_section.filtered_games.all_games > div.header > div.cpa-flex-row.showFilters > button:nth-child(3)")
boton.click()

# Esperar a que la página se cargue completamente
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.game_info")))

# Obtener los elementos con los selectores CSS especificados
elementos = driver.find_elements(By.CSS_SELECTOR, "div.game_info")
#day13#gqfels > div.game_info
# Recorrer los elementos y agregar solo aquellos que estén visibles al archivo CSV
with open("Encuentros(11-03-2023).csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
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

driver.quit()