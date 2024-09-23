import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool

fecha_global = "23-06-2024"
ANALISIS = f'../data/Analisis({fecha_global}).csv'
DATOSPARTIDOS = f'../data/DatosPartidos({fecha_global}).csv'

def scrape_data(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        partidos_container = driver.find_element(By.CSS_SELECTOR, "div.mainContent.main")

        partidos = partidos_container.find_elements(By.CSS_SELECTOR, "div.h2h_games div:nth-child(1) table tbody tr, table.table.homeAsHome.table--striped tbody tr, table.table.awayAsAway.table--striped tbody tr")
        
        data = set()

        for partido in partidos:
            fecha, local, resultado, visitante, corners = [partido.find_element(By.CSS_SELECTOR, f"td:nth-child({i})").text.replace(' 🟢', '') for i in range(2, 7)]

            if local and fecha and visitante and resultado and corners not in ("0-0", "0-0 ( 0-0)"):
                match_tuple = (fecha, local, resultado, visitante, corners)
                data.add(match_tuple)

        return data
            
    except NoSuchElementException:
        print(f"No se encontró 'partidos_container' en la URL: {url}")
        return set()
    finally:
        driver.quit()

if __name__ == '__main__':
    start_time = time.time()

    with open(DATOSPARTIDOS, mode='w', newline='', encoding="utf-8") as csv_file:
        fieldnames = ['Fecha', 'Local', 'Resultado', 'Visitante', 'Corners']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        with open(ANALISIS) as f:
            reader = csv.reader(f)
            next(reader)
            urls = [row[0] for row in reader]

            with Pool() as p:
                results = p.map(scrape_data, urls)

            for result in results:
                for match in result:
                    writer.writerow({'Fecha': match[0], 'Local': match[1], 'Resultado': match[2], 'Visitante': match[3], 'Corners': match[4]})

    print(f"Tiempo total: {round(time.time() - start_time, 0)} segundos")
