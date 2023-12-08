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
import json
import config as cf
import model
import time
import csv
import tracemalloc
from DISClib.ADT import graph as gr
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
from datetime import datetime, timedelta
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {
        "model": None
    }
    control["model"] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    filename_vertices = "tickets/bogota_vertices.txt"
    file=cf.data_dir+filename_vertices
    long_max = -100
    long_min = 100
    lat_max =  -100
    lat_min = 100
    with open(file, 'r') as archivo:
        for vertice in archivo:
            model.add_vertex(control['model'], vertice)
            lista = vertice.split(',')
            long = float(lista[1])
            lat = float(lista[2])
            if long > long_max:
                long_max = long
            if long < long_min:
                long_min = long
            if lat > lat_max:
                lat_max = lat
            if lat < lat_min:
                lat_min = lat
    i = 0 
    filename_vertices = "tickets/comparendos_2019_bogota_vertices.csv"
    filecomparendos=cf.data_dir+filename_vertices
    input_file = csv.DictReader(open(filecomparendos, encoding='utf-8'))

    for comparendo in input_file:
        date_registro = comparendo["FECHA_HORA"]
        date_registro = datetime.strptime(date_registro, '%Y-%m-%d %H:%M:%S%z')
        comparendo["FECHA_HORA"] = date_registro
        model.add_comparendo(control['model'], comparendo)
        model.add_MapClases(control['model'], comparendo, comparendo["CLASE_VEHICULO"])
        model.add_gravedad(control['model'],comparendo)
        
    filename_vertices = "tickets/estacionpolicia_bogota_vertices.csv"
    file_estaciones=cf.data_dir+filename_vertices
    input_file = csv.DictReader(open(file_estaciones, encoding='utf-8'))
    for estacion in input_file:
        i += 1
        model.add_estacion(control['model'], estacion)

    filename_vertices = "tickets/bogota_arcos.txt"
    file=cf.data_dir+filename_vertices
    key = 0
    with open(file, 'r') as archivo:
        for lista_adj in archivo:
            key += 1
            if key > 2:
                model.add_arco(control['model'], lista_adj)

    #model.sort(control['model'])
     
    return lat_max, lat_min, long_max, long_min

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, lat1, long1, lat2, long2) :
    """
    Retorna el resultado del requerimiento 1
    """
    return model.req_1(control['model'], lat1, long1, lat2, long2)


def req_2(control, lat_inicio, long_inicio, lat_destino, long_destino):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    return model.req_2(control["model"], lat_inicio, long_inicio, lat_destino, long_destino)


def req_3(control, M, localidad):
    """
    Retorna el resultado del requerimiento 3
    """
    respuesta = model.req_3(control['model'], M, localidad)
    print('Los vertices donde se deben poner las camaras son: ')
    for vertice in lt.iterator(respuesta[0]):
        print(vertice['id'])
    for arco in lt.iterator(respuesta[1]):
        print(arco)


def req_4(control,M):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    return model.req_4(control["model"],M)


def req_5(control, m, clase):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    return model.req_5(control['model'], m, clase)

def req_6(control, m):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    return model.req_6(control['model'], m)


def req_7(control,lat_inicio, long_inicio, lat_destino, long_destino):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    return model.req_7(control["model"],lat_inicio, long_inicio, lat_destino, long_destino)


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
