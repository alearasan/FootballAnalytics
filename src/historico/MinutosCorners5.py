#FUNCIONA PERO SI PILLA MUCHAS URL NO EXISTENTES SE RALLA

from selenium.common.exceptions import NoSuchElementException
import csv
import time
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

def scrape_data(url):
        try:
            driver.get(url)
            wait = WebDriverWait(driver, 1)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mainContent.live.analysis_live > div.side > div > div:nth-child(1) > div.header.cpa-flex-col > div.events_toggle > button:nth-child(3)')))
            boton = driver.find_element(By.CSS_SELECTOR, 'div.mainContent.live.analysis_live > div.side > div > div:nth-child(1) > div.header.cpa-flex-col > div.events_toggle > button:nth-child(3)')
            boton.click()
            elementos = driver.find_elements(By.CSS_SELECTOR, "div.mainContent.live.analysis_live")
            corners_wrapper = driver.find_element(By.CSS_SELECTOR, 'div.mainContent.live.analysis_live > div.side > div > div:nth-child(1) > div.content.events_wrapper > div:nth-child(3)')
            corners = corners_wrapper.find_elements(By.CSS_SELECTOR, 'div:nth-child(n)')
            home_elementos = []
            away_elementos = []
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
                        with open('../data/DatosPartidosMinutosCorners(20-04-2023).csv', "a", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f, delimiter = ";")
                            writer.writerow([fecha, local, visitante, home_elementos,away_elementos])
                            print((fecha, local, visitante))
                            print(home_elementos)
                            print(away_elementos)
        except Exception:
            print(f"Error en la url: {url}")

if __name__ == '__main__':
    start_time = time.time()
    urls = []
    with open('../data/EnlacesPartidos(20-04-2023).csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)  # skip header row
        for row in reader:
            urls.append(row[0])
    with Pool(5) as p:
        p.map(scrape_data, urls)
    driver.quit()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tiempo total: {total_time} segundos")