from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

# Unicos datos que hay que cambiar
fecha_global = "23-06-2024"
DIA = "#day"+fecha_global[:2]
boton_option = "#days > option:nth-child(7)" # option:nth-child(6) para mañana max 10

ANALISIS = f'../data/Analisis({fecha_global}).csv'
ENCUENTROS = f'../data/Encuentros({fecha_global}).csv'

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

start_time = time.time()  # Añadir la declaración de start_time
partidos_totales = 0

def extract_data(elemento):
    if elemento.is_displayed():
        local = elemento.find_element(By.CSS_SELECTOR, "div:nth-child(3) > a").text
        tiempo = elemento.find_element(By.CSS_SELECTOR, "div.cpa-flex-col > span").text
        visitante = elemento.find_element(By.CSS_SELECTOR, "div.cpa-flex-row.cpa-align-center.cpa-flex-row--collapse.cpa-flex-row--reverse > a").text
        url = elemento.find_element(By.CSS_SELECTOR, "div.links > a.link_analysis").get_attribute("href")
        print(local, tiempo, visitante, url)
        return (local, tiempo, visitante, url)
    else :
        print(None)

with webdriver.Chrome(options=options) as driver:
    
    driver.get("https://cornerprobet.com/")

    boton = driver.find_element(By.CSS_SELECTOR, boton_option) 
    boton.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, DIA)))

    elementos = driver.find_elements(By.CSS_SELECTOR, "div.game_info")

    with open(ENCUENTROS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Local", "Tiempo", "Visitante", "Analisis"])

        with ThreadPoolExecutor() as executor:
            results = executor.map(extract_data, elementos)
            for result in results:
                if result is not None:
                    writer.writerow(result)
                    partidos_totales += 1
                
    with open(ANALISIS, "w", newline="", encoding="utf-8") as fw:
        writer_fw = csv.writer(fw)
        writer_fw.writerow(["Analisis"])

        with open(ENCUENTROS, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)  # Skip header
            for row in reader:
                writer_fw.writerow([row[-1]])

print(f"Tiempo total: {round(time.time() - start_time, 0)} segundos")
print(f"Partidos totales: {partidos_totales} partidos")
