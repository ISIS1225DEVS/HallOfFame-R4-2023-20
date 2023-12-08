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
 * (at your option) any longer version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * alat withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import time
import csv
import tracemalloc
import json
import folium

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {"model": None}
    
    control["model"] = model.new_vial()
    
    return control


# Funciones para la carga de datos
def mapa_carga():
    m = folium.Map(location=(3.82, -73.20))
    return m

def load_data(control):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    
    tiempo_i = get_time()
    
    vial = control["model"]
    
    m = mapa_carga()
    
    vertices, min_long, min_lat, max_long, max_lat= load_vertices(vial, m)
    estaciones = load_estaciones(vial, m)
    comparendos = load_comparendos(vial, m)
    load_arcos(vial)
    arcos, t_arcos = model.list_arcos_adj(control["model"])
    model.agregar_comparendos_m(vial, m) 
    
    m.show_in_browser()
    
    tiempo_f = get_time()
    d_time = delata_time(tiempo_i, tiempo_f)
    
    return vertices, min_long, min_lat, max_long, max_lat, estaciones, comparendos, arcos, t_arcos, d_time
    
def load_vertices(vial, m):
    vertices_file = cf.data_dir + "tickets/bogota_vertices.txt"
    
    with open(vertices_file, "r") as vert_file:
        min_long = 0
        max_long = 0
        min_lat = 0
        max_lat = 0
        for info_vertice in vert_file :
            vertice = info_vertice.strip().split(",")
            if min_long == 0:
                min_long = float(vertice[1])
                max_long = float(vertice[1])
                min_lat = float(vertice[2])
                max_lat = float(vertice[2])
            else:
                if float(vertice[1]) < min_long:
                    min_long = float(vertice[1])
                if float(vertice[1]) > max_long:
                    max_long = float(vertice[1])
                if float(vertice[2]) < min_lat:
                    min_lat = float(vertice[2])
                if float(vertice[2]) > max_lat:
                    max_lat = float(vertice[2])
                    
            vertice_carga = model.add_vertice(vial ,vertice, m)
    return vertice_carga, min_lat, min_long, max_lat, max_long

def load_estaciones(vial, m):
    
    """
    with open(estaciones_file, encoding="utf-8") as est_file:
        estaciones = json.load(est_file)
        for dic in estaciones["features"]:
            estacion = dic["properties"]
            estaciones_carga = model.add_estacion(control["model"], estacion, m)
    """
    estaciones_file = cf.data_dir + "tickets/estacionpolicia_bogota_vertices.csv"
    input_file = csv.DictReader(open(estaciones_file, encoding="utf8"))
    for estacion in input_file:
        estaciones_carga = model.add_estacion(vial,estacion, m)
    
    return estaciones_carga

def load_comparendos(vial, m):
    comparendos_file = cf.data_dir + "tickets/comparendos_2019_bogota_vertices.csv"
    """
    with open(comparendos_file, encoding="utf-8") as comp_file:
        comparendos = json.load(comp_file)
        for dic in comparendos["features"]:
            comparendo = dic["properties"]
            comparendos_carga = model.add_comparendo(control["model"], comparendo)
    """   
    input_file = csv.DictReader(open(comparendos_file, encoding="utf8"))
    for comparendo in input_file:
        comparendos_carga = model.add_comparendo(vial, comparendo, m)
    #vial["comparendos_gravedad"] = model.ordenar_comparendos_gravedad(comparendos_gravedad)
    
    
    return comparendos_carga




def load_arcos(vial):
    arcos_file = cf.data_dir + "tickets/bogota_arcos.txt"
    
    with open(arcos_file, "r") as arc_file:
        for info_arco in arc_file :
            arco = info_arco.strip().split(" ")
            if arco[0] != "#":
              model.add_arco(vial, arco)
            
    return None
    

    
    


# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulata sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, lat_i, long_i, lat_f, long_f):
    """
    Retorna el resulatado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    tiempo_i = get_time()
    vertices, dist = model.req_1(control["model"], lat_i, long_i, lat_f, long_f)
    tiempo_f = get_time()
    d_time = delata_time(tiempo_i, tiempo_f)
    
    return vertices, dist, d_time


def req_2(control, lat_i, long_i, lat_f, long_f):
    """
    Retorna el resulatado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    tiempo_i = get_time()
    vertices, dist = model.req_2(control["model"], lat_i, long_i, lat_f, long_f)
    tiempo_f = get_time()
    d_time = delata_time(tiempo_i, tiempo_f)
    
    return vertices, dist, d_time

def req_3(control, localidad , m):
    """
    Retorna el resulatado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    tiempo_i = get_time()
    result = model.req_3(control["model"], localidad, m)
    tiempo_f = get_time()
    d_time = delata_time(tiempo_i, tiempo_f)
    return result , d_time

def req_4(control, n):
    """
    Retorna el resulatado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    tiempo_i = get_time()
    total_vertices, lista_vertices, arcos, total_km, costo = model.req_4(control["model"], n)
    tiempo_f = get_time()
    d_time = delata_time(tiempo_i, tiempo_f)
    
    return total_vertices, lista_vertices, arcos, total_km, costo, d_time


def req_5(control, clase_carro, m):
    """
    Retorna el resulatado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    tiempo_i= get_time()
    total_vertices, lis_vertices, arcos, total_km, costo= model.req_5(control["model"], clase_carro, m)
    tiempo_f= get_time()
    d_time= delata_time(tiempo_i, tiempo_f)
    return total_vertices, lis_vertices, arcos, total_km, costo, d_time

def req_6(control):
    """
    Retorna el resulatado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(control, lat_i, long_i, lat_f, long_f):
    """
    Retorna el resulatado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    tiempo_i = get_time()
    vertices, arcos, comparendos, km = model.req_7(control["model"], lat_i, long_i, lat_f, long_f)
    tiempo_f = get_time()
    d_time = delata_time(tiempo_i, tiempo_f)
    
    return vertices, arcos, comparendos, km, d_time


def req_8(control):
    """
    Retorna el resulatado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delata_time(start, end):
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


def delata_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resulatado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delata_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delata_memory = delata_memory + stat.size_diff
    # de Byte -> kByte
    delata_memory = delata_memory/1024.0
    return delata_memory
