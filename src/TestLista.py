'''
Created on 17 nov 2022

@author: aleja
'''
from funciones.Lectura import * 
from funciones.Funciones import *
import csv

freq = 6  # definir f como constante --> 6
hora_actual = datetime.now().time() 
from datetime import datetime

def imprime_segun_hora_mas(e,n):
    if  e[5] == "Postponed" or (datetime.strptime(e[4], '%Y-%m-%d %H:%M').hour >= hora_actual.hour-2):
        if e[5] != "Postponed":
            return "+",n ,e
    return None

def imprime_segun_hora_menos(e,n):
    if  e[4] == "Postponed" or (datetime.strptime(e[4], '%Y-%m-%d %H:%M').hour >= hora_actual.hour-2):
        if e[4] != "Postponed":
            return "-",n ,e
    return None

def test_analisis_corners_mitad(datos, encuentros):
        print("    Analisis Linea +4.5 corners HT:")
        for e in sorted(list(analisis_corners_mitad(datos, encuentros, n=4.5, f=freq, p=0.9,supera_n=True)), key=lambda x: x[-1]):
            print(e)
        print("    Analisis Linea -4.5 corners HT:")
        for e in sorted(list(analisis_corners_mitad(datos, encuentros, n=4.5, f=freq, p=0.9,supera_n=False)), key=lambda x: x[-1]):
            print(e)
            
def test_analisis_corners_total(datos, encuentros):
        print("    Analisis Linea +9.5 corners FT:")
        for e in sorted(list(analisis_corners_total(datos, encuentros, n=9.5, f=freq, p=0.9,supera_n=True)), key=lambda x: x[-1]):
            print(e)
        print("    Analisis Linea -9.5 corners FT:")
        for e in sorted(list(analisis_corners_total(datos, encuentros, n=9.5, f=freq, p=0.9,supera_n=False)), key=lambda x: x[-1]):
            print(e)
def test_analisis_goles_mitad(datos, encuentros):
        print("Analisis >=3 goles")
        for e in analisis_goles(datos, encuentros, n=3, f=f, p=0.5):
            print(e)
        
        print("Analisis >=2 goles")
        for e in analisis_goles(datos, encuentros, n=2, f=f, p=0.7):
            print(e)
        
        print("Analisis >=1 gol")
        for e in analisis_goles(datos, encuentros, n=1, f=f, p=0.90):
            print(e)

def test_analisis_goles_mitad_csv(datos, encuentros, output_file):
    print("    Analisis Linea +1.0 goles HT:")
    with open(output_file, 'w', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Probabilidad", "Cuota", "Local", "Visitante", "Fecha"])

        # Obtener los resultados de la función analisis_goles
        resultados = list(analisis_goles_mitad(datos, encuentros, n=1, f=freq, p=0.90,supera_n=True))

        # Ordenar por fecha (el último elemento de cada tupla)
        resultados_ordenados = sorted(resultados, key=lambda x: x[-1])

        for e in resultados_ordenados:
            if (("U19" not in e[3] and "U19" not in e[4]) and ("U18" not in e[3] and "U18" not in e[4])):
                print(e)
                csv_writer.writerow(e)
            
    print("    Analisis Linea -1.0 goles HT:")
    for e in sorted(list(analisis_goles_mitad(datos, encuentros, n=1, f=freq, p=0.9,supera_n=False)), key=lambda x: x[-1]):
        if e[1]!=0.0:
            print(e)


def test_analisis_goles_total(datos, encuentros):
    print("    Analisis Linea +2.5 goles FT:")
    for e in sorted(list(analisis_goles_total(datos, encuentros, n=2.5, f=freq, p=0.9,supera_n=True)), key=lambda x: x[-1]):
        if (("U19" not in e[3] and "U19" not in e[4]) and ("U18" not in e[3] and "U18" not in e[4])):
            print(e)
    print("    Analisis Linea -2.5 goles FT:")
    for e in sorted(list(analisis_goles_total(datos, encuentros, n=2.5, f=freq, p=0.9,supera_n=False)), key=lambda x: x[-1]):
        if (("U19" not in e[3] and "U19" not in e[4]) and ("U18" not in e[3] and "U18" not in e[4])):
            print(e)

def salida_por_consola():
    data = []
    for d in test_analisis_corners_total(datos, encuentros):
        if d is not None:
            e = d.split(", ")[-1]
            e = datetime.datetime.strptime(e, '%Y-%m-%d %H:%M')
            d.append(e)
            data.append(d)
    # sorted_data = sorted(data, key=lambda d: datetime.datetime.strptime(d.split(", ")[-1], '%Y-%m-%d %H:%M'))
    for e in data:
        print(e)

if __name__ == '__main__':
    fecha_global = "23-06-2024"

    # datos = lee_datos_partidos("../data/DatosPartidos(14-03-2023).csv")
    datos = lee_datos_partidos_selenium(f"../data/DatosPartidos({fecha_global}).csv")
    encuentros = lee_encuentros_selenium(f"../data/Encuentros({fecha_global}).csv")
    # test_analisis_goles_mitad_csv(datos, encuentros, f'../data/TestLista({fecha_global}).csv')
    test_analisis_goles_total(datos, encuentros)
    test_analisis_corners_mitad(datos, encuentros)
    test_analisis_corners_total(datos, encuentros)