def formatear_texto(texto):
    # Dividir el texto en líneas
    lineas = texto.strip().split("\n")

    # Lista para almacenar resultados formateados
    resultados_formateados = []

    # Iterar sobre cada línea y formatear el texto
    for linea in lineas:
        # Eliminar paréntesis y comillas
        linea = linea.replace("(", "").replace(")", "").replace("'", "")

        # Dividir campos por ,
        campos = linea.split(",")
        
        # Cambiar . por ,
        linea = linea.replace(".", ",")

        # Reorganizar los campos para que la fecha sea el primer elemento
        campos_reorganizados = [campos[-1]] + campos[:-1]
        
        # Reorganizar los campos y unirlos con ;
        resultado = ";".join(campos_reorganizados)
        
        # Agregar resultado a la lista
        resultados_formateados.append(resultado)

    return resultados_formateados

# Texto de entrada con varias líneas
texto_entrada = """
(0.94, 5.18, 'St. Albans Saints U23', 'Hume City U23', '2024-06-23 04:00')
(1.0, 5.6, 'Melbourne Knights U23', 'Moreland City U23', '2024-06-23 08:00')
(0.93, 4.93, 'Perth RedStar W', 'Murdoch Uni Melville W', '2024-06-23 09:00')
(0.95, 4.81, 'FH', 'Fylkir', '2024-06-23 21:15')
"""


# Formatear el texto y obtener resultados
resultados_formateados = formatear_texto(texto_entrada)

# Imprimir los resultados
for resultado in resultados_formateados:
    print(resultado)
