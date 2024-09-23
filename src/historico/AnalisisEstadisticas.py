'''
Created on 16 abr 2023

@author: aleja
'''
from collections import namedtuple
import csv
from datetime import *
from collections import Counter
import time
Estadisticas = namedtuple("Estadisticas","fecha,competicion,local,visitante,minuto,linea,cuota,probabilidad,partidos,corners,resultado")

def lee_estadisticas (fichero):
    res = []
    with open (fichero, encoding = "utf-8") as f:
        lector = csv.reader(f, delimiter = ";")
        next(lector)
        for fecha,competicion,local,visitante,minuto,linea,cuota,probabilidad,partidos,corners,resultado in lector:
            fecha = parsea_fecha(fecha)
            minuto = int(minuto)
            # linea = parsea_linea(linea)
            cuota = float(cuota)
            probabilidad = float(probabilidad)
            partidos = int(partidos)
            corners = int(corners)
            res.append(Estadisticas(fecha,competicion,local,visitante,minuto,linea,cuota,probabilidad,partidos,corners,resultado))
    return res

# Estadisticas = namedtuple("Estadisticas","fecha,competicion,local,visitante,minuto,linea,cuota,probabilidad,partidos,cornersactuales,media,cornersfinales,resultado")
#
# def lee_estadisticas (fichero):
#     res = []
#     with open (fichero, encoding = "utf-8") as f:
#         lector = csv.reader(f, delimiter = ";")
#         next(lector)
#         for fecha,competicion,local,visitante,minuto,linea,cuota,probabilidad,partidos,cornersactuales,media,cornersfinales,resultado in lector:
#             fecha = parsea_fecha(fecha)
#             minuto = int(minuto)
#             # linea = parsea_linea(linea)
#             cuota = float(cuota)
#             probabilidad = float(probabilidad)
#             partidos = int(partidos)
#             cornersactuales = int(cornersactuales)
#             media = float(media)
#             cornersfinales = int(cornersfinales)
#             res.append(Estadisticas(fecha,competicion,local,visitante,minuto,linea,cuota,probabilidad,partidos,cornersactuales,media,cornersfinales,resultado))
#     return res
# OBJETIVO MAXIMIZAR LA PROBABILIDAD DE ACIERTO
# JUGANDO CON EL MINUTO, EL NUMERO DE APUESTAS 
# REALIZADAS POR PARTIDO, EL MERCADO MAS Y MENOS,
# LA LINEA .0 Y .5

def desglose_estadisticas (datos):
    dicc = dict()
    total_apuestas = len(datos)
    for e in datos:
        clave = e.resultado
        if clave in dicc:
            dicc[clave]+=1
        else:
            dicc[clave] = 1
    if dicc["Acierto"] and dicc["Fallo"] != 0:
        units = dicc["Acierto"]-dicc["Fallo"]
        prob = dicc["Acierto"]/(dicc["Fallo"]+dicc["Acierto"])
    return f"Total apuestas: {total_apuestas},{dicc}, Unidades: {units}, Probabilidad acierto: {round(prob,2)}, Mayor racha aciertos: {mayor_racha(datos)[0]}, Mayor racha fallos: {mayor_racha(datos)[1]}"

def mayor_racha(datos):
    aciertos = 0
    fallos = 0
    max_aciertos = 0
    max_fallos = 0
    for e in datos:
        if e.resultado == "Acierto":
            aciertos += 1
            fallos = 0
            if aciertos > max_aciertos:
                max_aciertos = aciertos
        elif e.resultado == "Fallo":
            fallos += 1
            aciertos = 0
            if fallos > max_fallos:
                max_fallos = fallos
        else:
            # Si el valor de resultado no es "Acierto" o "Fallo", ignoramos la tupla
            continue
    return (max_aciertos, max_fallos)

# def encontrar_maximo(datos):
#     max_prob = 0
#     best_x = None
#     best_y = None
#     partidos = 0
#     for x in range(0, 90):
#         for y in range(x+1, 90+1):
#             dicc = dict()
#             # datos_filtrados = [e for e in seleccionar_x_apuestas_por_partido(datos,2) if x<e.minuto<y and ("Menos" in e.linea)]
#             datos_filtrados = [e for e in seleccionar_x_apuestas_por_partido(datos,z) if x<e.minuto<y and ("Menos" in e.linea)]
#             if len(datos_filtrados) < 40:
#                 continue
#             for e in datos_filtrados:
#                 clave = e.resultado
#                 if clave in dicc:
#                     dicc[clave]+=1
#                 else:
#                     dicc[clave] = 1
#             aciertos = dicc.get("Acierto", 0)
#             fallos = dicc.get("Fallo", 0)
#             if aciertos + fallos == 0:
#                 prob = 0
#             else:
#                 prob = aciertos/(aciertos+fallos)
#             if prob > max_prob:
#                 max_prob = prob
#                 best_x = x
#                 best_y = y
#                 partidos = aciertos+fallos
#                 unidades = aciertos-fallos
#     return f"Rango minutos ({best_x},{best_y}), Probabilidad acierto: {round(max_prob,2)}, Total partidos: {partidos}, Unidades: {unidades}"

# def encontrar_maximo(datos):
#     max_prob = 0
#     best_x = None
#     best_y = None
#     best_z = None
#     best_menos = None
#     best_punto5 = None
#     best_sinfiltro = None
#     partidos = 0
#     unidades = 0
#     for x in range(0, 100):
#         for y in range(x+1, 100+1):
#             for z in range(1, 5):
#                 for menos in [True, False]:
#                     for punto5 in [True, False]:
#                         for sinfiltro in [True, False]:
#                             if sinfiltro:
#                                 dicc = dict()
#                                 datos_filtrados = [e for e in seleccionar_x_apuestas_por_partido(datos, z) if x < e.minuto < y]
#                             else:
#                                 datos_filtrados = [e for e in seleccionar_x_apuestas_por_partido(datos, z) if x < e.minuto < y and
#                                        ("Menos" in e.linea) == menos and (".5" in e.linea) == punto5]
#                             if len(datos_filtrados) < 75:
#                                 continue
#                             for e in datos_filtrados:
#                                 clave = e.resultado
#                                 if clave in dicc:
#                                     dicc[clave]+=1
#                                 else:
#                                     dicc[clave] = 1
#                             aciertos = dicc.get("Acierto", 0)
#                             fallos = dicc.get("Fallo", 0)
#                             if aciertos + fallos == 0:
#                                 prob = 0
#                             else:
#                                 prob = aciertos/(aciertos+fallos)
#                             if prob > max_prob:
#                                 max_prob = prob
#                                 best_x = x
#                                 best_y = y
#                                 best_z = z
#                                 best_menos = menos
#                                 best_punto5 = punto5
#                                 best_sinfiltro = sinfiltro
#                                 partidos = aciertos+fallos
#                                 unidades = aciertos-fallos
#     return f"Rango minutos ({best_x},{best_y}), Z = {best_z}, SinFiltros = {best_sinfiltro}, Menos = {best_menos}, .5 = {best_punto5}, Probabilidad acierto: {round(max_prob,2)}, Total partidos: {partidos}, Unidades: {unidades}"


# def encontrar_maximo(datos):
#     max_prob = 0
#     best_x = None
#     best_y = None
#     best_z = None
#     best_menos = None
#     best_punto5 = None
#     best_sinfiltro = None
#     partidos = 0
#     unidades = 0
#     for x in range(0, 100):
#         for y in range(x+1, 100+1):
#             for z in range(1, 5):
#                 for sinfiltro in [True, False]:
#                     if sinfiltro == False:
#                         for menos in [True, False]:
#                             for punto5 in [True, False]:
#                                 datos_filtrados = [e for e in seleccionar_x_apuestas_por_partido(datos, z) if x < e.minuto < y and ("Menos" in e.linea) == menos and (".5" in e.linea) == punto5]
#
#                     else:
#                         best_menos = None
#                         best_punto5 = None
#                         datos_filtrados = [e for e in seleccionar_x_apuestas_por_partido(datos, z) if x < e.minuto < y]
#                     n = len(datos_filtrados)
#                     if n < 5:
#                         continue
#                     if n == 0:
#                         continue
#                     counter = Counter(e.resultado for e in datos_filtrados)
#                     aciertos = counter.get("Acierto", 0)
#                     fallos = counter.get("Fallo", 0)
#                     if aciertos + fallos == 0:
#                         prob = 0
#                     else:
#                         prob = aciertos/(aciertos+fallos)
#                     if prob > max_prob:
#                         max_prob = prob
#                         best_x = x
#                         best_y = y
#                         best_z = z
#                         best_menos = menos
#                         best_punto5 = punto5
#                         best_sinfiltro = sinfiltro
#                         partidos = n
#                         unidades = aciertos-fallos
#     return f"Rango minutos ({best_x},{best_y}), Z = {best_z}, SinFiltros = {best_sinfiltro}, Menos = {best_menos}, .5 = {best_punto5}, Probabilidad acierto: {round(max_prob,2)}, Total partidos: {partidos}, Unidades: {unidades}"

def encontrar_maximo(datos):
    max_prob = 0
    best_x = None
    best_y = None
    best_z = None
    best_menos = None
    best_punto5 = None
    best_sinfiltro = None
    partidos = 0
    unidades = 0
    for x in range(0, 100):
        for y in range(x+1, 100+1):
            for z in range(1, 5):
                for menos in [True, False]:
                    for punto5 in [True, False]:
                        for sinfiltro in [True, False]:
                            if sinfiltro:
                                datos_filtrados = [e for e in seleccionar_x_apuestas_por_partido(datos, z) if x < e.minuto < y]
                            else:
                                datos_filtrados = [e for e in seleccionar_x_apuestas_por_partido(datos, z) if x < e.minuto < y and
                                       ("Menos" in e.linea) == menos and (".5" in e.linea) == punto5]
                            n = len(datos_filtrados)
                            if n < 100:
                                continue
                            if n == 0:
                                continue
                            counter = Counter(e.resultado for e in datos_filtrados)
                            aciertos = counter.get("Acierto", 0)
                            fallos = counter.get("Fallo", 0)
                            if aciertos + fallos == 0:
                                prob = 0
                            else:
                                prob = aciertos/(aciertos+fallos)
                            if prob > max_prob:
                                max_prob = prob
                                best_x = x
                                best_y = y
                                best_z = z
                                best_menos = menos
                                best_punto5 = punto5
                                best_sinfiltro = sinfiltro
                                apuestas = n
                                unidades = aciertos-fallos
    return f"Rango minutos ({best_x},{best_y}), Z = {best_z}, SinFiltros = {best_sinfiltro}, Menos = {best_menos}, .5 = {best_punto5}, Probabilidad acierto: {round(max_prob,2)}, Total apuestas: {apuestas}, Unidades: {unidades}"

def seleccionar_x_apuestas_por_partido(datos,x):
    # Crea un diccionario para agrupar las apuestas por partido
    partidos = {}
    for apuesta in datos:
        clave_partido = (apuesta.fecha, apuesta.competicion, apuesta.local, apuesta.visitante)
        if clave_partido not in partidos:
            partidos[clave_partido] = []
        partidos[clave_partido].append(apuesta)

    # Elige una apuesta por partido
    apuestas_seleccionadas = []
    for partido, apuestas_partido in partidos.items():
        # Ordena las apuestas por probabilidad de acierto y selecciona las dos con mayor probabilidad
        apuestas_partido_ordenadas = sorted(apuestas_partido, key=lambda x: x.minuto, reverse=False)
        apuestas_seleccionadas.extend(apuestas_partido_ordenadas[:x])

    return apuestas_seleccionadas

def media_cuotas(datos):
    return sum([e.cuota for e in datos])/len(datos)

def parsea_fecha (str):
    return datetime.strptime(str,"%d/%m/%Y").date()

if __name__ == '__main__':
    datos = lee_estadisticas("../data/Estadisticas.csv")
    # datos = [e for e in datos if e.minuto <= 45]
    # print(media_cuotas(datos))
    print(desglose_estadisticas(datos))
    n = 3
    # print("Desglose estadisticas")
    print(desglose_estadisticas(seleccionar_x_apuestas_por_partido(datos,n)))
    # start_time = time.time()
    # print("\n""Intervalo minutos y Filtros óptimos: ")
    # print(encontrar_maximo(datos))
    # end_time = time.time()
    # print(end_time - start_time)