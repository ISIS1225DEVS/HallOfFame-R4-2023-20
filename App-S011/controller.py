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
import json


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""




def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control= model.new_data_structs()

    return control


# Funciones para la carga de datos

def load_data(control,arcosFile,verticesFile,comparendosFile,esatcionesFile):

    
    archivo_vertices = open(verticesFile, "r", encoding="utf-8")

    for linea in archivo_vertices.readlines():
        id, longitud,  latitud = linea.split(",")
        vertice = {
            "id": int(id),
            "longitud": float(longitud),
            "latitud": float(latitud),
        }
        model.add_vertice(control, vertice)

    archivo_vertices.close()



    archivo_arcos = open(arcosFile, "r", encoding="utf-8")
    
    cL = 0
    for linea in archivo_arcos.readlines():
        if cL < 2:
            cL += 1
            continue
        info = linea.strip().split(" ")

        id = int(info[0])
        adyacentes = list(map(int, info[1:]))
        if len(adyacentes)!=0:
            for x in adyacentes:
                model.addArco(control, id,x)
                
    archivo_arcos.close()

    
    archivo_comparendos = csv.DictReader(open(comparendosFile, "r", encoding="utf-8"))
    len_comparendos=0
    for comparendo in archivo_comparendos:
        len_comparendos +=1
        model.addComparendo(control, comparendo)
  
    archivo_estaciones = csv.DictReader(open(esatcionesFile, "r", encoding="utf-8"))

    for estacion in archivo_estaciones:
        model.addEstacion(control, estacion)
    

    return control
    








def printCarga(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    data= model.printData(control)
    return data


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


def req_1(analyzer, longI, latiI, longDes, latitudDes):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    return model.req_1(analyzer, longI, latiI, longDes, latitudDes)


def req_2(control, iniLong, iniLati, desLong, desLati):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    return model.req_2(control, iniLong, iniLati, desLong, desLati)


def req_3(analyzer, localidad, m):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    return model.req_3(analyzer, localidad, int(m))


def req_4(control, m):
    """
    Retorna el resultado del requerimiento 4
    """
    return model.req_4(control, int(m))


def req_5(control, m, vehiculo):
    """
    Retorna el resultado del requerimiento 5
    """
    return model.req_5(control, int(m), vehiculo)


def req_6(control, m):
    """
    Retorna el resultado del requerimiento 6
    """
    return model.req_6(control, int(m))


def req_7(control):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    return model.req_7(control)


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
