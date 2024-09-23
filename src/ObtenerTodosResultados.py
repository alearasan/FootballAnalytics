import pandas as pd
import os
from datetime import datetime, timedelta
import time

start_time = time.time()

# Definir la fecha inicial y final
fecha_inicial = datetime.strptime("01-01-2022", "%d-%m-%Y")
fecha_actual = datetime.now()

# Crear una lista de fechas desde la fecha_inicial hasta la fecha_actual
fechas = [fecha_inicial + timedelta(days=d) for d in range((fecha_actual - fecha_inicial).days + 1)]

# Crear un DataFrame vacío para almacenar todos los datos
datos_combinados = pd.DataFrame()

# Iterar a través de las fechas y procesar los archivos
for fecha in fechas:
    # Convierte la fecha en el formato deseado (por ejemplo, "08-04-2023")
    fecha_str = fecha.strftime("%d-%m-%Y")
    
    # Construye la ruta del archivo con la fecha actual
    ruta_archivo = f"../data/Resultados1({fecha_str}).csv"
    
    # Verifica si el archivo existe
    if os.path.exists(ruta_archivo):
        # Carga el archivo CSV en un DataFrame de pandas
        df = pd.read_csv(ruta_archivo)
        
        # Agrega los datos del archivo actual al DataFrame combinado
        datos_combinados = pd.concat([datos_combinados, df], ignore_index=True)

# Guarda el DataFrame combinado en un nuevo archivo CSV
datos_combinados.to_csv("../data/Resultados_Combinados1.csv", index=False)

end_time = time.time()
total_time = end_time - start_time

print(f"Tiempo total: {total_time} segundos")
