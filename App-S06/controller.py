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
csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = model.new_data_structs()
    return control



# Funciones para la carga de datos

def load_data(control, vertexname, arcosname, policestation, comparendos):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    vertexfile = cf.data_dir + vertexname
    arcosfile = cf.data_dir + arcosname
    stationfile = open(cf.data_dir + policestation)
    comparendosfile = open(cf.data_dir + comparendos, encoding="utf8")
    input_vertex_file = csv.DictReader(open(vertexfile, encoding="utf-8"),
                                       delimiter=",")
    input_arcos_file = csv.DictReader(open(arcosfile, encoding="utf-8"),
                                      delimiter=",")
    station_data = json.load(stationfile)
    comparendos_data = json.load(comparendosfile)
    for comparendo in comparendos_data['features']:
        model.addComparendos(control, comparendo)
    for station in station_data['features']:
        model.addVertexStations(control, station)
    for vertex in input_vertex_file :
        model.addBogotaVertex(control, vertex)
        model.add_Req_vertex(control, vertex)
    for arco in input_arcos_file:
        model.addBogotaArc(control, arco)
        model.edge_req(control, arco)
    

    return control


# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control):
    """
    Retorna un dato por su ID.
    """
    start = get_time()
    tracemalloc.start()
    stations, numV, Vertex, min_lon, max_lon, min_lat, max_lat, Nume, comparendos, num_St, com_St, edges = model.get_data(control)
    end = get_time()
    delt = delta_time(start, end)
    tracemalloc.stop()
    return stations, numV, Vertex, min_lon, max_lon, min_lat, max_lat, Nume, comparendos, num_St, com_St, edges, delt


def req_1(control, initial_point, final_point):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1}
    star_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()
    distancia_total, numero_vertices_recorridos, camino = model.req_1(control, initial_point, final_point)
    final_time = getTime()
    delt = round(deltaTime_reqs(star_time, final_time), 3)
    end_memory = getMemory()
    tracemalloc.stop()
    deltM = round(deltaMemory(end_memory, start_memory), 2)
    return distancia_total, numero_vertices_recorridos, camino, delt, deltM

def req_2(control, initial_point, final_point):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    return model.req_2(control, initial_point, final_point)


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(control, M):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    star_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()

    total_vertices, lista_camino, vertice_initial, vertice_final, distancia_total, costo_total=model.req_4(control, M)

    final_time = getTime()
    delt = round(deltaTime_reqs(star_time, final_time), 3)
    end_memory = getMemory()
    tracemalloc.stop()
    deltM = round(deltaMemory(end_memory, start_memory), 2)

    return total_vertices, lista_camino, vertice_initial, vertice_final, distancia_total, costo_total, delt, deltM


def req_5(control, M, V):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    start = get_time()
    tracemalloc.start()
    distance, costo, total_vertices,vertices_identicadores, arcos, v = model.req_5(control, M, V)
    end = get_time()
    delt = delta_time(start, end)
    tracemalloc.stop()
    return distance, costo, total_vertices,vertices_identicadores, arcos, v, delt

def req_6(control, M):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    return model.req_6(control, int(M))



def req_7(control, initial_point, final_point):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7

    star_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()

    total_vertices, lista_vertices, vertice_initial, vertice_destiny, comparendos_totales, distancia_total=model.req_7(control, initial_point, final_point)

    final_time = getTime()
    delt = round(deltaTime_reqs(star_time, final_time), 3)
    end_memory = getMemory()
    tracemalloc.stop()
    deltM = round(deltaMemory(end_memory, start_memory), 2)

    return total_vertices, lista_vertices, vertice_initial, vertice_destiny, comparendos_totales, distancia_total, delt, deltM



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

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def deltaTime_reqs(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = round(float(end - start), 2)
    return elapsed
# Funciones para medir la memoria utilizada


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
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
    return round(delta_memory, 2)


