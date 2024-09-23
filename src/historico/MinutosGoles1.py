#FUNCIONA 

import re
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool
import pandas as pd

fecha_global = "10-10-2023"

def scrape_data(url):
    service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Proyectos/Scraping/Corners/Controlador Chrome/chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
            driver.get(url)
            boton = driver.find_element(By.CSS_SELECTOR, 'div.mainContent.live.analysis_live > div.side > div > div:nth-child(1) > div.header.cpa-flex-col > div.events_toggle > button:nth-child(2)')
            boton.click()#qf253 > div.mainContent.live.analysis_live > div.side > div > div:nth-child(1) > div.header.cpa-flex-col > div.events_toggle > button.cpa_tab_btn.cpa_tab_btn--active
            elementos = driver.find_elements(By.CSS_SELECTOR, "div.mainContent.live.analysis_live")
            corners_wrapper = driver.find_element(By.CSS_SELECTOR, 'div.mainContent.live.analysis_live > div.side > div > div:nth-child(1) > div.content.events_wrapper > div:nth-child(2)')
            corners = corners_wrapper.find_elements(By.CSS_SELECTOR, 'div:nth-child(n)')
            home_elementos = []
            away_elementos = []
            data = []
            for elemento in elementos:
                if elemento.is_displayed():
                    fecha = elemento.find_element(By.CSS_SELECTOR, "div.middle > p.match_date").text.split(" ")[2]
                    local = elemento.find_element(By.CSS_SELECTOR, "div.home > p.homeName").text
                    visitante = elemento.find_element(By.CSS_SELECTOR, "div.away > p.awayName").text
                    
                    home_elementos = []
                    away_elementos = []
                    
                    for corner in corners:
                        corner_text = corner.text
                        corner_number = re.search(r'\d+', corner_text)  # Busca el primer dígito en el texto
                        if corner_number:
                            corner_number = corner_number.group()  # Obtén el dígito coincidente
                            if 'event-item-home' in corner.get_attribute('class'):
                                home_elementos.append(corner_number)
                            elif 'event-item-away' in corner.get_attribute('class'):
                                away_elementos.append(corner_number)                    
                    if len(home_elementos)!= 0 or len(away_elementos)!=0:
                        data.append({'Fecha': fecha, 'Local': local, 'Visitante': visitante, 'GolesLocal': home_elementos, 'GolesVisitante': away_elementos})
                        print((fecha, local, visitante))
                        print(home_elementos)
                        print(away_elementos)                        

    except Exception:
        print(f"Error en la url: {url}")
        if "Estamos a ter muitos pedidos ao mesmo tempo. Tente mais tarde. [TOO_MANY_REQUESTS]" in driver.page_source:
            print("[TOO_MANY_REQUESTS]")
        data = []
        
    driver.quit()
    return data

if __name__ == '__main__':
    start_time = time.time()
    
# Crear un conjunto para almacenar los valores únicos de 'Local' en resultados.csv
    local_set = set()
    
    # Leer resultados.csv y almacenar los valores de 'Local' en el conjunto
    with open(f'../data/TestLista({fecha_global}).csv', 'r', encoding='utf-8') as resultados_file:
        next(resultados_file)  # Saltar la primera línea (encabezado)
        for line in resultados_file:
            valores = line.strip().split(',')
            local_set.add(valores[2])  # Suponiendo que 'Local' es la tercera columna en resultados.csv
    
    # Crear un archivo para escribir los análisis filtrados
    with open('analisis_filtrados.csv', 'w', encoding='utf-8') as salida_file:
        salida_file.write("Analisis\n")  # Escribir el encabezado en el archivo de salida
        
        # Leer encuentros.csv y escribir los análisis correspondientes a los 'Local' en resultados.csv
        with open(f"../data/Encuentros({fecha_global}).csv", 'r', encoding='utf-8') as encuentros_file:
            next(encuentros_file)  # Saltar la primera línea (encabezado)
            for line in encuentros_file:
                valores = line.strip().split(';')
                if valores[0] in local_set:
                    salida_file.write(f"{valores[3]}\n")  # Suponiendo que 'Analisis' es la cuarta columna en encuentros.csv

    
    urls = []
    with open(f'../data/DatosPartidosMinutosGoles({fecha_global}).csv', mode='w', newline='', encoding="utf-8") as csv_file:
        fieldnames = ['Fecha', 'Local', 'Visitante', 'GolesLocal', 'GolesVisitante']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter = ";")
        writer.writeheader()
        
        with open('analisis_filtrados.csv') as f:
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