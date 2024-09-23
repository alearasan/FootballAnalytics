import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool

# Unicos datos que hay que cambiar
ENLACESPARTIDOS = '../data/EnlacesPartidos(20-04-2023).csv'
DATOSPARTIDOS = '../data/DatosPartidosMinutosCorners(20-04-2023).csv'
#############################################
def scrape_data(url):
    service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Scraping/Corners/Controlador Chrome/chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    data = []
    try:
        driver.get(url)
        boton = driver.find_element(By.CSS_SELECTOR, 'div.mainContent.live.analysis_live > div.side > div > div:nth-child(1) > div.header.cpa-flex-col > div.events_toggle > button:nth-child(3)')
        boton.click()
    # Encontrar los elementos
        elementos = driver.find_elements(By.CSS_SELECTOR, "div.mainContent.live.analysis_live")
        corners_wrapper = driver.find_element(By.CSS_SELECTOR, 'div.mainContent.live.analysis_live > div.side > div > div:nth-child(1) > div.content.events_wrapper > div:nth-child(3)')
        corners = corners_wrapper.find_elements(By.CSS_SELECTOR, 'div:nth-child(n)')

        home_elementos = []
        away_elementos = []

    # Recorrer los elementos y agregar solo aquellos que estén visibles al archivo CSV

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
                if len(home_elementos)!= 0 or len(away_elementos)!=0:
                    data.append({"Fecha": fecha,'Local': local,'Visitante': visitante, "ArrayLocal":home_elementos,"ArrayVisitante":away_elementos})
                    print((fecha, local, visitante))
                    print(home_elementos)
                    print(away_elementos)
    except NoSuchElementException:
        print(f"Error en la url: {url}")


    driver.quit()
    return data

if __name__ == '__main__':
    start_time = time.time()
    with open(DATOSPARTIDOS, "w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ['Fecha','Local', 'Visitante', 'ArrayLocal','ArrayVisitante']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter = ";")
        writer.writeheader()
        
        with open(ENLACESPARTIDOS) as f:
            reader = csv.reader(f)
            next(reader)
            urls = [row[0] for row in reader]

            with Pool() as p:
                results = p.map(scrape_data, urls)
                
            for result in results:
                try:
                    for row in result:
                        if row != "":
                            writer.writerow(row)
                except Exception:
                    continue
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tiempo total: {total_time} segundos")
