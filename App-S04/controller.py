﻿"""
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
csv.field_size_limit(2147483647)
import tracemalloc
import sys

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {'model':None,
               'loaded':False}
    control['model'] = model.new_data_structs()
    return control


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Funciones para carga de datos
# =============================================================================================================================================================================
# =============================================================================================================================================================================

def load_data(control, memflag):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    data_structs = control['model']
    start_time = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
    
    count = {'limits':{'latmax':0,
                       'latmin':float('inf'),
                       'longmax':float('-inf'),
                       'longmin':0}}
    
    loadModelData(data_structs, count)
    
    control['loaded'] = True
    
    stop_time = get_time()
    time = delta_time(start_time, stop_time)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        memory = delta_memory(stop_memory, start_memory)
        return count, time, memory
    else:
        return count, time, None

def loadModelData(data_structs, count):
    # invocar funciones de carga individuales
    loadStations(data_structs, count)
    loadVertexData(data_structs, count)
    loadTickets(data_structs, count)
    loadEdgeData(data_structs, count)


# =============================================================================================================================================================================
# vertices

def loadVertexData(data_structs, count):
    vertex_file = cf.data_dir + 'tickets/bogota_vertices.txt'
    with open(vertex_file, 'r', encoding='utf-8') as vertex_txt:
        data = vertex_txt.readline().strip('\n')
        while len(data) > 0:
            model.addData(data_structs, data, 'vertex', count)
            data = vertex_txt.readline().strip('\n')


# =============================================================================================================================================================================
# estaciones

def loadStations(data_structs, count):
    stations_file = cf.data_dir + 'tickets/estacionpolicia_bogota_vertices.csv'
    input_file = csv.DictReader(open(stations_file, encoding='utf-8'))
    for station in input_file:
        model.addData(data_structs, station, 'station', count)


# =============================================================================================================================================================================
# comparendos

def loadTickets(data_structs, count):
    tickets_file = cf.data_dir + 'tickets/comparendos_2019_bogota_vertices.csv'
    input_file = csv.DictReader(open(tickets_file, encoding='utf-8'))
    for ticket in input_file:
        model.addData(data_structs, ticket, 'ticket', count)


# =============================================================================================================================================================================
# arcos

def loadEdgeData(data_structs, count):
    edges_file = cf.data_dir + 'tickets/bogota_arcos.txt'
    with open(edges_file, 'r', encoding='utf-8') as edges_txt:
        edges_txt.readline()
        edges_txt.readline()
        data = edges_txt.readline().strip('\n').split(" ")
        while len(data) > 0 and data[0] != '':
            if len(data) != 1:
                model.addData(data_structs, data, 'edge', count)
            data = edges_txt.readline().strip('\n').split(" ")


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# crear listas para la vista
# =============================================================================================================================================================================
# =============================================================================================================================================================================


def createTopNList(lst, n):
    if model.getListSize(lst) <= 2*n:
        top_n_list = lst
    else:
        top_n_list = model.createTopNSublist(lst, n)
    return top_n_list


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Funciones de consulta
# =============================================================================================================================================================================
# =============================================================================================================================================================================


def getListSize(lst):
    return model.getListSize(lst)

def getEdges(control):
    data_structs = control['model']
    edges = model.getEdges(data_structs)
    return edges

def getDataLists(control):
    """
    Retorna un dato por su ID.
    """
    # Llamar la función del modelo para obtener un dato
    data_structs = control['model']
    return model.getDataLists(data_structs)


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Requerimientos
# =============================================================================================================================================================================
# =============================================================================================================================================================================


# =============================================================================================================================================================================
# req1

def req1(control, lati, longi, latf, longf, memflag):
    """
    Retorna el resultado del requerimiento 1
    """
    # Modificar el requerimiento 1
    data_structs = control['model'] 
    vi = {'lat':lati, 'long':longi}
    vf = {'lat':latf, 'long':longf}
    if memflag:
        mi = get_memory()

    ti = get_time()
    
    count = {'distance':0}
    path_stack = model.req1(data_structs, vi, vf, count)
    
    tf = get_time()
    time = delta_time(ti, tf)
    
    if memflag:
        mf = get_memory()
        memory = delta_memory(mf, mi)
    else:
        memory = None
        
    return path_stack, count, time, memory


# =============================================================================================================================================================================
# req2

def req2(control, lati, longi, latf, longf, memflag):
    """
    Retorna el resultado del requerimiento 2
    """
    # Modificar el requerimiento 2
    data_structs = control['model'] 
    vi = {'lat':lati, 'long':longi}
    vf = {'lat':latf, 'long':longf}
    if memflag:
        mi = get_memory()

    ti = get_time()
    
    count = {'distance':0,
             'cost':0,
             'included_vertices':None,
             'total_vertices':0}
    path_stack = model.req2(data_structs, vi, vf, count)
    
    tf = get_time()
    time = delta_time(ti, tf)
    
    if memflag:
        mf = get_memory()
        memory = delta_memory(mf, mi)
    else:
        memory = None
        
    return path_stack, count, time, memory


# =============================================================================================================================================================================
# req3

def req3(control, cameras, localidad, cost, memflag):
    """
    Retorna el resultado del requerimiento 3
    """
    # Modificar el requerimiento 3
    data_structs = control['model'] 

    if memflag:
        mi = get_memory()
    ti = get_time()
    
    count = {'distance':0,
             'cost':0,
             'included_vertices':None,
             'total_vertices':[]}
    paths, vertex_path_list, first_vertex_index = model.req3(data_structs, cameras, localidad, cost, count)
    
    tf = get_time()
    time = delta_time(ti, tf)
    
    if memflag:
        mf = get_memory()
        memory = delta_memory(mf, mi)
    else:
        memory = None
        
    return paths, vertex_path_list, first_vertex_index, count, time, memory


# =============================================================================================================================================================================
# req4

def req_4(control, cameras, localidad, cost, whole, memflag):
    """
    Retorna el resultado del requerimiento 4
    """
    # Modificar el requerimiento 4
    data_structs = control['model'] 

    if memflag:
        mi = get_memory()
    ti = get_time()
    
    count = {'distance':0,
             'cost':0,
             'included_vertices':None,
             'total_vertices':[]}
    paths, vertex_path_list, first_vertex_index = model.req_4(data_structs, cameras, cost, whole, count)
    
    tf = get_time()
    time = delta_time(ti, tf)
    
    if memflag:
        mf = get_memory()
        memory = delta_memory(mf, mi)
    else:
        memory = None
        
    return paths, vertex_path_list, first_vertex_index, count, time, memory


# =============================================================================================================================================================================
# req5

def req5(control, cameras, vehicle, cost, memflag):
    """
    Retorna el resultado del requerimiento 5
    """
    # Modificar el requerimiento 5
    data_structs = control['model'] 

    if memflag:
        mi = get_memory()
    ti = get_time()
    
    count = {'distance':0,
             'cost':0,
             'included_vertices':None,
             'total_vertices':[]}
    paths, vertex_path_list, first_vertex_index = model.req5(data_structs, cameras, vehicle, cost, count)
    
    tf = get_time()
    time = delta_time(ti, tf)
    
    if memflag:
        mf = get_memory()
        memory = delta_memory(mf, mi)
    else:
        memory = None
        
    return paths, vertex_path_list, first_vertex_index, count, time, memory


# =============================================================================================================================================================================
# req6

def req6(control, tickets, memflag):
    """
    Retorna el resultado del requerimiento 6
    """
    # Modificar el requerimiento 6
    data_structs = control['model']
    
    if memflag:
        mi = get_memory()
    ti = get_time()
    
    count = {'included_vertices':None,
             'total_vertices':[]}
    paths, ticket_q = model.req6(data_structs, tickets, count)
    
    tf = get_time()
    time = delta_time(ti, tf)
    
    if memflag:
        mf = get_memory()
        memory = delta_memory(mf, mi)
    else:
        memory = None
        
    return paths,ticket_q, count, time, memory


# =============================================================================================================================================================================
# req7

def req7(control, lati, longi, latf, longf, memflag):
    """
    Retorna el resultado del requerimiento 7
    """
    # Modificar el requerimiento 7
    data_structs = control['model'] 
    vi = {'lat':lati, 'long':longi}
    vf = {'lat':latf, 'long':longf}
    if memflag:
        mi = get_memory()

    ti = get_time()
    
    count = {'distance':0,
             'tickets':0}
    path_stack = model.req7(data_structs, vi, vf, count)
    
    tf = get_time()
    time = delta_time(ti, tf)
    
    if memflag:
        mf = get_memory()
        memory = delta_memory(mf, mi)
    else:
        memory = None
        
    return path_stack, count, time, memory


# =============================================================================================================================================================================
# req8

def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # Modificar el requerimiento 8
    pass


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Tiempos de ejecucion
# =============================================================================================================================================================================
# =============================================================================================================================================================================

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
    tracemalloc.start()
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