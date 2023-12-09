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

csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    analyzer = model.new_data_structs()
    return analyzer

# Funciones para la carga de datos
def load_data(analyzer):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    load_vertices(analyzer)
    load_police_stations(analyzer)
    load_comparendos(analyzer)
    load_edges(analyzer)

    return analyzer

def load_vertices(analyzer):

    verticesRuta = cf.data_dir + "/tickets/bogota_vertices.txt"

    with open(verticesRuta, "r") as vertices:

        for vertice in vertices:
            infoVertex = vertice.split(",")
            vertexId = infoVertex[0]
            longitudeVertex = float(infoVertex[1])
            latitudeVertex = float(infoVertex[2])

            vertexDict = {
                          "ID": vertexId,
                          "longitudeVertex": longitudeVertex,
                          "latitudeVertex": latitudeVertex
                         }
            
            model.add_vertex(analyzer, vertexId, longitudeVertex, latitudeVertex, vertexDict)

def load_police_stations(analyzer):
    
    estacionesRuta = cf.data_dir + "/tickets/estacionpolicia_bogota_vertices.csv"

    with open(estacionesRuta, "r", encoding="utf-8") as estaciones: 
        estacionesCSV = csv.DictReader(estaciones, delimiter=",")
        
        for infoStation in estacionesCSV:
            model.add_police_station(analyzer, infoStation)

def load_comparendos(analyzer):
    
    comparendosRuta = cf.data_dir + "/tickets/comparendos_2019_bogota_vertices.csv"

    with open(comparendosRuta, "r", encoding="utf-8") as comparendos:
        comparendosCSV = csv.DictReader(comparendos, delimiter=",")

        for infoComparendo in comparendosCSV:
            model.add_comparendo(analyzer, infoComparendo)

def load_edges(analyzer):

    arcosRuta = cf.data_dir + "/tickets/bogota_arcos.txt"
            
    with open(arcosRuta, "r") as arcos:

        for arco in arcos:
            infoArco = arco.split()

            if len(infoArco) > 1:
                outVertex = infoArco[0]
                inVertices = infoArco[1:]    

                for inVertex in inVertices:
                    model.add_edge(analyzer, outVertex, inVertex)

# Funciones de consulta sobre el catálogo

def get_load_info(analyzer):
    """
    Retorna info del modelo
    """
    #TODO: Llamar la función del modelo para obtener un dato
    totalInfractions, InfractionsList, totalPoliceStations, policeStationsList, totalVertices, verticesList, limits, totalEdges, edgesList = model.get_load_info(analyzer)
    return totalInfractions, InfractionsList, totalPoliceStations, policeStationsList, totalVertices, verticesList, limits, totalEdges, edgesList

def req_1(analyzer, longitud1, latitud1, longitud2, latitud2):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    distancia, vertices, camino = model.req_1(analyzer, longitud1, latitud1, longitud2, latitud2)
    return distancia, vertices, camino

def req_2(analyzer, originLatiude, originLongitude, destinationLatitude, destinationLongitude):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    path, verticesPath, totalDistance, routeVertices = model.req_2(analyzer, originLatiude, originLongitude, destinationLatitude, destinationLongitude)
    return path, verticesPath, totalDistance, routeVertices

def req_3(analyzer, cameras, locality):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    camerasVertices, originVertex, routesRed, DistanceRed, totalCost = model.req_3(analyzer, cameras, locality)
    return camerasVertices, originVertex, routesRed, DistanceRed, totalCost

def req_4(analyzer, m):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    time, total, vertices, ruta, km, costo = model.req_4(analyzer, m)
    return time, total, vertices, ruta, km, costo

def req_5(data, m, clase_v):
    """
    Retorna el resultado del requerimiento 5
    """
    time_1 = get_time()
    m, vertices_red, kms, costo_total = model.req_5(data['connectionsDistance'], data['intersections'], m, clase_v)
    time_2 = get_time()
    total = delta_time(time_1, time_2)
    return m, vertices_red, kms, costo_total, total

def req_6(data, estacion, m):
    """
    Retorna el resultado del requerimiento 6
    """
    time_1 = get_time()
    rta = model.req_6(data['connectionsDistance'], data['intersections'], m, data['policeStations'], estacion)
    time_2 = get_time()
    total = delta_time(time_1, time_2)
    return rta, total 

def req_7(analyzer, originLatiude, originLongitude, destinationLatitude, destinationLongitude):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    path, verticesPath, totalInfractions, totalDistance = model.req_7(analyzer, originLatiude, originLongitude, destinationLatitude, destinationLongitude)
    return path, verticesPath, totalInfractions, totalDistance

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