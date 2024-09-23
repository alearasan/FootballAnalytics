# FUNCIONA
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Unicos datos que hay que cambiar
fecha_global = "18-01-2024"
#05-10-2023

ANALISIS = f'../data/Analisis({fecha_global}).csv'
DATOSPARTIDOS = f'../data/DatosPartidos({fecha_global}).csv'
#############################################

def scrape_data(url):
    # service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Proyectos/Scraping/Corners/Controlador Chrome/chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    driver = webdriver.Chrome( options=chrome_options)

    try:
        driver.get(url)

        # try:
        #     tiempo_maximo_espera = 2000  # en segundos
        #     boton = WebDriverWait(driver, tiempo_maximo_espera).until(
        #         EC.element_to_be_clickable((By.CSS_SELECTOR, '#app > div.page > section > div.navigation > button:nth-child(1)'))
        #     )
        #     boton.click()
        # except Exception as e:
        #     print(f"No se pudo hacer clic en el botón. Error: {e}")
        
        partidos_container = driver.find_element(By.CSS_SELECTOR, "div.mainContent.main")

        partidos_h2h = partidos_container.find_elements(By.CSS_SELECTOR, "div.h2h_games div:nth-child(1) table tbody tr")

        partidos_local = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.homeAsHome.table--striped tbody tr")
        partidos_visitante = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.awayAsAway.table--striped tbody tr")
        total_partidos = 0
        data = []
        for partido in partidos_local + partidos_visitante:
            fecha = partido.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
            local = partido.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
            resultado = partido.find_element(By.CSS_SELECTOR, "td.result").text
            visitante = partido.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
            corners = partido.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
            if local and fecha and visitante and resultado and corners != "0-0 (0-0)":
                data.append({'Local': local, 'Fecha': fecha, 'Visitante': visitante, 'Resultado': resultado, 'Corners': corners})
                total_partidos =+ 1
        
        for h2h in partidos_h2h:
            fecha = h2h.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
            local = h2h.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.replace(' 🟢', '')
            resultado = h2h.find_element(By.CSS_SELECTOR, "td.result").text
            visitante = h2h.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.replace(' 🟢', '')
            corners = h2h.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
            if local and fecha and visitante and resultado and corners != "0-0":
                data.append({'Local': local, 'Fecha': fecha, 'Visitante': visitante, 'Resultado': resultado, 'Corners': corners})
                data.append({'Local': local, 'Fecha': fecha, 'Visitante': visitante, 'Resultado': resultado, 'Corners': corners})
                total_partidos =+ 1
            
    except NoSuchElementException:
        print(f"No se encontró 'partidos_container' en la URL: {url}")
        data = []
        
    driver.quit()
    return data

if __name__ == '__main__':
    start_time = time.time()
    
    with open(DATOSPARTIDOS, mode='w', newline='', encoding="utf-8") as csv_file:
        fieldnames = ['Fecha','Local', 'Resultado',  'Visitante', 'Corners']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter = ";")
        writer.writeheader()
        
        with open(ANALISIS) as f:
            reader = csv.reader(f)
            next(reader)
            urls = [row[0] for row in reader]
            
            with Pool() as p:
                results = p.map(scrape_data, urls)
                
            for result in results:
                for row in result:
                    if row != "":
                        writer.writerow(row)
            
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tiempo total: {total_time} segundos")
    