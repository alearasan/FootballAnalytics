'''
Created on 17 nov 2022

@author: aleja
'''
from funciones.Lectura import *

fecha_empieza_contar = "2023-08-01"


def probabilidad_corner_10min(datos_minutos, local, visitante, f):
    fecha_inicio = parsea_fecha(fecha_empieza_contar)
    
    filtro_local = [e for e in datos_minutos if e.local == local and e.fecha > fecha_inicio]
    filtro_visitante = [e for e in datos_minutos if e.visitante == visitante and e.fecha > fecha_inicio]
    
    if len(filtro_local) < f or len(filtro_visitante) < f:
        return 0
    
    local_supera_n = [e for e in filtro_local if any(numero <= 10 for numero in e.home_elementos + e.away_elementos)]
    visitante_supera_n = [e for e in filtro_visitante if any(numero <= 10 for numero in e.home_elementos + e.away_elementos)]
    
    total_local_visitante = len(filtro_local) + len(filtro_visitante)
    
    return round((len(local_supera_n) + len(visitante_supera_n)) / total_local_visitante, 2) if total_local_visitante > 0 else 0


def analisis_minutos_corners (datos_minutos,encuentros,f,p):
    l = [(probabilidad_corner_10min(datos_minutos, e.local, e.visitante, f),
          e.local,
          e.visitante,
          e.tiempo)
          for e in encuentros if probabilidad_corner_10min(datos_minutos, e.local, e.visitante, f) > p]
    
    return sorted(l, key= lambda x : x[0],reverse = False)


def media_corners_mitad (datos, local, visitante):
    filtro_local = [e.cfm + e.ccm for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e.cfm + e.ccm for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    return round(sum(filtro_local+filtro_visitante) / len(filtro_local+filtro_visitante),2)

 
def probabilidad_corners_mitad(datos, local, visitante, n, f,supera_n=True):
    filtro_local = [e for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]

    if len(filtro_local) >= f and len(filtro_visitante) >= f:
        if supera_n:
            local_condicion = lambda e: e.cfm + e.ccm >= n
            visitante_condicion = lambda e: e.cfm + e.ccm >= n
        else:
            local_condicion = lambda e: e.cfm + e.ccm <= n and e.cfm + e.ccm != 0
            visitante_condicion = lambda e: e.cfm + e.ccm <= n and e.cfm + e.ccm != 0

        local_supera_n = [e.cfm + e.ccm for e in filtro_local if local_condicion(e)]
        visitante_supera_n = [e.cfm + e.ccm for e in filtro_visitante if visitante_condicion(e)]

        total_supera_n = local_supera_n + visitante_supera_n

        if len(total_supera_n) == 0:
            res = 0
        else:
            res = len(total_supera_n) / len(filtro_local + filtro_visitante)
    else:
        res = 0

    return round(res, 2)


def analisis_corners_mitad(datos, encuentros, n, f, p, supera_n=True):
    l = [(probabilidad_corners_mitad(datos, e.local, e.visitante, n, f, supera_n=supera_n),
          media_corners_mitad(datos, e.local, e.visitante),
          e.local,
          e.visitante,
          e.tiempo)
         for e in encuentros if probabilidad_corners_mitad(datos, e.local, e.visitante, n, f, supera_n=supera_n) > p]

    return sorted(l, key=lambda x: x[4], reverse=False)


def media_corners_total (datos, local, visitante):
    filtro_local = [e.cft + e.cct for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e.cft + e.cct for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    return round(sum(filtro_local+filtro_visitante) / len(filtro_local+filtro_visitante),2)


def probabilidad_corners_total(datos, local, visitante, n, f, supera_n=True):
    filtro_local = [e for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]

    if len(filtro_local) >= f and len(filtro_visitante) >= f:
        if supera_n:
            local_condicion = lambda e: e.cft + e.cct >= n
            visitante_condicion = lambda e: e.cft + e.cct >= n
        else:
            local_condicion = lambda e: e.cft + e.cct <= n and e.cft + e.cct != 0
            visitante_condicion = lambda e: e.cft + e.cct <= n and e.cft + e.cct != 0

        local_supera_n = [e.cft + e.cct for e in filtro_local if local_condicion(e)]
        visitante_supera_n = [e.cft + e.cct for e in filtro_visitante if visitante_condicion(e)]

        total_supera_n = local_supera_n + visitante_supera_n

        if len(total_supera_n) == 0:
            res = 0
        else:
            res = len(total_supera_n) / len(filtro_local + filtro_visitante)
    else:
        res = 0

    return round(res, 2)


def analisis_corners_total(datos, encuentros, n, f, p, supera_n=True):
    l = [(probabilidad_corners_total(datos, e.local, e.visitante, n, f, supera_n=supera_n),
          media_corners_total(datos, e.local, e.visitante),
          e.local,
          e.visitante,
          e.tiempo)
         for e in encuentros if probabilidad_corners_total(datos, e.local, e.visitante, n, f, supera_n=supera_n) > p]

    return sorted(l, key=lambda x: x[4], reverse=False)

def media_goles_mitad (datos, local, visitante):
    filtro_local = [e.gfm + e.gcm for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e.gfm + e.gcm for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    return round(sum(filtro_local+filtro_visitante) / len(filtro_local+filtro_visitante),2)

    
def probabilidad_goles_mitad(datos, local, visitante, n, f,supera_n=True):
    filtro_local = list(set([e for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]))
    filtro_visitante = list(set([e for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]))

    if len(filtro_local) >= f and len(filtro_visitante) >= f:
        if supera_n:
            local_condicion = lambda e: e.gfm + e.gcm >= n
            visitante_condicion = lambda e: e.gfm + e.gcm >= n
        else:
            local_condicion = lambda e: e.gfm + e.gcm <= n
            visitante_condicion = lambda e: e.gfm + e.gcm <= n

        local_supera_n = [e.gfm + e.gcm for e in filtro_local if local_condicion(e)]
        visitante_supera_n = [e.gfm + e.gcm for e in filtro_visitante if visitante_condicion(e)]

        total_supera_n = local_supera_n + visitante_supera_n

        if len(total_supera_n) == 0:
            res = 0
        else:
            res = len(total_supera_n) / len(filtro_local + filtro_visitante)
    else:
        res = 0

    return round(res, 2)

def analisis_goles_mitad (datos,encuentros,n,f,p,supera_n=True):
    if supera_n:
        l = [(probabilidad_goles_mitad(datos, e.local, e.visitante, n, f, supera_n=supera_n),
          media_goles_mitad(datos, e.local, e.visitante),
          probabilidad_goles_mitad(datos, e.local, e.visitante, n+1, f, supera_n=supera_n),
          e.local,
          e.visitante,
          e.tiempo)
          for e in encuentros if probabilidad_goles_mitad(datos, e.local, e.visitante, n, f, supera_n=supera_n) > p]
    else:
        l = [(probabilidad_goles_mitad(datos, e.local, e.visitante, n, f, supera_n=supera_n),
          media_goles_mitad(datos, e.local, e.visitante),
          probabilidad_goles_mitad(datos, e.local, e.visitante, n-1, f, supera_n=supera_n),
          e.local,
          e.visitante,
          e.tiempo)
          for e in encuentros if probabilidad_goles_mitad(datos, e.local, e.visitante, n, f, supera_n=supera_n) > p]
    return sorted(l, key= lambda x : x[4],reverse = False)


def media_goles_encuentro_total (datos, local, visitante):
    filtro_local = [e.gft + e.gct for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e.gft + e.gct for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    return round(sum(filtro_local+filtro_visitante) / len(filtro_local+filtro_visitante),2)

def probabilidad_goles_total(datos, local, visitante, n, f,supera_n=True):
    filtro_local = [e for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]

    if len(filtro_local) >= f and len(filtro_visitante) >= f:
        if supera_n:
            local_condicion = lambda e: e.gft + e.gct >= n
            visitante_condicion = lambda e: e.gft + e.gct >= n
        else:
            local_condicion = lambda e: e.gft + e.gct <= n
            visitante_condicion = lambda e: e.gft + e.gct <= n

        local_supera_n = [e.gft + e.gct for e in filtro_local if local_condicion(e)]
        visitante_supera_n = [e.gft + e.gct for e in filtro_visitante if visitante_condicion(e)]

        total_supera_n = local_supera_n + visitante_supera_n

        if len(total_supera_n) == 0:
            res = 0
        else:
            res = len(total_supera_n) / len(filtro_local + filtro_visitante)
    else:
        res = 0

    return round(res, 2)

def analisis_goles_total (datos,encuentros,n,f,p,supera_n=True):
    l = [(probabilidad_goles_total(datos, e.local, e.visitante, n, f, supera_n=supera_n),
          media_goles_encuentro_total(datos, e.local, e.visitante),
          e.local,
          e.visitante,
          e.tiempo)
          for e in encuentros if probabilidad_goles_total(datos, e.local, e.visitante, n, f, supera_n=supera_n) > p]
    
    return sorted(l, key= lambda x : x[4],reverse = False)