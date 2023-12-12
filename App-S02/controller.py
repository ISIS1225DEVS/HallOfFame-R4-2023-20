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
import tracemalloc
import math
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
    control['model'] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control, filename):
    """
    Carga los datos del reto
    """
    inicio = time.time()
    vertices = open("Data/tickets/bogota_vertices.txt")
    n_vertices = 0
    for linea in vertices:
        info = linea.strip().split(",")
        model.add_vertex(control["model"], info)
        n_vertices += 1
    vertices.close()
    
    n_comparendos = 0
    input_file = csv.DictReader(open("Data/tickets/comparendos_2019_bogota_vertices.csv", encoding='utf-8'))
    for comparendo in input_file:
        model.cargar_comparendo(control["model"], comparendo)
        n_comparendos += 1
    
    n_estaciones = 0
    input_file = csv.DictReader(open("Data/tickets/estacionpolicia_bogota_vertices.csv", encoding='utf-8'))
    for estacion in input_file:
        model.cargar_estacion(control["model"], estacion)
        n_estaciones += 1
    
    arcos = open("Data/tickets/bogota_arcos.txt")
    n_arcos = -2
    for linea in arcos:
        n_arcos += 1
        if n_arcos > 0:
            info = linea.strip().split(" ")
            model.agregar_arco(control["model"], info)
    arcos.close()
    fin = time.time()
    tiempo = fin-inicio
    return n_vertices, n_arcos, n_comparendos, n_estaciones, tiempo

# Funciones de ordenamiento

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


def req_1(control, latO, longO, latD, longD):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    camino, totalD, totalV = model.req_1(control['model'], latO, longO, latD, longD)
    
    
    
    
    return camino, totalD, totalV


def req_2(control, latO, longO, latD, longD):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    
    camino, totalD, totalV = model.req_2(control['model'], latO, longO, latD, longD)
    
    
    
    
    return camino, totalD, totalV
    
    pass


def req_3(control, n, localidad):
    """
    Retorna el resultado del requerimiento 3
    """
    inicio = time.time() 
    vertices_red, arcos_red, distance, costo, total_v = model.req_3(control["model"], n, localidad)
    fin = time.time()
    tiempo = fin-inicio
    return vertices_red, arcos_red, distance, costo, total_v, tiempo


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control, n):
    """
    Retorna el resultado del requerimiento 6
    """
    inicio = time.time() 
    total_v, grupos_v, arcos_red, distance = model.req_6(control["model"], n)
    fin = time.time()
    tiempo = fin-inicio
    return total_v, grupos_v, arcos_red, distance, tiempo


def req_7(control, lato, longo, latd, longd):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    camino = model.req_7(control['model'], lato, longo, latd, longd)
    return camino


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
