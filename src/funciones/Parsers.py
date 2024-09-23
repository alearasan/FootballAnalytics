'''
Created on 17 nov 2022

@author: aleja
'''
from datetime import *
def parsea_fecha (str):
    return datetime.strptime(str,"%Y-%m-%d").date()

def parsea_fecha_hora_esp(str):
    if str == "Postponed":
        return "Postponed"
    else:
        fecha_hora = datetime.strptime(str, '%Y-%m-%d %H:%M')
        nueva_fecha_hora = fecha_hora + timedelta(hours=2)
        nuevo_archivo = nueva_fecha_hora.strftime('%Y-%m-%d %H:%M')
    return nuevo_archivo
def parsea_resultado (str):
    #1-0(0-0)
    no_spaces = str.strip()
    separacion = no_spaces.split("(")
    total = separacion[0].strip()
    mitad = separacion[1].strip(")")
    gft = int(total.split("-")[0])
    gct = int(total.split("-")[1])
    gfm = int(mitad.split("-")[0])
    gcm = int(mitad.split("-")[1])
    return gft,gct,gfm,gcm

def parsea_corners(cadena):
    # Ejemplo de cadena: "1-8 (1-5)" o "1-7"
    separacion = cadena.strip().split("(")
    # Si hay dos partes (total y mitad)
    if len(separacion) == 2:
        total_corners = separacion[0].strip()
        mitad_corners = separacion[1].strip(")")
    # Si solo hay una parte (solo total)
    elif len(separacion) == 1:
        total_corners = separacion[0].strip()
        mitad_corners = "0-0"
    else:
        raise ValueError("Formato de cadena no compatible")

    cft, cct = map(int, total_corners.split("-"))
    cfm, ccm = map(int, mitad_corners.split("-"))

    return cft, cct, cfm, ccm

def parsea_minutos (cadena):
    if not cadena or len(cadena) == 0:
        return []
    elementos = cadena[1:-1].split(',')
    resultado = []
    for elemento in elementos:
        sinEspacios = elemento.strip()[1:-1]
        if len(sinEspacios) > 0:
            numero = sinEspacios.split("+")[0]
            resultado.append(int(numero))
    return resultado