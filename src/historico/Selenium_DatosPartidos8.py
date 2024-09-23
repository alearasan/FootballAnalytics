# FUNCIONA
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool

ANALISIS = '../data/Analisis(12-04-2023).csv'
DATOSPARTIDOS = '../data/DatosPartidos(11-04-2023)(v3).csv'

def scrape_data(url):
    try:
        service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(url)
        partidos_container = driver.find_element(By.CSS_SELECTOR, "div.mainContent.main")
        partidos_local = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.homeAsHome.table--striped tbody tr")
        partidos_visitante = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.awayAsAway.table--striped tbody tr")
        
        data = []
        for partido in partidos_local + partidos_visitante:
            fecha = partido.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
            local = partido.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
            resultado = partido.find_element(By.CSS_SELECTOR, "td.result").text
            visitante = partido.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text
            corners = partido.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text
            
            if local and fecha and visitante and resultado and corners:
                data.append({'Local': local, 'Fecha': fecha, 'Visitante': visitante, 'Resultado': resultado, 'Corners': corners})
            
        driver.quit()
        return data
    
    except NoSuchElementException:
        print(f"No se encontró 'partidos_container' en la URL: {url}")
        return []

if __name__ == '__main__':
    start_time = time.time()
    
    with open(DATOSPARTIDOS, mode='a', newline='', encoding="utf-8") as csv_file:
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
                    writer.writerow(row)
            
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tiempo total: {total_time} segundos")