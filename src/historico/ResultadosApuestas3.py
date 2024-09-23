import csv
import ast

fecha_global = "10-10-2023"

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
