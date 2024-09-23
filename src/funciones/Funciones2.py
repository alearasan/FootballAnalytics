'''
Created on 17 nov 2022

@author: aleja
'''
from funciones.Lectura import *

fecha_empieza_contar = "2022-08-01"

def hay_numero_menor_que_10(lista):
    return any(numero <= 10 for numero in lista)

def probabilidad_corner_10min (datos_minutos, local, visitante, f):
    filtro_local = [e for e in datos_minutos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e for e in datos_minutos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    
    if len(filtro_local)>=f and len(filtro_visitante)>=f:
        local_supera_n = [e for e in filtro_local if hay_numero_menor_que_10(e.home_elementos) or  hay_numero_menor_que_10(e.away_elementos)]
        visitante_supera_n = [e for e in filtro_visitante if hay_numero_menor_que_10(e.home_elementos) or  hay_numero_menor_que_10(e.away_elementos)]
    
        if len(local_supera_n + visitante_supera_n) == 0:
            res = 0 
        else:
            res = len(local_supera_n + visitante_supera_n) / len(filtro_local + filtro_visitante)
            
    else: res = 0
    
    return round(res,2)

def analisis_minutos_corners (datos_minutos,encuentros,f,p):
    l = [(probabilidad_corner_10min(datos_minutos, e.local, e.visitante, f),
          e.local,
          e.visitante,
          e.tiempo)
          for e in encuentros if probabilidad_corner_10min(datos_minutos, e.local, e.visitante, f) > p]
    
    return sorted(l, key= lambda x : x[0],reverse = False)

def total_equipos (partidos):
    equipos = [e.local for e in partidos]
    equipos.append(e.visitantes for e in partidos)
    conj = set(equipos)
    lista = list(conj)
    return len(lista)

def media_corners_favor_total (partidos):
    lista_corners = [e.cft for e in partidos]
    media = sum(lista_corners)/len(lista_corners)
    return media

def media_corners_contra_total (partidos):
    lista_corners = [e.cct for e in partidos]
    media = sum(lista_corners)/len(lista_corners)
    return media

def media_corners_favor_mitad (partidos):
    lista_corners = [e.cfm for e in partidos]
    media = sum(lista_corners)/len(lista_corners)
    return media

def media_corners_contra_mitad (partidos):
    lista_corners = [e.ccm for e in partidos]
    media = sum(lista_corners)/len(lista_corners)
    return media

def equipo_media_corners (partidos, equipo, local, mitad):
    dicc = {}
    if local == "True":
        filtro = [e for e in partidos if e.local == equipo]
        for e in filtro:
            clave = e.local
            if clave in dicc:
                dicc[clave].append(e)
            else:
                dicc[clave] = [e]
                
    elif local == "False": 
        filtro = [e for e in partidos if e.visitante == equipo]
        for e in filtro:
            clave = e.visitante
            if clave in dicc:
                dicc[clave].append(e)
            else:
                dicc[clave] = [e]
                
    if mitad == "True":
        for campo, lista in dicc.items():
            dicc[campo] = media_corners_favor_mitad(lista) + media_corners_contra_mitad(lista)
    elif mitad == "False":
        for campo, lista in dicc.items():
            dicc[campo] = media_corners_favor_total(lista) + media_corners_contra_total(lista)
    
    return dicc

def probabilidad_corners_supera_n (partidos, equipo, local, mitad, n):
    dicc = {}
    if local == "True":
        filtro = [e for e in partidos if e.local == equipo]
        for e in filtro:
            clave = e.local
            if clave in dicc:
                dicc[clave].append(e)
            else:
                dicc[clave] = [e]
                
    elif local == "False": 
        filtro = [e for e in partidos if e.visitante == equipo]
        for e in filtro:
            clave = e.visitante
            if clave in dicc:
                dicc[clave].append(e)
            else:
                dicc[clave] = [e]

    if mitad == "True":
        for campo, lista in dicc.items():
            dicc[campo] = len([e.cfm + e.ccm for e in lista if e.cfm + e.ccm >= n]) * 100 / len(lista)
    elif mitad == "False":
        for campo, lista in dicc.items():
            dicc[campo] = len([e.cft + e.cct for e in lista if e.cfm + e.ccm >= n]) * 100 / len(lista)
            
    return dicc

def media_corners_encuentro (datos, local, visitante):
    filtro_local = [e.cfm + e.ccm for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e.cfm + e.ccm for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    return round(sum(filtro_local+filtro_visitante) / len(filtro_local+filtro_visitante),2)

def probabilidad_corners_supera_n_encuentro (datos, local, visitante, n, f):
    filtro_local = [e for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    
    if len(filtro_local)>=f and len(filtro_visitante)>=f:
        local_supera_n = [e.cfm + e.ccm for e in filtro_local if e.cfm + e.ccm >= n]
        visitante_supera_n = [e.cfm + e.ccm for e in filtro_visitante if e.cfm + e.ccm >= n]
    
        if len(local_supera_n + visitante_supera_n) == 0:
            res = 0
        else:
            res = len(local_supera_n + visitante_supera_n) / len(filtro_local + filtro_visitante)
            
    else: res = 0
    
    return round(res,2)

def analisis (datos,encuentros,n,f,p):
    l = [(probabilidad_corners_supera_n_encuentro(datos, e.local, e.visitante, n, f),
          media_corners_encuentro(datos, e.local, e.visitante),
          e.local,
          e.visitante,
          e.tiempo)
          for e in encuentros if probabilidad_corners_supera_n_encuentro(datos, e.local, e.visitante, n, f) > p]
    
    return sorted(l, key= lambda x : x[4],reverse = False)

def probabilidad_corners_no_supera_n_encuentro (datos, local, visitante, n, f):
    filtro_local = [e for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    
    if len(filtro_local)>=f and len(filtro_visitante)>=f:
        local_supera_n = [e.cfm + e.ccm for e in filtro_local if e.cfm + e.ccm <= n]
        visitante_supera_n = [e.cfm + e.ccm for e in filtro_visitante if e.cfm + e.ccm <= n]
    
        if len(local_supera_n + visitante_supera_n) == 0:
            res = 0
        else:
            res = len(local_supera_n + visitante_supera_n) / len(filtro_local + filtro_visitante)
            
    else: res = 0
    
    return round(res,2)

def analisis_corners_mitad_no_supera (datos,encuentros,n,f,p):
    l = [(probabilidad_corners_no_supera_n_encuentro(datos, e.local, e.visitante, n, f),
          media_corners_encuentro(datos, e.local, e.visitante),
          e.local,
          e.visitante,
          e.tiempo)
          for e in encuentros if probabilidad_corners_no_supera_n_encuentro(datos, e.local, e.visitante, n, f) > p]
    
    return sorted(l, key= lambda x : x[4],reverse = False)

def media_goles_encuentro (datos, local, visitante):
    filtro_local = [e.gfm + e.gcm for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e.gfm + e.gcm for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    return round(sum(filtro_local+filtro_visitante) / len(filtro_local+filtro_visitante),2)

def probabilidad_goles_supera_n_encuentro (datos, local, visitante, n, f):
    filtro_local = [e for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    
    if len(filtro_local)>=f and len(filtro_visitante)>=f:
        local_supera_n = [e.gfm + e.gcm for e in filtro_local if e.gfm + e.gcm >= n]
        visitante_supera_n = [e.gfm + e.gcm for e in filtro_visitante if e.gfm + e.gcm >= n]
    
        if len(local_supera_n + visitante_supera_n) == 0:
            res = 0
        else:
            res = len(local_supera_n + visitante_supera_n) / len(filtro_local + filtro_visitante)
            
    else: res = 0
    
    return round(res,2)

def analisis_goles (datos,encuentros,n,f,p):
    l = [(probabilidad_goles_supera_n_encuentro(datos, e.local, e.visitante, n, f),
          media_goles_encuentro(datos, e.local, e.visitante),
          e.local,
          e.visitante,
          e.tiempo)
          for e in encuentros if probabilidad_goles_supera_n_encuentro(datos, e.local, e.visitante, n, f) > p]
    
    return sorted(l, key= lambda x : x[4],reverse = False)

def media_corners_encuentro_total (datos, local, visitante):
    filtro_local = [e.cft + e.cct for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e.cft + e.cct for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    return round(sum(filtro_local+filtro_visitante) / len(filtro_local+filtro_visitante),2)

def probabilidad_corners_supera_n_encuentro_total (datos, local, visitante, n, f):
    filtro_local = [e for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    
    if len(filtro_local)>=f and len(filtro_visitante)>=f:
        local_supera_n = [e.cft + e.cct for e in filtro_local if e.cft + e.cct >= n]
        visitante_supera_n = [e.cft + e.cct for e in filtro_visitante if e.cft + e.cct >= n]
    
        if len(local_supera_n + visitante_supera_n) == 0:
            res = 0
        else:
            res = len(local_supera_n + visitante_supera_n) / len(filtro_local + filtro_visitante)
            
    else: res = 0
    
    return round(res,2)

def analisis_corners_total (datos,encuentros,n,f,p):
    l = [(probabilidad_corners_supera_n_encuentro_total(datos, e.local, e.visitante, n, f),
          media_corners_encuentro_total(datos, e.local, e.visitante),
          e.local,
          e.visitante,
          e.tiempo)
          for e in encuentros if probabilidad_corners_supera_n_encuentro_total(datos, e.local, e.visitante, n, f) > p]
    
    return sorted(l, key= lambda x : x[4],reverse = False)

def probabilidad_corners_no_supera_n_encuentro_total (datos, local, visitante, n, f):
    filtro_local = [e for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    
    if len(filtro_local)>=f and len(filtro_visitante)>=f:
        local_supera_n = [e.cft + e.cct for e in filtro_local if e.cft + e.cct <= n]
        visitante_supera_n = [e.cft + e.cct for e in filtro_visitante if e.cft + e.cct <= n]
    
        if len(local_supera_n + visitante_supera_n) == 0:
            res = 0
        else:
            res = len(local_supera_n + visitante_supera_n) / len(filtro_local + filtro_visitante)
            
    else: res = 0
    
    return round(res,2)

def analisis_corners_no_supera_total (datos,encuentros,n,f,p):
    l = [(probabilidad_corners_no_supera_n_encuentro_total(datos, e.local, e.visitante, n, f),
          media_corners_encuentro_total(datos, e.local, e.visitante),
          e.local,
          e.visitante,
          e.tiempo)
          for e in encuentros if probabilidad_corners_no_supera_n_encuentro_total(datos, e.local, e.visitante, n, f) > p]
    
    return sorted(l, key= lambda x : x[4],reverse = False)

def media_goles_encuentro_total (datos, local, visitante):
    filtro_local = [e.gft + e.gct for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e.gft + e.gct for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    return round(sum(filtro_local+filtro_visitante) / len(filtro_local+filtro_visitante),2)

def probabilidad_goles_supera_n_encuentro_total (datos, local, visitante, n, f):
    filtro_local = [e for e in datos if e.local == local and e.fecha > parsea_fecha(fecha_empieza_contar)]
    filtro_visitante = [e for e in datos if e.visitante == visitante and e.fecha > parsea_fecha(fecha_empieza_contar)]
    
    if len(filtro_local)>=f and len(filtro_visitante)>=f:
        local_supera_n = [e.gft + e.gct for e in filtro_local if e.gft + e.gct >= n]
        visitante_supera_n = [e.gft + e.gct for e in filtro_visitante if e.gft + e.gct >= n]
    
        if len(local_supera_n + visitante_supera_n) == 0:
            res = 0
        else:
            res = len(local_supera_n + visitante_supera_n) / len(filtro_local + filtro_visitante)
            
    else: res = 0
    
    return round(res,2)

def analisis_goles_total (datos,encuentros,n,f,p):
    l = [(probabilidad_goles_supera_n_encuentro_total(datos, e.local, e.visitante, n, f),
          media_goles_encuentro_total(datos, e.local, e.visitante),
          e.local,
          e.visitante,
          e.tiempo)
          for e in encuentros if probabilidad_goles_supera_n_encuentro_total(datos, e.local, e.visitante, n, f) > p]
    
    return sorted(l, key= lambda x : x[4],reverse = False)