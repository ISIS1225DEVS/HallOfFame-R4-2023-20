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
import csv
import model
import time
import json
import geojson
import tracemalloc
from DISClib.ADT import graph as gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt



"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    return model.new_data_structs()


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    start_time = get_time()
    dir_comparendos = cf.data_dir+'tickets/'+'comparendos_2019_bogota_vertices.csv'
    dir_estaciones = cf.data_dir+'tickets/'+'estacionpolicia_bogota_vertices.csv'
    filename_arcos=cf.data_dir+"/tickets/bogota_arcos.txt"
    filename_vertices=cf.data_dir+"/tickets/bogota_vertices.txt"

    comparendos = csv.DictReader(open(dir_comparendos,encoding='utf-8'),delimiter=",")
    estaciones = csv.DictReader(open(dir_estaciones,encoding='utf-8'),delimiter=",")

    lista_comparendos = lt.newList(datastructure='ARRAY_LIST')
    contador_comparendos = 0
    for comparendo in comparendos:
        lt.addLast(lista_comparendos, comparendo)
        contador_comparendos +=1
        tupla = (comparendo['VERTICES'], comparendo['TIPO_SERVICIO'], comparendo['INFRACCION'])
        lt.addLast(control['lista_comparendos_grave'], tupla)
        if mp.contains(control["hash_map_comparendos"], comparendo['VERTICES']):
            llv_lista = mp.get(control["hash_map_comparendos"], comparendo['VERTICES'])
            lista = me.getValue(llv_lista)
            lt.addLast(lista, comparendo)
            mp.put(control["hash_map_comparendos"], comparendo['VERTICES'], lista)
            
        else:
            lista = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(lista, comparendo)
            mp.put(control["hash_map_comparendos"], comparendo['VERTICES'], lista)

        if mp.contains(control["hash_map_localides_comparendos"], comparendo['LOCALIDAD']):

            llv_mapa_vertices = mp.get(control["hash_map_localides_comparendos"], comparendo['LOCALIDAD'])
            mapa_vertices = me.getValue(llv_mapa_vertices)
            if mp.contains(mapa_vertices, comparendo['VERTICES']):
                llv_lista = mp.get(mapa_vertices, comparendo['VERTICES'])
                lista = me.getValue(llv_lista)
                lt.addLast(lista, comparendo)
                mp.put(mapa_vertices, comparendo['VERTICES'], lista)
                mp.put(control['hash_map_localides_comparendos'], comparendo['LOCALIDAD'], mapa_vertices)
            else:
                lista = lt.newList(datastructure='ARRAY_LIST')
                lt.addLast(lista, comparendo)
                mp.put(mapa_vertices, comparendo['VERTICES'], lista)
                mp.put(control["hash_map_localides_comparendos"], comparendo['LOCALIDAD'], mapa_vertices)
        else:
            mapa_vertices = mp.newMap(maptype='CHAINING')
            lista = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(lista, comparendo)
            mp.put(mapa_vertices, comparendo['VERTICES'], lista)
            mp.put(control['hash_map_localides_comparendos'], comparendo['LOCALIDAD'], mapa_vertices)

    model.sort_comparendos_mas_graves(control)

    lista_estaciones = lt.newList(datastructure='ARRAY_LIST')
    contador_estaciones = 0
    for estacion in estaciones:
        lt.addLast(lista_estaciones, estacion)
        contador_estaciones +=1
        mp.put(control['hash_map_estaciones'], estacion['VERTICES'], estacion)

    input_file_arcos= open(filename_arcos).readlines()[2:]
    input_file_arcos = [line.rstrip('\n') for line in input_file_arcos]
    input_file_vertices=open(filename_vertices).readlines()
    input_file_vertices = [line.rstrip('\n') for line in input_file_vertices]

    lista_vertices = lt.newList(datastructure='ARRAY_LIST')
    contador_vertices = 0
    for vertice in input_file_vertices:
        lt.addLast(lista_vertices, vertice)
        contador_vertices += 1
        str_list = vertice.split(',')
        num = str_list[0]
        coords = (str_list[1], str_list[2])
        mp.put(control["hash_map_num_loc"], num, coords)
        model.add_vertice(control,num)

    lista_arcos = lt.newList(datastructure='ARRAY_LIST')
    contador_arcos = 0
    for arco in input_file_arcos:
        lt.addLast(lista_arcos, arco)
        contador_arcos += 1
        model.add_arcos(control, arco)

    lista_comparendos_10 = lt.subList(lista_comparendos, 1, 5)
    lista_estaciones_10 = lt.subList(lista_estaciones, 1, 5)
    lista_vertices_10 = lt.subList(lista_vertices, 1, 5)
    lista_arcos_10 = lt.subList(lista_arcos, 1, 5)
    for comparendo2 in lt.subList(lista_comparendos, lt.size(lista_comparendos)-5, 5):
        lt.addLast(lista_comparendos_10, comparendo2)
    for estaciones2 in lt.subList(lista_estaciones, lt.size(lista_estaciones)-5, 5):
        lt.addLast(lista_estaciones_10, estaciones2)
    for vertice2 in lt.subList(lista_vertices, lt.size(lista_vertices)-5, 5):
        lt.addLast(lista_vertices_10, vertice2)
    for arco2 in lt.subList(lista_arcos, lt.size(lista_arcos)-5, 5):
        lt.addLast(lista_arcos_10, arco2)



    stop_time = get_time()
    delta_times = delta_time(start_time, stop_time)
    print('La carga se ha demorado: ' + str(delta_times) + ' milisegundos')
    return contador_vertices, contador_arcos, contador_comparendos, contador_estaciones, lista_comparendos_10, lista_estaciones_10, lista_vertices_10, lista_arcos_10


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


def req_1(control, punto_origen_lat, punto_origen_lon, punto_destino_lat, punto_destino_lon):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    return model.req_1(control, punto_origen_lat, punto_origen_lon, punto_destino_lat, punto_destino_lon)


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control, localidad, cantidad_cams):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()
    cant_vertices, lista_vertices, lista_arcos, dist_total = model.req_3(control, localidad, cantidad_cams)
    stop_time = get_time()
    delta_times = delta_time(start_time, stop_time)
    print('El algoritmos se ha demorado: ' + str(delta_times) + ' milisegundos')
    return cant_vertices, lista_vertices, lista_arcos, dist_total


def req_4(control, cantidad_cams):
    """
    Retorna el resultado del requerimiento 4
    """
    start_time = get_time()
    cant_vertices, lista_vertices, lista_arcos, dist_total = model.req_4(control,cantidad_cams)
    stop_time = get_time()
    delta_times = delta_time(stop_time,start_time)
    print('El algoritmos se ha demorado: ' + str(delta_times) + ' milisegundos')
    print("\n")
    return cant_vertices, lista_vertices, lista_arcos, dist_total


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control, num_comparendos_graves):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6


    start_time = get_time()
    mapa_comp_est = model.req_6(control, num_comparendos_graves)
    stop_time = get_time()
    delta_times = delta_time(start_time, stop_time)
    print('El algoritmos se ha demorado: ' + str(delta_times) + ' milisegundos')
    return mapa_comp_est


def req_7(data_structs, punto_origen_lat, punto_origen_lon, punto_destino_lat, punto_destino_lon):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    return model.req_7(data_structs, punto_origen_lat, punto_origen_lon, punto_destino_lat, punto_destino_lon)


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
