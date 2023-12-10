"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import time
import csv
import json
import tracemalloc
import os
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }
    control['model'] = model.newCatalog()
    return control


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    maxlong = None
    minlong = None
    maxlat= None
    minlat= None
    
    catalog = control['model']
    verticesfile = cf.data_dir + "tickets/bogota_vertices.txt"
    arcosfile = cf.data_dir + "tickets/bogota_arcos.txt"
    comparendos_vertices = cf.data_dir + "tickets/comparendos_2019_bogota_vertices.csv"
    estaciones_vertices = cf.data_dir + "tickets/estacionpolicia_bogota_vertices.csv"
    
    
    
    #Añade la informacion de las estaciones mas cercanas a los vertices de la malla vial     
    print("Añadiendo las estaciones...") 
    input_file_estaciones = csv.DictReader(open(estaciones_vertices, encoding="utf-8"), delimiter=",")
    for vertice_comparendo in input_file_estaciones:
        model.add_estacion(catalog, vertice_comparendo)
        
    #Crea los vertices para los dos grafos.
    print("Cargando los vertices para los grafos...") 
    with open(verticesfile, 'r') as archivovertice:
        for linea in archivovertice:
            fila = linea.strip().split(',')
            longitud = float(fila[1])
            latitud = float(fila[2])
            if maxlong == None:
                maxlong = longitud
                minlong = longitud
                maxlat  =  latitud
                minlat  =  latitud
            maxlong,minlong,maxlat,minlat = max_min(maxlong,minlong,maxlat,minlat,longitud,latitud)
            model.add_vertice_array(catalog, fila, fila[1], fila[2])
            model.add_vertice_malla(catalog,fila)
            model.add_vertice_comparendos(catalog,fila) 
            
    
    
    #Añade la informacion de los comparendos mas cercanos a los vertices de la malla vial

    input_file_comparendos = csv.DictReader(open(comparendos_vertices, encoding="utf-8"), delimiter=",")
    for vertice_comparendo in input_file_comparendos:
        model.add_comparendo(catalog, vertice_comparendo)  
        model.add_grafo_comparendo(catalog, vertice_comparendo)    
        
    
    comparendos_ordenados = model.sort_comparendos(catalog["comparendos"])

    
    #Añade la informacion de las estaciones mas cercanas a los vertices de la malla vial     
    print("Añadiendo las estaciones...") 
    input_file_estaciones = csv.DictReader(open(estaciones_vertices, encoding="utf-8"), delimiter=",")
    for vertice_comparendo in input_file_estaciones:
        model.add_grafo_estacion(catalog, vertice_comparendo)  
    
        #progress_bar(i, total_estaciones)
        
    
    #Carga los arcos para los grafos
    print("Añadiendo los arcos...") 
    with open(arcosfile, 'r') as archivoarco:
        for linea in archivoarco:
            linea = linea.strip().split(" ")
            arco  = {"ID": int(linea[0]), "Vertices Adyacentes": linea[:] }
            model.add_arco_array(catalog, arco)
            model.add_arco(catalog, linea)
    
    
    return catalog["comparendos"], catalog["estaciones_policias"], catalog["vertices"], catalog["arcos"], maxlong,minlong,maxlat,minlat, comparendos_ordenados
    


    


def req_1(control, vertices, latitud1, longitud1, latitud2, longitud2):
    """
    Retorna el resultado del requerimiento 1
    """
    itime=get_time()
    camino_total,distancia_total,total_vertx = model.req_1(control['model'], vertices, latitud1, longitud1, latitud2, longitud2)
    ftine=get_time()
    dtine=round(delta_time(itime, ftine),2)
    print(f"\nEl tiempo que se demora algoritmo en encontrar la solución : {dtine} ms")
    return camino_total,distancia_total,total_vertx
def req_2(control, vertices, latitud1, longitud1, latitud2, longitud2):
    """
    Retorna el resultado del requerimiento 2
    """
    itime=get_time()
    camino_total,distancia_total,total_vertx = model.req_2(control['model'], vertices, latitud1, longitud1, latitud2, longitud2)
    ftine=get_time()
    dtine=round(delta_time(itime, ftine),2)
    print(f"\nEl tiempo que se demora algoritmo en encontrar la solución : {dtine} ms")
    return camino_total,distancia_total,total_vertx

def req_3(control,vertices, cantidadCamaras,localidad):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    return model.req_3(control["model"],vertices,cantidadCamaras,localidad)


def req_4(control, comparendos_ordenados, camaras, bono):
    """
    Retorna el resultado del requerimiento 4
    """
    itime=get_time()
    vertices, arcos, weight =  model.req_4(control["model"], comparendos_ordenados, camaras, bono)
    ftine=get_time()
    dtine=round(delta_time(itime, ftine),2)
    print(f"\nEl tiempo que se demora algoritmo en encontrar la solución : {dtine} ms\n")
    return vertices, arcos, weight

def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control, numero_comparendos, comparendos_ordenados, bono):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    itime=get_time()
    camino_total = model.req_6(control["model"], numero_comparendos, comparendos_ordenados, bono)
    ftine=get_time()
    dtine=round(delta_time(itime, ftine),2)
    print(f"\nEl tiempo que se demora algoritmo en encontrar la solución : {dtine} ms\n")
    return camino_total
    


def req_7(control, vertices,  lat1, long1, lat2, long2, bono):
    """
    Retorna el resultado del requerimiento 7
    """
    return model.req_7(control["model"], vertices,  lat1, long1, lat2, long2, bono)


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

        
def max_min(maxlong,minlong,maxlat,minlat,long,lat):
    
    if long > maxlong:
        maxlong = long
    if long < minlong:
        minlong = long
    if lat > maxlat:
        maxlat = lat
    if lat < minlat:
        minlat = lat
    return maxlong,minlong,maxlat,minlat