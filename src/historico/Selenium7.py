# FUNCIONA
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Unicos datos que hay que cambiar
fecha_global = "19-01-2024"
ANALISIS = f'../data/Analisis({fecha_global}).csv'
ENCUENTROS = f'../data/Encuentros({fecha_global}).csv'
DIA = "#day19"
#############################################

# service = Service("C:/Users/aleja/OneDrive/Escritorio/HACKING/Proyectos/Scraping/Corners/Controlador Chrome/chromedriver.exe")
# driver = webdriver.Chrome(service=service)
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

start_time = time.time()

# driver = webdriver.Chrome(options=options,service=service)
driver = webdriver.Chrome(options=options)

driver.get("https://cornerprobet.com/")

time.sleep(2)
# start_time = time.time()
#app > div.page > section > div.navigation > button.cpa_tab_btn.cpa_tab_btn--active
boton = driver.find_element(By.CSS_SELECTOR, "#days > option:nth-child(7)") # option:nth-child(6) para mañana max 10
# boton = driver.find_element(By.CSS_SELECTOR, "#app > div.page > section.filtered > div.cpa_section.filtered_games.all_games > div.header > div.cpa-flex-row.showFilters > button:nth-child(3)") #para coger los schedule
boton.click()
time.sleep(2)
# Esperar a que la página se cargue completamente
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, DIA)))
# Obtener los elementos con los selectores CSS especificados
elementos = driver.find_elements(By.CSS_SELECTOR, "div.game_info")
#day13#gqfels > div.game_info
# Recorrer los elementos y agregar solo aquellos que estén visibles al archivo CSV
with open(ENCUENTROS, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter = ";")
    writer.writerow(["Local", "Tiempo", "Visitante", "Analisis"])
    print(driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div.league_header > div.logo_name > p").text)
    for elemento in elementos:
        #day04 > div:nth-child(1) > div.league_header > div.logo_name > p
        #day04 > div:nth-child(1) > div.league_header > div.logo_name > p
        #day04 > div:nth-child(2) > div.league_header > div.logo_name > p
        # Verificar si el elemento está visible
        if elemento.is_displayed():
            local = elemento.find_element(By.CSS_SELECTOR, "div:nth-child(3) > a").text#gqqgqj > div.game_info > div:nth-child(3) > a
            tiempo = elemento.find_element(By.CSS_SELECTOR, "div.cpa-flex-col > span").text
            visitante = elemento.find_element(By.CSS_SELECTOR, "div.cpa-flex-row.cpa-align-center.cpa-flex-row--collapse.cpa-flex-row--reverse > a").text
            url = elemento.find_element(By.CSS_SELECTOR, "div.links > a.link_analysis").get_attribute("href")
            writer.writerow([local, tiempo, visitante, url])
            # Imprimir la tupla en la consola (opcional)
            print((local, tiempo, visitante, url))

# Abrir el archivo original
with open(ENCUENTROS, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    header = next(reader)  # Leer la primera fila (encabezado)

    # Encontrar el índice de la columna "Analisis" en el encabezado
    analisis_index = header.index("Analisis")

    # Abrir el nuevo archivo CSV y escribir el encabezado
    with open(ANALISIS, "w", newline="", encoding="utf-8") as fw:
        writer = csv.writer(fw)
        writer.writerow(["Analisis"])

        # Leer las filas del archivo original y escribir solo la columna "Analisis"
        for row in reader:
            analisis = row[analisis_index]
            writer.writerow([analisis])

driver.quit()

end_time = time.time()
total_time = end_time - start_time
print(f"Tiempo total: {round(total_time,0)} segundos")
