import pandas as pd
import ast

def cargar_datos(ruta_archivo):
    df = pd.read_csv(ruta_archivo)
    # Convierte las cadenas en listas
    df['GolesLocal'] = df['GolesLocal'].apply(lambda x: ast.literal_eval(x))
    df['GolesVisitante'] = df['GolesVisitante'].apply(lambda x: ast.literal_eval(x))
    return df

def probabilidad_todos_acertados(ruta_archivo):
    # Cargar datos
    df = cargar_datos(ruta_archivo)

    # Eliminar filas con valores no válidos en la columna 'Fecha'
    df = df[df['Fecha'].str.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', na=False)]

    # Convertir la columna 'Fecha' a tipo 'datetime'
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

    # Crear una nueva columna 'Fecha_solo_dia' que contenga solo la fecha (sin la hora)
    df['Fecha_solo_dia'] = df['Fecha'].dt.date
    # Filtrar solo los días donde el número de partidos es igual al número de aciertos
    dias_validos = df[df.groupby('Fecha_solo_dia')['Fecha'].transform('count') == df.groupby('Fecha_solo_dia')['Acertada'].transform('sum')]

    # Calcular la probabilidad
    probabilidad = len(dias_validos['Fecha_solo_dia'].unique()) / len(df['Fecha_solo_dia'].unique())

    return probabilidad, 1/probabilidad


def probabilidad_todos_acertados_por_num_partidos(ruta_archivo, numero_partidos):
    # Cargar datos
    df = cargar_datos(ruta_archivo)
    cuota_equilibrio = 0
    # Eliminar filas con valores no válidos en la columna 'Fecha'
    df = df[df['Fecha'].str.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', na=False)]

    # Convertir la columna 'Fecha' a tipo 'datetime'
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

    # Crear una nueva columna 'Fecha_solo_dia' que contenga solo la fecha (sin la hora)
    df['Fecha_solo_dia'] = df['Fecha'].dt.date
    
    # Verificar si hay días disponibles para el número de partidos dado
    if numero_partidos not in df.groupby('Fecha_solo_dia')['Fecha'].count().value_counts().index:
        return None

    # Filtrar solo los días con el número deseado de partidos
    df_filtrado = df[df.groupby('Fecha_solo_dia')['Fecha'].transform('count') == numero_partidos]

    # Filtrar solo los días donde el número de partidos es igual al número de aciertos
    dias_validos = df_filtrado[df_filtrado.groupby('Fecha_solo_dia')['Fecha'].transform('count') == df_filtrado.groupby('Fecha_solo_dia')['Acertada'].transform('sum')]

    # Calcular la probabilidad
    probabilidad = len(dias_validos['Fecha_solo_dia'].unique()) / len(df_filtrado['Fecha_solo_dia'].unique())
    
    if probabilidad != 0:
        # Calcular la cuota de equilibrio
        cuota_equilibrio = 1 / probabilidad

    return probabilidad, cuota_equilibrio
if __name__ == "__main__":
    # Ruta del archivo de datos
    ruta_archivo_ejemplo = "../data/Resultados_Combinados.csv"
    
    # Llamada a la función desde el bloque principal
    resultado_prob, cuota_eq = probabilidad_todos_acertados(ruta_archivo_ejemplo)
    print(f"Probabilidad de que todos los partidos de un día sean True: Probabilidad = {resultado_prob:.4f}, Cuota equilibrio = {cuota_eq:.2f}")

    # Crear una lista con diferentes números de partidos
    numeros_partidos = list(range(1, 100))

    # Iterar sobre los diferentes números de partidos
    for numero_partidos_deseado in numeros_partidos:
        # Llamada a la función
        resultado = probabilidad_todos_acertados_por_num_partidos(ruta_archivo_ejemplo, numero_partidos_deseado)

        if resultado is not None:
            # Mostrar los resultados en la consola
            probabilidad, cuota_equilibrio = resultado
            print(f"Para días con {numero_partidos_deseado} partidos: {probabilidad:.2f}, {cuota_equilibrio:.2f}")
        