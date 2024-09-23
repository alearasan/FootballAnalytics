'''
Created on 17 nov 2022

@author: aleja
'''
from collections import namedtuple
import csv
from datetime import *
from funciones.Parsers import *

DatosPartido = namedtuple("DatosPartido","copa,fecha,local,gft,gct,gfm,gcm,visitante\
                                    ,cft,cct,cfm,ccm,analisis")

DatosPartido_selenium = namedtuple("DatosPartido_selenium","fecha,local,gft,gct,gfm,gcm,visitante\
                                    ,cft,cct,cfm,ccm")

DatosPartidoMinuto = namedtuple("DatosPartidoMinuto", "fecha,local,visitante,home_elementos,away_elementos")

Encuentros = namedtuple("Encuentro","copa,local,tiempo,visitante,analisis")

Encuentros_selenium = namedtuple("Encuentros_selenium","local,tiempo,visitante,analisis")

def lee_datos_partidos_minutos (fichero):
    res = []
    with open (fichero, encoding = "utf-8") as f:
        lector = csv.reader(f, delimiter = ";")
        next(lector)
        for fecha,local,visitante,home_elementos,away_elementos in lector:
            fecha = parsea_fecha(fecha)
            home_elementos = parsea_minutos(home_elementos)
            away_elementos = parsea_minutos(away_elementos)
            res.append(DatosPartidoMinuto(fecha,local,visitante,home_elementos,away_elementos))
    return res

def lee_datos_partidos (fichero):
    res = []
    with open (fichero, encoding = "utf-8") as f:
        lector = csv.reader(f, delimiter = ";")
        next(lector)
        for copa,fecha,local,resultado,visitante,corners,analisis in lector:
            fecha = parsea_fecha(fecha)
            gft,gct,gfm,gcm = parsea_resultado(resultado)
            cft,cct,cfm,ccm = parsea_corners(corners)
            res.append(DatosPartido(copa,fecha,local,gft,gct,gfm,gcm,visitante
                                    ,cft,cct,cfm,ccm,analisis))
    return res

def lee_datos_partidos_selenium (fichero):
    res = []
    with open (fichero, encoding = "utf-8") as f:
        lector = csv.reader(f, delimiter = ";")
        next(lector)
        for fecha,local,resultado,visitante,corners in lector:
            fecha = parsea_fecha(fecha)
            gft,gct,gfm,gcm = parsea_resultado(resultado)
            cft,cct,cfm,ccm = parsea_corners(corners)
            res.append(DatosPartido_selenium(fecha,local,gft,gct,gfm,gcm,visitante
                                    ,cft,cct,cfm,ccm))
    return res

def lee_encuentros (fichero):
    res = []
    with open (fichero, encoding = "utf-8") as f:
        lector = csv.reader(f, delimiter = ";")
        next(lector)
        for copa,local,tiempo,visitante,analisis in lector:
            res.append(Encuentros(copa,local,tiempo,visitante,analisis))
    return res

def lee_encuentros_selenium (fichero):
    res = []
    with open (fichero, encoding = "utf-8") as f:
        lector = csv.reader(f, delimiter = ";")
        next(lector)
        for local,tiempo,visitante,analisis in lector:
            tiempo = parsea_fecha_hora_esp(tiempo)
            res.append(Encuentros_selenium(local,tiempo,visitante,analisis))
    return res