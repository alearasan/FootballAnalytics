import pandas as pd
import ast
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from telebot.formatting import mitalic
import numpy as np


# Función para leer el archivo CSV y realizar conversiones
def cargar_datos(ruta_archivo):
    df = pd.read_csv(ruta_archivo)
    # Convierte las cadenas en listas
    df['GolesLocal'] = df['GolesLocal'].apply(lambda x: ast.literal_eval(x))
    df['GolesVisitante'] = df['GolesVisitante'].apply(lambda x: ast.literal_eval(x))
    return df

# Función para filtrar partidos según el minuto mínimo
def filtrar_partidos(df, minuto):
    def seleccion_partidos(lista):
        return all(int(gol) > minuto for gol in lista)

    df_filtrado = df[df['GolesLocal'].apply(seleccion_partidos) & df['GolesVisitante'].apply(seleccion_partidos)]
    return df_filtrado

# Función para calcular la probabilidad de 2 o más goles en un partido
def calcular_probabilidad_2_o_mas_goles(df):
    def dos_o_mas_goles(row):
        return (len(row['GolesLocal']) + len(row['GolesVisitante'])) >= 2

    partidos_con_dos_o_mas_goles = df.apply(dos_o_mas_goles, axis=1)
    return partidos_con_dos_o_mas_goles.sum() / len(df)

# Función para calcular el minuto del primer gol en un partido
def calcular_minuto_primer_gol(df):
    def minuto_primer_gol(lista_local, lista_visitante):
        minutos_goles = [int(gol) for gol in lista_local + lista_visitante if gol]
        return min(minutos_goles) if minutos_goles else None

    df['MinutoPrimerGol'] = df.apply(lambda row: minuto_primer_gol(row['GolesLocal'], row['GolesVisitante']), axis=1)
    return df, df['MinutoPrimerGol'].mean()


# Función para calcular la probabilidad de al menos dos goles después de un gol
def calcular_probabilidad_al_menos_dos_goles(df):
    partidos_con_un_gol_o_mas = df[(df['GolesLocal'].apply(len) > 0) | (df['GolesVisitante'].apply(len) > 0)]
    def al_menos_dos_goles(row):
        return len(row['GolesLocal']) + len(row['GolesVisitante']) > 1

    partidos_con_al_menos_dos_goles = partidos_con_un_gol_o_mas.apply(al_menos_dos_goles, axis=1)
    return partidos_con_al_menos_dos_goles.sum() / len(partidos_con_un_gol_o_mas)

def mostrar_grafico_probabilidad_acumulada(df):
    plt.figure(figsize=(12, 6))
    # Conteo de partidos por minuto del primer gol
    conteo_minutos_primer_gol = df['MinutoPrimerGol'].value_counts().sort_index()
    # Cálculo de la probabilidad
    total_partidos = len(df)
    probabilidad = conteo_minutos_primer_gol / total_partidos
    # Cálculo de la probabilidad acumulada
    probabilidad_acumulada = probabilidad.cumsum()
    # Calcular la diferencia entre cada minuto y el siguiente
    diferencia_probabilidad = probabilidad_acumulada.diff().fillna(0)
    plt.plot(diferencia_probabilidad.index, diferencia_probabilidad.values, color='skyblue', marker='o', linestyle='-')
    plt.title('Diferencia en la Probabilidad Acumulada entre Minutos')
    plt.xlabel('Minuto')
    plt.ylabel('Diferencia en Probabilidad Acumulada')
    plt.grid(axis='y')
    plt.show()

def mostrar_grafico_barras_minuto_primer_gol(df):
    plt.figure(figsize=(12, 6))
    # Conteo de partidos por minuto del primer gol
    conteo_minutos_primer_gol = df['MinutoPrimerGol'].value_counts().sort_index()
    # Crear el gráfico de barras
    plt.bar(conteo_minutos_primer_gol.index, conteo_minutos_primer_gol.values, color='skyblue')
    plt.title('Número de Partidos vs Minuto del Primer Gol')
    plt.xlabel('Minuto del Primer Gol')
    plt.ylabel('Número de Partidos')
    plt.grid(axis='y')
    plt.show()

def calcular_probabilidad_dos_goles_por_cuota(df):
    # Define los intervalos de cuotas (ajusta según tus datos)
    intervalos_cuotas = [1.0, 1.5, 2.0, 2.5, 3.0]
    probabilidades_por_cuota = []

    for i in range(len(intervalos_cuotas) - 1):
        cuota_inferior = intervalos_cuotas[i]
        cuota_superior = intervalos_cuotas[i + 1]

        partidos_en_intervalo = df[(df["Cuota"] >= cuota_inferior) & (df["Cuota"] < cuota_superior)]
        probabilidad_dos_goles = len(partidos_en_intervalo[partidos_en_intervalo["GolesTotales"] >= 2]) / len(partidos_en_intervalo)
        probabilidades_por_cuota.append((cuota_inferior, cuota_superior, probabilidad_dos_goles))

    return probabilidades_por_cuota

def calcular_minuto_primer_gol_por_cuota(df):
    # Define los intervalos de cuotas (ajusta según tus datos)
    intervalos_cuotas = [1.0, 1.5, 2.0, 2.5, 3.0]
    minuto_primer_gol_por_cuota = []
    
    for i in range(len(intervalos_cuotas) - 1):
        cuota_inferior = intervalos_cuotas[i]
        cuota_superior = intervalos_cuotas[i + 1]

        partidos_en_intervalo = df[(df["Cuota"] >= cuota_inferior) & (df["Cuota"] < cuota_superior)].copy()  # Copia el DataFrame
        df_con_minutos, minuto_primer_gol = calcular_minuto_primer_gol(partidos_en_intervalo)
        minuto_primer_gol_por_cuota.append((cuota_inferior, cuota_superior, minuto_primer_gol))

    return minuto_primer_gol_por_cuota

def calcular_linea(df, cuota_media, importe, goles_necesarios):
    partidos_sin_goles = len(df[df["GolesTotales"] == 0])
    partidos_con_goles = len(df[df["GolesTotales"] >= goles_necesarios])
    ganancias_sin_goles = -importe * partidos_sin_goles
    ganancias_con_goles = (cuota_media * importe - importe) * partidos_con_goles
    ganancias_totales = ganancias_sin_goles + ganancias_con_goles
    return ganancias_totales

def calcular_ganancias_por_cuota(df, cuotas, importe, goles_necesarios):
    ganancias_por_cuota = {}
    for minuto, cuota in enumerate(cuotas, start=1):
        df_filtrado = filtrar_partidos(df, minuto)
        ganancias = calcular_linea(df_filtrado, cuota, importe, goles_necesarios)
        ganancias_por_cuota[minuto] = ganancias
    return ganancias_por_cuota

def mostrar_grafico_ganancias_por_minuto(ganancias_linea_0_5_dict, ganancias_linea_1_0_dict):
    minutos = np.arange(1, 43)
    ganancias_linea_0_5 = [ganancias_linea_0_5_dict.get(minuto, np.nan) for minuto in minutos]
    ganancias_linea_1_0 = [ganancias_linea_1_0_dict.get(minuto, np.nan) for minuto in minutos]

    plt.figure(figsize=(12, 6))
    plt.plot(minutos, ganancias_linea_0_5, label='Linea 0.5', marker='o', linestyle='-', color='b')
    plt.plot(minutos, ganancias_linea_1_0, label='Linea 1.0', marker='o', linestyle='-', color='g')
    plt.xlabel('Minuto')
    plt.ylabel('Ganancias (€)')
    plt.title('Ganancias de Estrategia de Apuestas cada Minuto')
    plt.legend()
    plt.grid(True)
    plt.show()

def encontrar_cuota_media_para_ganancia_cero(df, importe, goles_necesarios):
    minutos = list(range(1, 21))
    cuotas_necesarias = []
    
    # Itera a través de los minutos
    for minuto in minutos:
        cuota = 1.15  # Inicializa la cuota con un valor bajo
    
        # Usa un bucle para encontrar la cuota necesaria para ganancia cero
        while True:
            ganancia = calcular_linea(filtrar_partidos(df, minuto), cuota, importe, goles_necesarios)
            if ganancia >= 0:
                cuotas_necesarias.append(cuota)
                break
            cuota += 0.005  # Incrementa la cuota en un pequeño paso
    
    # Graficar los resultados
    plt.bar(minutos, cuotas_necesarias)
    plt.xlabel('Minuto')
    plt.ylabel('Cuota necesaria')
    plt.title('Cuota mínima necesaria (LINEA 0_5)')
    plt.xticks(minutos)
    plt.ylim(1.20, 1.50)
    plt.yticks(np.arange(1.2, 1.55, 0.05))  # Establece las cuotas en el eje y
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)  # Agrega líneas horizontales
    plt.show()
    
def encontrar_cuota_media_para_ganancia(df,cuotas_05, importe, goles_necesarios):
    minutos = list(range(1, 41))
    cuotas_necesarias = []
    
    # Itera a través de los minutos
    for minuto in minutos:
        cuota = 1.0  # Inicializa la cuota con un valor bajo
    
        # Usa un bucle para encontrar la cuota necesaria para ganancia cero
        while True:
            ganancia = calcular_linea(filtrar_partidos(df, minuto), cuota, importe, goles_necesarios)
            if ganancia >= 0:
                cuotas_necesarias.append(cuota)
                break
            cuota += 0.01  # Incrementa la cuota en un pequeño paso
    
    cuotas_05.extend([0] * (len(minutos) - len(cuotas_05)))
    # Graficar los resultados
    plt.bar(minutos, cuotas_necesarias, color='blue', alpha=0.5, label='Cuota necesaria')
    plt.xlabel('Minuto')
    plt.ylabel('Cuota necesaria')
    plt.title('Cuota necesaria para ganancia cero por minuto')
    
    # Puntos de cuotas_05
    plt.scatter(minutos[:len(cuotas_05)], cuotas_05, color='red', label='Cuotas 0.5')
    
    plt.xticks(minutos)
    plt.ylim(1.15, 3.0)
    plt.yticks(np.arange(1.15, 3.05, 0.05))  # Establece las cuotas en el eje y
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)  # Agrega líneas horizontales
    plt.legend()
    plt.show()

def calcular_ganancias_acumuladas(df, cuota_media_05, cuota_media_10, importe):
    # Filtra las filas con fechas válidas y convierte la columna 'Fecha' en tipo 'Timestamp'
    df = df[df['Fecha'].str.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', na=False)]  # Filtra las fechas con el formato correcto
    df.loc[:, 'Fecha'] = pd.to_datetime(df['Fecha'])

    fechas_unicas = df['Fecha'].unique()
    ganancias_05_acumuladas = []
    ganancias_10_acumuladas = []

    for fecha in fechas_unicas:
        partidos_hasta_fecha = df[df['Fecha'] <= fecha]
        ganancia_05 = calcular_linea(partidos_hasta_fecha, cuota_media_05, importe, 1)
        ganancia_10 = calcular_linea(partidos_hasta_fecha, cuota_media_10, importe, 2)

        ganancias_05_acumuladas.append(ganancia_05)
        ganancias_10_acumuladas.append(ganancia_10)
        
    # Convierte la fecha de inicio al formato adecuado
    fecha_inicio = pd.to_datetime('2023-08-28 00:00', format='%Y-%m-%d %H:%M')  # Ajusta la fecha según tus datos
    # Filtra las fechas a partir del 28 de agosto
    fechas_unicas = fechas_unicas[fechas_unicas >= fecha_inicio]
    
    # Crea un gráfico de líneas para visualizar las ganancias acumuladas
    plt.figure(figsize=(12, 6))
    plt.plot(fechas_unicas, ganancias_05_acumuladas[-len(fechas_unicas):], marker='o', linestyle='-', markersize=3, label='Cuota Media 0.5')
    plt.plot(fechas_unicas, ganancias_10_acumuladas[-len(fechas_unicas):], marker='o', linestyle='-', markersize=3, label='Cuota Media 1.0')
    plt.title ('Ganancias acumuladas a lo largo del tiempo')
    plt.xlabel('Fecha del partido')
    plt.ylabel('Ganancias acumuladas')
    plt.legend()  # Agregar una leyenda para las líneas

    # Configura los intervalos de fecha en el eje x (en este caso, cada 5 días)
    ax = plt.gca()
    locator = mdates.DayLocator(interval=3)
    formatter = mdates.DateFormatter("%m-%d")
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()
    

if __name__ == "__main__":
    ruta_archivo = "../data/Resultados_Combinados1.csv"
    df = cargar_datos(ruta_archivo)
    # minuto = 0
    #
    # df_filtrado = filtrar_partidos(df, minuto)
    # Convertir la columna "Probabilidad2" a números (si aún no lo está)
    df['Probabilidad2'] = pd.to_numeric(df['Probabilidad2'], errors='coerce')
    
    # Filtrar los datos donde la probabilidad2 sea mayor de 0.5
    df_filtrado = df[df['Probabilidad2'] > 0]
    numero_aciertos = df_filtrado["Acertada"].sum()
    numero_apuestas_totales = len(df) - 1
    numero_apuestas = len(df_filtrado) - 1
    probabilidad_acierto = round(numero_aciertos / numero_apuestas, 4)
    cuota_equilibrio = (1 / probabilidad_acierto)

    print(f"Número total apuestas: {numero_apuestas_totales}")
    print("")
    # print(f"Apostando a partir del minuto: {minuto}")
    print(f"Número apuestas seleccionadas: {numero_apuestas}")
    print(f"Ratio acierto/seleccionadas {probabilidad_acierto}")
    print(f"La cuota equilibrio para un ratio de acierto/total de {probabilidad_acierto} es: {round(cuota_equilibrio, 3)}")
    probabilidad_dos_o_mas_goles_seleccionados = calcular_probabilidad_2_o_mas_goles(df_filtrado)
    print(f"Probabilidad 2 o más goles: {probabilidad_dos_o_mas_goles_seleccionados:.4f}")
    print("")
    df, minuto_medio = calcular_minuto_primer_gol(df)
    print(f"El minuto medio del primer gol en los partidos es: {minuto_medio:.2f}")

    probabilidad_dos_o_mas_goles = calcular_probabilidad_2_o_mas_goles(df)
    print(f"La probabilidad de que haya 2 o más goles en un partido es: {probabilidad_dos_o_mas_goles:.4f}")

    probabilidad_al_menos_dos_goles = calcular_probabilidad_al_menos_dos_goles(df)
    print(f"La probabilidad de que en los partidos en los que ya haya un gol, haya al menos otro gol más es: {probabilidad_al_menos_dos_goles:.4f}")
    
    print("")    
    # encontrar_cuota_media_para_ganancia_cero(df, importe=5, goles_necesarios=1)
    # print("")
    # cuotas_10 = [1.8, 1.85, 1.9, 1.975, 2.025, 2.075, 2.1, 2.1, 2.1, 2.250, 2.3, 2.4, 2.4, 2.55, 2.625, 2.825, 2.95, 3.075, 3.2, 3.4, 3.6, 3.8, 4.0, 4.45, 4.8, 5.0, 5.6, 6.6]
    # cuotas_05 = [0.0,  0,   0,  0,    0,   0 ,  0,    1.35,1.375,1.375,1.375,1.375,1.375,1.4,  1.4,  1.425,1.425,1.475,1.5,1.5, 1.525,1.575,1.625,1.65,1.675,1.8,1.8, 1.85,1.9,1.925,2.05,2.15,2.25,2.35,2.45,2.65]
    # encontrar_cuota_media_para_ganancia(df, cuotas_05, importe=5, goles_necesarios=1)

    probabilidades_dos_goles_por_cuota = calcular_probabilidad_dos_goles_por_cuota(df)
    print("Probabilidad de 2 goles o más en función de la media:")
    for cuota_inf, cuota_sup, probabilidad in probabilidades_dos_goles_por_cuota:
        print(f"-> Media goles ({cuota_inf}-{cuota_sup}): {probabilidad:.2f}")
        
    print("")    

    print("Ganancias apostando prepartido con importe 5€:")
    cuota_media_05 = 1.28
    linea_05 = calcular_linea(df_filtrado, cuota_media_05, importe=5, goles_necesarios=1)
    cuota_media_10 = 1.59
    linea_10 = calcular_linea(df_filtrado, cuota_media_10, importe=5, goles_necesarios=2)
    cuota_media_075 = (cuota_media_05 + cuota_media_10) / 2
    linea_075 = (linea_05 + linea_10) / 2
    print(f"-> Linea_0.5 para cuota media {cuota_media_05}: {linea_05:.2f}")
    print(f"-> Linea_0.75 para cuota media {cuota_media_075}: {linea_075:.2f}")
    print(f"-> Linea_1.0 para cuota media {cuota_media_10}: {linea_10:.2f}")
    print(f"-> Ganancias totales: ",round(linea_05 +linea_10+(linea_05 +linea_10)/2, 2)) 
    
    # Implementar una grafica con las ganancias que habria tenido a medida que pasa el tiempo, fijandome en la fecha del partido
    # Tomando como referencia la cuota media de todos los partidos que tengo apuntados
    calcular_ganancias_acumuladas(df_filtrado,cuota_media_05,cuota_media_10,5)
    print("")    

    minuto_primer_gol_por_cuota = calcular_minuto_primer_gol_por_cuota(df)
    print("Minuto medio primer gol en función de la media:")
    for cuota_inf, cuota_sup, minuto_medio in minuto_primer_gol_por_cuota:
        print(f"-> Media goles ({cuota_inf}-{cuota_sup}): {minuto_medio:.2f}")
        
    # cuotas_05 = [1.375,1.4,  1.4, 1.425,1.425,1.45, 1.475,1.5,  1.5,1.525,1.525,1.575,1.575,1.6, 1.65, 1.65, 1.7,  1.775,1.8, 1.85,1.9,1.95,2.0,1.975,2.075,2.1,  2.2,  2.3, 2.375,2.425,2.5,2.6,2.675,2.75,2.85,3.3,3.45,3.7,4.1,4.1]
    # cuotas_075 = [1.5, 1.525,1.55,1.575,1.6,  1.625,1.65, 1.725,1.7,1.75, 1.8,  1.85, 1.875,1.9, 2.0,  2.025,2.075,2.1,  2.15,2.2, 2.3,2.35,2.4,2.4,  2.625,2.625,2.825,2.95,3.2,  3.4,  3.5,3.5,3.6,  3.9, 4.15,4.8,5.2, 5.4,6.4,6.4]
    # cuotas_10 = [1.8,  1.85, 1.9, 1.95,2.025,2.075,2.1,  2.1,  2.1,2.250,2.3,  2.4,  2.4,  2.55,2.625,2.825,2.95, 3.075,3.2, 3.4, 3.6,3.8, 4.0,4.45, 4.8,  5.0,  5.6,  6.6]


    # Simulación estrategia apostando cada minuto:
    importe = 5
    cuotas_05 = [1.25, 1.275,1.275,1.3,  1.3, 1.325,1.325,1.35,1.375,1.375,1.375,1.375,1.375,1.4,  1.4,  1.425,1.425,1.475,1.5,1.5, 1.525,1.575,1.625,1.65,1.675,1.8,1.8, 1.85,1.9,1.925,2.05,2.15,2.25,2.35,2.45,2.65]
    cuotas_10 = [1.5,1.55, 1.6,  1.625,1.65,1.65, 1.725,1.8, 1.825,1.825,1.825,1.85, 1.9,  1.925,1.925,2.0,  2.0,  2.2,  2.2,2.25,2.35, 2.5,  2.6,  2.75,2.85, 3.3,3.45,3.45,3.7,3.8,  4.5, 5.25,5.9, 6.8, 8.0, 9.0]
    

    ganancias_linea_0_5_dict = calcular_ganancias_por_cuota(df, cuotas_05, importe, goles_necesarios=1)
    
    ganancias_linea_1_0_dict = calcular_ganancias_por_cuota(df, cuotas_10, importe, goles_necesarios=2)
    
    mostrar_grafico_ganancias_por_minuto(ganancias_linea_0_5_dict, ganancias_linea_1_0_dict)
    # mostrar_grafico_probabilidad_acumulada(df)
    # mostrar_grafico_barras_minuto_primer_gol(df)
