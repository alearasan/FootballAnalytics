from funciones.Lectura import * 
from funciones.Funciones import *
import csv
import csv
import ast
import re
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool
import pandas as pd

def test_analisis_goles_mitad_csv(datos, encuentros, output_file):
    print("Analisis >=1 gol")
    with open(output_file, 'w', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Probabilidad", "Cuota", "Local", "Visitante", "Fecha"])

        for e in analisis_goles(datos, encuentros, n=1, f=f, p=0.90):
            print(e)
            csv_writer.writerow(e)
            
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
    fecha_global = "01-09-2023"
    f = 6
    start_time = time.time()

    # datos = lee_datos_partidos("../data/DatosPartidos(14-03-2023).csv")
    datos = lee_datos_partidos_selenium(f"../data/historico/DatosPartidos({fecha_global}).csv")
    encuentros = lee_encuentros_selenium(f"../data/historico/Encuentros({fecha_global}).csv")
    test_analisis_goles_mitad_csv(datos, encuentros, f'../data/TestLista({fecha_global}).csv')

    
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
        with open(f"../data/historico/Encuentros({fecha_global}).csv", 'r', encoding='utf-8') as encuentros_file:
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

    # Leer los datos de PruebaDatosPartidos.csv
    equipos_validos = set()
    with open(f'../data/DatosPartidosMinutosGoles({fecha_global}).csv', 'r', encoding='utf-8') as minutos_goles_file:
        reader = csv.DictReader(minutos_goles_file, delimiter=';')  # Utilizar el punto y coma como delimitador
        for row in reader:
            local = row['Local']
            visitante = row['Visitante']
            equipos_validos.add(local)
            equipos_validos.add(visitante)
    
    # Leer los datos de resultados.csv y filtrar equipos válidos
    resultados_data = []
    with open(f'../data/TestLista({fecha_global}).csv', 'r', encoding='utf-8') as resultados_file:
        reader = csv.DictReader(resultados_file, delimiter=',')
        for row in reader:
            local = row['Local']
            visitante = row['Visitante']
            if local in equipos_validos and visitante in equipos_validos:
                resultados_data.append(row)
    
    # Crear un diccionario para almacenar los goles de cada partido
    minutos_goles_dict = {}
    with open(f'../data/DatosPartidosMinutosGoles({fecha_global}).csv', 'r', encoding='utf-8') as minutos_goles_file:
        reader = csv.DictReader(minutos_goles_file, delimiter=';')  # Utilizar el punto y coma como delimitador
        for row in reader:
            partido_key = f"{row['Local']};{row['Visitante']}"
            goles_local = ast.literal_eval(row['GolesLocal'])  # Usamos ast.literal_eval para convertir la cadena en una lista
            goles_visitante = ast.literal_eval(row['GolesVisitante'])
            minutos_goles_dict[partido_key] = {
                'GolesLocal': goles_local,
                'GolesVisitante': goles_visitante
            }
    
    # Combinar datos y calcular los goles en la primera mitad y los goles totales en la primera parte
    for row in resultados_data:
        partido_key = f"{row['Local']};{row['Visitante']}"
        
        # Seleccionar goles en la primera mitad para el equipo local
        goles_local_primera_mitad = [gol for gol in minutos_goles_dict.get(partido_key, {'GolesLocal': []})['GolesLocal'] if 0 <= int(gol) <= 45]
        
        # Seleccionar goles en la primera mitad para el equipo visitante
        goles_visitante_primera_mitad = [gol for gol in minutos_goles_dict.get(partido_key, {'GolesVisitante': []})['GolesVisitante'] if 0 <= int(gol) <= 45]
        
        # Calcular los goles totales en la primera parte
        goles_totales_primera_mitad = len(goles_local_primera_mitad) + len(goles_visitante_primera_mitad)
        
        # Combinar los goles en un formato deseado
        goles_local_str = str(goles_local_primera_mitad)
        goles_visitante_str = str(goles_visitante_primera_mitad)
        
        # Actualizar las columnas en la fila de resultados
        row['GolesLocal'] = goles_local_str
        row['GolesVisitante'] = goles_visitante_str
        row['GolesTotales'] = goles_totales_primera_mitad
        row['Acertada'] = goles_totales_primera_mitad > 0
    
    # Escribir los resultados en un nuevo archivo CSV
    with open(f'../data/Resultados({fecha_global}).csv', 'w', newline='', encoding='utf-8') as output_file:
        fieldnames = ['Probabilidad', 'Cuota', 'Local', 'Visitante', 'Fecha', 'GolesLocal', 'GolesVisitante', 'GolesTotales', 'Acertada']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in resultados_data:
            writer.writerow(row)