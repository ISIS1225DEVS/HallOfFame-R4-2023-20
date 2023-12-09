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

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
def newController():
    return model.newDataStructs()

# Funciones para la carga de datos
def loadData(dataStructs):
    path = f'{cf.data_dir}'
    file = open(f'{path}/bogota_vertices.txt', encoding='utf-8')
    line = file.readline().strip('\n')
    while len(line) > 0:
        line = line.split(',')
        vertex = {'id': line[0], 'coordinates': (float(line[2]), float(line[1])), 'latitude': float(line[2]), 'longitude': float(line[1])}
        model.addVertex(dataStructs, vertex)
        line = file.readline().strip('\n')
    file.close()
    file = csv.DictReader(open(f'{path}/comparendos_2019_bogota_vertices.csv', encoding='utf-8'), delimiter=',')
    for infraction in file:
        model.addInfraction(dataStructs, infraction)
    file = csv.DictReader(open(f'{path}/estacionpolicia_bogota_vertices.csv', encoding='utf-8'), delimiter=',')
    for station in file:
        model.relateToVertex(dataStructs, station, 'stations')
    file = open(f'{path}/bogota_arcos.txt', encoding= "utf-8")
    line = file.readline().strip('\n')
    while len(line) > 0:
        line = line.split()
        edge = {"vertex": line[0], "adjacentVertex": line[1:]}
        model.addEdge(dataStructs, edge)
        line = file.readline().strip('\n')
    file.close()
    model.sortInfractions(dataStructs)

# Funciones de ordenamiento
def firstAndLastNData(data, N):
    return model.firstAndLastNData(data, N)

# Funciones de consulta sobre el catálogo
def req1(dataStructs, startPoint, arrivalPoint):
    tracemalloc.start()
    start_memory = getMemory()
    req, meta = model.req1(dataStructs, (float(startPoint[0]), float(startPoint[1])), (float(arrivalPoint[0]), float(arrivalPoint[1])))
    stop_memory = getMemory()
    tracemalloc.stop()
    deltaOfMemory = deltaMemory(stop_memory, start_memory)
    return req, meta, deltaOfMemory

def req2(dataStructs, startPoint, arrivalPoint):
    tracemalloc.start()
    start_memory = getMemory()
    req, meta = model.req2(dataStructs, (float(startPoint[0]), float(startPoint[1])), (float(arrivalPoint[0]), float(arrivalPoint[1])))
    stop_memory = getMemory()
    tracemalloc.stop()
    deltaOfMemory = deltaMemory(stop_memory, start_memory)
    return req, meta, deltaOfMemory

def req3(dataStructs, locality, M):
    tracemalloc.start()
    start_memory = getMemory()
    req, meta = model.req3(dataStructs, locality.title(), M)
    stop_memory = getMemory()
    tracemalloc.stop()
    deltaOfMemory = deltaMemory(stop_memory, start_memory)
    return req, meta, deltaOfMemory

def req4(dataStructs, M):
    tracemalloc.start()
    start_memory = getMemory()
    req, meta = model.req4(dataStructs, M)
    stop_memory = getMemory()
    tracemalloc.stop()
    deltaOfMemory = deltaMemory(stop_memory, start_memory)
    return req, meta, deltaOfMemory

def req5(dataStructs, vehicle, M):
    tracemalloc.start()
    start_memory = getMemory()
    req, meta = model.req5(dataStructs, vehicle.title(), M)
    stop_memory = getMemory()
    tracemalloc.stop()
    deltaOfMemory = deltaMemory(stop_memory, start_memory)
    return req, meta, deltaOfMemory

def req6(dataStructs, M):
    tracemalloc.start()
    start_memory = getMemory()
    req, meta = model.req6(dataStructs, M)
    stop_memory = getMemory()
    tracemalloc.stop()
    deltaOfMemory = deltaMemory(stop_memory, start_memory)
    return req, meta, deltaOfMemory

def req7(dataStructs, startPoint, arrivalPoint):
    tracemalloc.start()
    start_memory = getMemory()
    req, meta = model.req7(dataStructs, (float(startPoint[0]), float(startPoint[1])), (float(arrivalPoint[0]), float(arrivalPoint[1])))
    stop_memory = getMemory()
    tracemalloc.stop()
    deltaOfMemory = deltaMemory(stop_memory, start_memory)
    return req, meta, deltaOfMemory

# Funciones para medir tiempos de ejecucion
def getTime():
    return float(time.perf_counter()*1000)

def deltaTime(end, start):
    elapsed = float(end - start)
    return elapsed

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
    return delta_memory