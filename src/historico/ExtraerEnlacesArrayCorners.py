# FUNCIONA
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool

# Unicos datos que hay que cambiar
ANALISIS = '../data/Analisis(08-05-2023).csv'
DATOSPARTIDOS = '../data/EnlacesPartidos(08-05-2023).csv'
#############################################
def scrape_data(url):
    service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)

        partidos_container = driver.find_element(By.CSS_SELECTOR, "div.mainContent.main")

        partidos_local = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.homeAsHome.table--striped tbody tr")
        partidos_visitante = partidos_container.find_elements(By.CSS_SELECTOR, "table.table.awayAsAway.table--striped tbody tr")
        
        data = []
        for partido in partidos_local + partidos_visitante:
            url = partido.find_element(By.CSS_SELECTOR, " td.analysis_link > a").get_attribute("href")
            if url:
                data.append({'Url': url})
            
    except NoSuchElementException:
        print(f"No se encontró 'partidos_container' en la URL: {url}")
        data = []
        
    driver.quit()
    return data

if __name__ == '__main__':
    start_time = time.time()
    
    with open(DATOSPARTIDOS, mode='w', newline='', encoding="utf-8") as csv_file:
        fieldnames = ['Url']
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
