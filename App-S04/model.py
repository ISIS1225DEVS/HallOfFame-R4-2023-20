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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
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
assert cf
import math as m
from tabulate import tabulate

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    # Inicializar las estructuras de datos
    data_structs = {'stations_list':None,
                    'tickets_list':None,
                    'vertex_list':None,
                    'edges_list':None,
                    'graph_distance':None,
                    'graph_tickets':None,
                    'vertex_map':None,
                    'vertex_tree':None,
                    'req3':{},
                    'req5':{},
                    'req6':{}}
    
    data_structs['stations_list'] = lt.newList(datastructure='ARRAY_LIST') # lista de todas las estaciones
    data_structs['tickets_list'] = lt.newList(datastructure='ARRAY_LIST') # lista de todos los comparendos
    data_structs['vertex_list'] = lt.newList(datastructure='ARRAY_LIST') # lista de todos los vertices
    data_structs['edges_list'] = lt.newList(datastructure='ARRAY_LIST') # lista de todos los arcos cargados
    
    data_structs['graph_distance'] = gr.newGraph(size=250000,
                                                 cmpfunction=compareGraphs) # grafo con arcos de distancia
    
    data_structs['graph_tickets'] = gr.newGraph(size=250000,
                                                cmpfunction=compareGraphs) # grafo con arcos de comparendos
    
    data_structs['vertex_map'] = mp.newMap(numelements=100000,
                                           loadfactor=3) # mapa de los vertices del grafo
    
    data_structs['vertex_tree'] = om.newMap(cmpfunction=compareVertexLatitudeAndLongitude) # arbol para ubicar los vertices de acuerdo a latitud y longitud
    
    data_structs['req6']['stations'] = gr.newGraph(cmpfunction=compareGraphs) # grafo de las estaciones para el requerimiento 6
    data_structs['req6']['subgraphs'] = mp.newMap(loadfactor=4) # mapa con los 21 subgrafos del requerimiento 6, cada valor es un grafo
    data_structs['req6']['tickets'] = mp.newMap(loadfactor=4) # mapa de todas las gravedades de comparendos, cada valor es un stack
    data_structs['req6']['queue'] = mpq.newMinPQ(cmpfunction=compareGravity) # cola de prioridad indexada de todos los comparendo, cada valor es una llave del mapa
    
    return data_structs


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Funciones para agregar informacion al modelo
# =============================================================================================================================================================================
# =============================================================================================================================================================================

def addData(data_structs, data, filename, count):
    """
    Función para agregar nuevos elementos a la lista
    """
    # Crear la función para agregar elementos a una lista
    addListItem(data_structs, data, filename) # añadir información a las listas
    # añadir información a los grafos y demás estructuras
    if filename == 'vertex':
        newVertexData(data_structs, data, count) 
    elif filename == 'station':
        newStationsData(data_structs, data, count)
    elif filename == 'ticket':
        newTicketData(data_structs, data, count)
    elif filename == 'edge':
        newEdgeData(data_structs, data, count)

def addListItem(data_structs, data, filename):
    if filename == 'vertex':
        new_data = getVertexData(data)
        lt.addLast(data_structs['vertex_list'], new_data)
        
    elif filename == 'station':
        new_data = getStationData(data)
        lt.addLast(data_structs['stations_list'], new_data)
        
    elif filename == 'ticket':
        new_data = getTicketData(data)
        lt.addLast(data_structs['tickets_list'], new_data)
        
    elif filename == 'edge':
        new_data = getEdgeData(data)
        lt.addLast(data_structs['edges_list'], new_data) 


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Funciones para creacion de datos
# =============================================================================================================================================================================
# =============================================================================================================================================================================


# =============================================================================================================================================================================
# Vertices

def newVertexData(data_structs, data, count):
    """
    Crea una nueva estructura para modelar los datos
    """
    # Crear la función para estructurar los datos
    
    # se accede a todas las estructuras de datos del necesarias
    vertices_map = data_structs['vertex_map']
    vertices_tree = data_structs['vertex_tree']
    graph_distance = data_structs['graph_distance']
    graph_tickets = data_structs['graph_tickets']
    req6 = data_structs['req6']
    # obtener datos del vertice 
    data_list = data.split(',')
    # obtener el índice del vertice
    index = int(data_list[0])
    # agregar vertice a los grafos
    gr.insertVertex(graph_distance, index)
    gr.insertVertex(graph_tickets, index)
    # obtener longitud y latitud del vertice
    longref = data_list[1]
    latref = data_list[2]
    coordinates = {'long':longref, 'lat':latref}
    # crear la información del vertice
    vertex = {'index':index, # vertice mas cercano
              'coordinates':coordinates, # coordenadas
              'stations':lt.newList('ARRAY_LIST'), # lista de estaciones
              'tickets':lt.newList('ARRAY_LIST')} # lista de comparendos
    # poner el vertice en el mapa del vertice
    if not mp.contains(vertices_map, index):
        mp.put(vertices_map, index, vertex)
    # verificar el arbol de vertices agregar la latitud
    if not om.contains(vertices_tree, (round(float(latref), 2))):
        om.put(vertices_tree, (round(float(latref), 2)), om.newMap(cmpfunction=compareVertexLatitudeAndLongitude))
    # acceder a la latitud en el arbol, el cual es un arbol de longitud
    entry = om.get(vertices_tree, round(float(latref), 2))
    long_map = me.getValue(entry)
    # acceder a la longitud en el arbol, si no existe crear una lista vacia
    if not om.contains(long_map, (round(float(longref), 2))):
        om.put(long_map, (round(float(longref), 2)), lt.newList('ARRAY_LIST'))
    # agregar el vertice a la lista
    entry = om.get(long_map, round(float(longref), 2))
    long_lst = me.getValue(entry)
    lt.addLast(long_lst, vertex)
    # cambiar valores de latitud/longitud mínima/máxima
    if float(longref) > float(count['limits']['longmax']):
        count['limits']['longmax'] = longref
        
    if float(longref) < float(count['limits']['longmin']):
        count['limits']['longmin'] = longref
        
    if float(latref) > float(count['limits']['latmax']):
        count['limits']['latmax'] = latref
        
    if float(latref) < float(count['limits']['latmin']):
        count['limits']['latmin'] = latref
    # req6
    req6Vertices(req6, vertex)

def req6Vertices(req6, vertex):
    # acceder a las estructuras de datos del req6
    req6_stations = req6['stations']
    req6_subgraphs = req6['subgraphs']
    # obtener latitud y longitud
    latref = vertex['coordinates']['lat']
    longref = vertex['coordinates']['long']
    # obtener estacion más cercana
    closest_station = getClosestStation(latref, longref, req6_stations, req6_subgraphs) 
    # acceder al subgrafo de la estación
    entry = mp.get(req6_subgraphs, closest_station)
    station = me.getValue(entry)
    # insertar vértice al subgrafo
    gr.insertVertex(station['graph'], vertex['index'])
    # crear información del vértice
    info = {'index':vertex['index'], # indice del vertice
            'coordinates': vertex['coordinates'], # coordenadas del vertice
            'station':closest_station} # estación más cercana
    # agregar la información al mapa del subgrafo
    mp.put(station['vertices'], vertex['index'], info)


# =============================================================================================================================================================================
# Estaciones

def newStationsData(data_structs, data, count):
    """
    Crea una nueva estructura para modelar los datos
    """
    # Crear la función para estructurar los datos
    # se accede a todas las estructuras necesarias
    vertices_map = data_structs['vertex_map']
    vertices_tree = data_structs['vertex_tree']
    req6 = data_structs['req6']
    req6_stations = req6['stations']
    req6_subgraphs = req6['subgraphs']
    # se obtiene la latitud y longitud de la estación
    data_lat = data['EPOLATITUD']
    data_long = data['EPOLONGITU']
    name = data['EPONOMBRE']
    # buscar los vertices más cercanos
    closest_vertex = int(data['VERTICES'])
    # añadir informacion de la estación al vertice
    if not mp.contains(vertices_map, closest_vertex):
        coordinates = {'long':data_long, 'lat':data_lat}
        vertex = {'index':closest_vertex, # vertice mas cercano
                  'coordinates':coordinates, # coordenadas
                  'stations':lt.newList('ARRAY_LIST'), # lista de estaciones
                  'tickets':lt.newList('ARRAY_LIST')} # lista de comparendos
        mp.put(vertices_map, closest_vertex, vertex)
    # acceder al vertice
    vertex_entry = mp.get(vertices_map, closest_vertex)
    vertex = me.getValue(vertex_entry)
    # añadir estación al vertice
    lt.addLast(vertex['stations'], data)
    # ===== req6 =====
    # crear información de la estacion para el requerimiento 6
    coordinates = {'lat':data_lat, 'long':data_long}
    station = {'index':closest_vertex, # vertice de la estación
               'coordinates':coordinates, # coordenadas
               'station':data, # toda la información original de la estación
               'graph':gr.newGraph(cmpfunction=compareGraphs), # el subgrafo de la estación
               'vertices':mp.newMap(loadfactor=4)} # el mapa de vertices del subgrafo
    gr.insertVertex(req6_stations, closest_vertex) # insertar la estacion al grafo de estaciones
    gr.insertVertex(station['graph'], closest_vertex) # insertar el vertice al subgrafo de la estacion
    mp.put(req6_subgraphs, closest_vertex, station) # insertar el vertice en el mapa del subgrafo


# =============================================================================================================================================================================
# Comparendos

def newTicketData(data_structs, data, count):
    """
    Crea una nueva estructura para modelar los datos
    """
    # Crear la función para estructurar los datos
    vertices_map = data_structs['vertex_map']
    vertices_tree = data_structs['vertex_tree']
    req3 = data_structs['req3']
    req5 = data_structs['req5']
    req6 = data_structs['req6']
    # obtener latitud y longitud
    data_lat = data['LATITUD']
    data_long = data['LONGITUD']
    # obtener el vertice mas cercano
    closest_vertex = int(data['VERTICES'])
    # añadir información del comparendo al vertice
    vertex_entry = mp.get(vertices_map, closest_vertex)
    vertex = me.getValue(vertex_entry)
    lt.addLast(vertex['tickets'], data)
    # requerimiento 3
    req3TicketData(data, req3, closest_vertex, data_lat, data_long)
    #requerimiento 5
    req5TicketData(data, req5, closest_vertex, data_lat, data_long)
    # requerimiento 6
    req6TicketData(data, req6, closest_vertex, data_lat, data_long, vertex)
        
    #requerimiento 5
    '''vehicle_info = data['CLASE_VEHICULO']
    vehicle_exist = mp.contains(req5, vehicle_info)
    if vehicle_exist:
        entry_vehicle = mp.get(req5, vehicle_info)
        vehicle = me.getValue(entry_vehicle)
    else:
        vehicle = {'vehicle':vehicle_info,
                   'vertex':None}
        vehicle['vertex'] = mp.newMap()
        mp.put(req5, vehicle_info, vehicle)
    vertex_exist = mp.contains(vehicle['vertex'], closest_vertex )
    if vertex_exist:
        entry_vertex = mp.get(vehicle['vertex'], closest_vertex)
        tickets = me.getValue(entry_vertex)
    else:
        tickets = {'vertex':closest_vertex,
                   'tickets':None}
        tickets['tickets'] = lt.newList('ARRAY_LIST')
        mp.put(vehicle['vertex'],closest_vertex, tickets)
    lt.addLast(tickets['tickets'],data)'''
    
    
        
    
    
    
    
    
    
def req3TicketData(data, req3, closest_vertex, data_lat, data_long):
    data_localidad = data['LOCALIDAD'] 
    # corregir nombre de la localidad
    data_localidad = data_localidad.lower().strip(' ')
    if '-' in data_localidad:
        data_localidad = data_localidad.split('-')
        data_localidad = data_localidad[1].strip(' ')
    # agregar localidad al diccionario
    if data_localidad not in req3:
        req3[data_localidad] = None
    # crear info de la localidad
    if req3[data_localidad] is None:
        req3[data_localidad] = {'graph':gr.newGraph(cmpfunction=compareGraphs), # subgrafo vacío
                                'vertices':mp.newMap(loadfactor=4), # mapa de vertices de la localidad con comparendos
                                'tickets':impq.newIndexMinPQ(cmpfunction=compareLocalidad)} # cola de prioridad vacía
    # insertar vertice del comparendo 
    if not gr.containsVertex(req3[data_localidad]['graph'], closest_vertex):
        gr.insertVertex(req3[data_localidad]['graph'], closest_vertex)
    # si no existe, crear vertice en el mapa de vertices
    if not mp.contains(req3[data_localidad]['vertices'], closest_vertex):
        v = {'coordinates':{'lat':data_lat, 'long':data_long}, # coordenadas
             'tickets':lt.newList('ARRAY_LIST')} # lista de comparendos
        mp.put(req3[data_localidad]['vertices'], closest_vertex, v)
    # obtener vertice del mapa
    entry = mp.get(req3[data_localidad]['vertices'], closest_vertex)
    vertex_list = me.getValue(entry)
    # añadir comparendo a la lista del vertice
    lt.addLast(vertex_list['tickets'], data)
    
    
def req5TicketData(data, req5, closest_vertex, data_lat, data_long):
    data_vehicle = data['CLASE_VEHICULO'] 
    # agregar vehiculo al diccionario
    if data_vehicle not in req5:
        req5[data_vehicle] = None
    # crear info del vehiculo
    if req5[data_vehicle] is None:
        req5[data_vehicle] = {'graph':gr.newGraph(cmpfunction=compareGraphs), # subgrafo vacío
                                'vertices':mp.newMap(loadfactor=4), # mapa de vertices de la localidad con comparendos
                                'tickets':impq.newIndexMinPQ(cmpfunction=compareLocalidad)} # cola de prioridad vacía
    # insertar vertice del comparendo 
    if not gr.containsVertex(req5[data_vehicle]['graph'], closest_vertex):
        gr.insertVertex(req5[data_vehicle]['graph'], closest_vertex)
    # si no existe, crear vertice en el mapa de vertices
    if not mp.contains(req5[data_vehicle]['vertices'], closest_vertex):
        v = {'coordinates':{'lat':data_lat, 'long':data_long}, # coordenadas
             'tickets':lt.newList('ARRAY_LIST')} # lista de comparendos
        mp.put(req5[data_vehicle]['vertices'], closest_vertex, v)
    # obtener vertice del mapa
    entry = mp.get(req5[data_vehicle]['vertices'], closest_vertex)
    vertex_list = me.getValue(entry)
    # añadir comparendo a la lista del vertice
    lt.addLast(vertex_list['tickets'], data)
    
        
def req6TicketData(data, req6, closest_vertex, data_lat, data_long, vertex):
    # obtener estructuras del req6
    req6_queue = req6['queue']
    req6_tickets_map  = req6['tickets']
    req6_stations = req6['stations']
    req6_subgraphs = req6['subgraphs']
    # obtener gravedad y tipo de servicio
    grav = data['INFRACCION']
    data_class = data['TIPO_SERVICIO']
    # crear llave
    key = f'{grav}-{data_class}'
    # si el mapa no contiene la llave
    if not mp.contains(req6_tickets_map, key):
        mp.put(req6_tickets_map, key, st.newStack()) # nuevo stack de comparendos
        mpq.insert(req6_queue, key) # insertar llave a la cola de prioridad
    # obtener el stack de la gravedad en el mapa de gravedades
    entry = mp.get(req6_tickets_map, key)
    ticket_stack = me.getValue(entry)
    # coordenadas
    coordinates = {'lat':vertex['coordinates']['lat'],
                   'long':vertex['coordinates']['long']}
    # obtener estación más cercana
    closest_station = getClosestStation(coordinates['lat'], coordinates['long'], req6_stations, req6_subgraphs)
    # crear información del comparendo
    info = {'index':closest_vertex,
            'closest_station':closest_station,
            'ticket':data,
            'coordinates':coordinates,
            'gravedad':key}
    # agregar comparendo al stack de la gravedad 
    st.push(ticket_stack, info)


# =============================================================================================================================================================================
# Arcos
    
def newEdgeData(data_structs, data, count):
    """
    Crea una nueva estructura para modelar los datos
    """
    # Crear la función para estructurar los datos
    # obtener estructuras de datos
    graph_distance = data_structs['graph_distance']
    graph_tickets = data_structs['graph_tickets']
    vertices_map = data_structs['vertex_map']
    req6 = data_structs['req6']
    # obtener vertice de partida
    vi_index = int(data[0])
    # obtener información del vertice
    vi_lat, vi_long, vi_tickets_list = getVertexEdgeInfo(vertices_map, vi_index)
    # recorrer los vecinos del vertice
    for vf_index in data[1:]:
        # obtener información de los vecinos
        vf_index = int(vf_index)
        vf_lat, vf_long, vf_tickets_list = getVertexEdgeInfo(vertices_map, vf_index)
        # contar distancia y cantidad total de comparendos
        distance = haversineDistance(vi_lat, vf_lat, vi_long, vf_long)
        tickets = lt.size(vi_tickets_list) + lt.size(vf_tickets_list)
        # añadir arcos al grafo de distancia y comparendos
        gr.addEdge(graph_distance, vi_index, vf_index, distance)
        gr.addEdge(graph_tickets, vi_index, vf_index, tickets)
        # requerimiento 6
        req6EdgesData(req6, vi_index, vf_index, distance)
        
def getVertexEdgeInfo(vertices_map, v_index):
    # obtener vertice del mapa
    entry = mp.get(vertices_map, v_index)
    v = me.getValue(entry)
    # obtener coordenadas y lista de comparendos
    v_lat = v['coordinates']['lat']
    v_long = v['coordinates']['long']
    v_tickets_list = v['tickets']
    return v_lat, v_long, v_tickets_list
            
def req6EdgesData(req6, vi_index, vf_index, distance):
    # obtener estructuras del requerimiento 6
    req6_stations = req6['stations']
    req6_subgraphs = req6['subgraphs']
    # obtener lista de estaciones del grafo
    stations = gr.vertices(req6_stations)
    for station_index in lt.iterator(stations):
        # obtener subgrafo de la estacion
        entry = mp.get(req6_subgraphs, station_index)
        station = me.getValue(entry)
        graph = station['graph']
        # si el subgrafo tiene ambos vertices, añadir arco
        if gr.containsVertex(graph, vi_index) and gr.containsVertex(graph, vf_index):
            gr.addEdge(graph, vi_index, vf_index, distance)


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Calculo de distancias
# =============================================================================================================================================================================
# =============================================================================================================================================================================

def haversineDistance(lat1, lat2, long1, long2):
    # convertir a radianes
    lat1 = m.radians(float(lat1))
    lat2 = m.radians(float(lat2))
    long1 = m.radians(float(long1))
    long2 = m.radians(float(long2))
    # primer termino
    halflatdiff = (lat2 - lat1)/2
    first_term = m.sin(halflatdiff)**2
    # segundo termino
    coslat1 = m.cos(lat1)
    coslat2 = m.cos(lat2)
    halflongdiff = (long2 - long1)/2
    second_term = coslat1 * coslat2 * (m.sin(halflongdiff)**2)
    # expresion de la raiz
    in_root_expression = first_term + second_term
    # termino final
    final_term = m.asin(m.sqrt(in_root_expression))
    # distancia final
    distance = 2*final_term*6341 
    return distance


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# crear listas para la vista
# =============================================================================================================================================================================
# =============================================================================================================================================================================

def createTopNSublist(lst, n):
    """creates a list that contains the first n and last n elements of
        a data structure

    Args:
        data_structs (list): original data structure
        n (int): 

    Returns:
        list: a list containing the first 3 and last 3 elements of the original list
    """
    topbot = lt.newList('ARRAY_LIST')
    toplist = lt.subList(lst, 1, n)
    botlist = lt.subList(lst, lt.size(lst)-n+1, n)
    
    for elem in lt.iterator(toplist):
        list_elem = []
        if type(elem) is dict:
            for value in elem.values():
                list_elem.append(value)
        elif type(elem) is list:
            for value in elem:
                list_elem.append(value)
        lt.addLast(topbot, list_elem)
    
    for elem in lt.iterator(botlist):
        list_elem = []
        if type(elem) is dict:
            for value in elem.values():
                list_elem.append(value)
        elif type(elem) is list:
            for value in elem:
                list_elem.append(value)
        lt.addLast(topbot, list_elem)
        
    return topbot


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Funciones de consulta
# =============================================================================================================================================================================
# =============================================================================================================================================================================

def getVertexData(data):
    """
    Retorna un dato a partir de su ID
    """
    # Crear la función para obtener un dato de una lista
    # crea elemento de la lista de vertices
    data = data.split(',')
    new_data = {'index':data[0],
                'lat':data[2],
                'long': data[1]}
    return new_data

def getStationData(data):
    """
    Retorna un dato a partir de su ID
    """
    # Crear la función para obtener un dato de una lista
    # crea elemento de la lista de estaciones
    new_data = {'id':data['OBJECTID'],
                'name':data['EPONOMBRE'],
                'lat':data['EPOLATITUD'],
                'long':data['EPOLONGITU'],
                'description':data['EPODESCRIP'],
                'address':data['EPODIR_SITIO'],
                'service':data['EPOSERVICIO'],
                'schedule':data['EPOHORARIO'],
                'telephone':data['EPOTELEFON'],
                'email':data['EPOCELECTR']
                }

    return new_data

def getTicketData(data):
    """
    Retorna un dato a partir de su ID
    """
    # Crear la función para obtener un dato de una lista
    # crea elemento de la lista de comparendos
    new_data = {'id':data['OBJECTID'],
                'lat':data['LATITUD'],
                'long':data['LONGITUD'],
                'date':data['FECHA_HORA'],
                'medium':data['MEDIO_DETECCION'],
                'vehicle':data['CLASE_VEHICULO'],
                'service':data['TIPO_SERVICIO'],
                'infraction':data['INFRACCION'],
                'description':data['DES_INFRACCION']
                }
    
    return new_data
    
def getEdgeData(data):
    """
    Retorna un dato a partir de su ID
    """
    # Crear la función para obtener un dato de una lista
    # crea elemento de la lista de arcos
    new_data = {'index':data[0],
                'neighbors':None}
    
    neighbors = []
    for neighbor in data[1:]:
        neighbors.append(neighbor)
        
    new_data['neighbors'] = tabulate([neighbors], tablefmt='grid')
    
    return new_data

def getListSize(lst):
    # retorna el tamaño de una lista para la vista
    return lt.size(lst)

def getEdges(data_structs):
    # obtener numero de arcos para la vista
    distance_graph = data_structs['graph_distance']
    edges = gr.numEdges(distance_graph)
    return edges

def getDataLists(data_structs):
    """ Return the data lists from the model

    Args:
        data_structs (dict): model with all the data structures

    Returns:
        tuple: tuple with all the lists of the model
    """
    stations = data_structs['stations_list']
    tickets = data_structs['tickets_list']
    vertices = data_structs['vertex_list']
    edges = data_structs['edges_list']
    
    return stations, tickets, vertices, edges


# =============================================================================================================================================================================
# Buscar mas cercano

def searchClosestVertex(graph, lat, long):
    # buscar vértice más cercano
    # primero se recorre el arbol de latitudes
    lat_entry = om.get(graph, round(float(lat), 2))
    if lat_entry is None:
        ceiling = om.ceiling(graph, round(float(lat), 2))
        floor = om.floor(graph, round(float(lat), 2))
        if ceiling is None:
            lat_entry = om.get(graph, floor)
        elif floor is None:
            lat_entry = om.get(graph, ceiling)
        else:
            ceiling_distance = abs(float(lat) - float(ceiling))
            floor_distance = abs(float(lat) - float(floor))
            if ceiling_distance < floor_distance:
                lat_entry = om.get(graph, ceiling)
            else:
                lat_entry = om.get(graph, floor)
    # se obtiene la latitud mas cercana, y se accede al arbol de longitudes
    long_map = me.getValue(lat_entry)
    # se recorre el arbol para buscar la longitud más cercana
    long_entry = om.get(long_map, round(float(long), 2))
    if long_entry is None:
        ceiling = om.ceiling(long_map, round(float(long), 2))
        floor = om.floor(long_map, round(float(long), 2))
        if ceiling is None:
            long_entry = om.get(long_map, floor)
        elif floor is None:
            long_entry = om.get(long_map, ceiling)
        else:
            ceiling_distance = abs(float(long) - float(ceiling))
            floor_distance = abs(float(long) - float(floor))
            if ceiling_distance < floor_distance:
                long_entry = om.get(long_map, ceiling)
            else:
                long_entry = om.get(long_map, floor)
    # se obtiene la lista de la longitud más cercana y se recorre
    lst = me.getValue(long_entry)
    # se recorre la lista para determinar cual es el vertice mas cercano
    closest_vertex = -1
    distance = float('inf')
    for vertex in lt.iterator(lst):
        vertex_lat = vertex['coordinates']['lat']
        vertex_long = vertex['coordinates']['long']
        temp_distance = haversineDistance(lat, vertex_lat, long, vertex_long)
        if temp_distance < distance:
            distance = temp_distance
            closest_vertex = vertex['index']
    # retorna el indice del vertice más cercano
    return closest_vertex

def getClosestStation(latref, longref, req6_stations, req6_subgraphs):
    # se busca la estación más cercana
    stations = gr.vertices(req6_stations)
    # se comparan todas las distancias del vertice a todas las estaciones
    mindist = float('inf')
    closest_station = -1
    for station_vertex in lt.iterator(stations):
        entry = mp.get(req6_subgraphs, station_vertex)
        station = me.getValue(entry)
        lat = station['coordinates']['lat']
        long = station['coordinates']['long']
        distance = haversineDistance(latref, lat, longref, long)
        if distance < mindist:
            mindist = distance
            closest_station = station_vertex  
    # retorna la estacion más cercana
    return closest_station


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Requerimientos
# =============================================================================================================================================================================
# =============================================================================================================================================================================


# =============================================================================================================================================================================
# req1

def req1(data_structs, vi, vf, count):
    """
    Función que soluciona el requerimiento 1
    """
    # Realizar el requerimiento 1
    distance_graph = data_structs['graph_distance']
    vertices_map = data_structs['vertex_map']
    vertices_tree = data_structs['vertex_tree']
    
    vi_index = searchClosestVertex(vertices_tree, vi['lat'], vi['long'])
    vf_index = searchClosestVertex(vertices_tree, vf['lat'], vf['long'])
    paths = dfs.DepthFirstSearch(distance_graph, vi_index)
    if not dfs.hasPathTo(paths, vf_index):
        temp_stack =  st.newStack()
    else:
        temp_stack = dfs.pathTo(paths, vf_index)
    
    path_q = st.newStack()
    i = 0
    prev = None
    while not st.isEmpty(temp_stack):
        vi = st.pop(temp_stack)
        qu.enqueue(path_q, vi)
        if i == 0:
            entry = mp.get(vertices_map, vi)
            vi_info = me.getValue(entry)
            vilat = vi_info['coordinates']['lat']
            vilong = vi_info['coordinates']['long']
            
            if prev is None:
                prev = {'index':vi,
                        'coordinates':{'lat':vilat,
                                       'long':vilong}}
            else:
                vflat = prev['coordinates']['lat']
                vflong = prev['coordinates']['long']
                
                count['distance'] += abs(haversineDistance(vilat, vflat, vilong, vflong))
                
                prev = {'index':vi,
                        'coordinates':{'lat':vilat,
                                       'long':vilong}}
            i+=1
        else:
            i = 0
        
    return path_q


# =============================================================================================================================================================================
# req2

def req2(data_structs, vi, vf, count):
    """
    Función que soluciona el requerimiento 2
    """
    # Realizar el requerimiento 2
    distance_graph = data_structs['graph_distance']
    vertices_map = data_structs['vertex_map']
    vertices_tree = data_structs['vertex_tree']
    
    vi_index = searchClosestVertex(vertices_tree, vi['lat'], vi['long'])
    vf_index = searchClosestVertex(vertices_tree, vf['lat'], vf['long'])
    
    paths = bfs.BreathFirstSearch(distance_graph, vi_index)
    if not bfs.hasPathTo(paths, vf_index):
        temp_stack =  st.newStack()
    else:
        temp_stack = bfs.pathTo(paths, vf_index)
        
    path_q = st.newStack()
    i = 0
    prev = None
    while not st.isEmpty(temp_stack):
        vi = st.pop(temp_stack)
        qu.enqueue(path_q, vi)
        if i == 0:
            entry = mp.get(vertices_map, vi)
            vi_info = me.getValue(entry)
            vilat = vi_info['coordinates']['lat']
            vilong = vi_info['coordinates']['long']
            
            if prev is None:
                prev = {'index':vi,
                        'coordinates':{'lat':vilat,
                                       'long':vilong}}
            else:
                vflat = prev['coordinates']['lat']
                vflong = prev['coordinates']['long']
                
                count['distance'] += abs(haversineDistance(vilat, vflat, vilong, vflong))
                
                prev = {'index':vi,
                        'coordinates':{'lat':vilat,
                                       'long':vilong}}
            i+=1
        else:
            i = 0
        
    return path_q


# =============================================================================================================================================================================
# req3

def req3(data_structs, cameras, localidad, cost, count):
    """
    Función que soluciona el requerimiento 3
    """
    # Realizar el requerimiento 3
    distance_graph = data_structs['graph_distance']
    req3 = data_structs['req3']
    
    count['included_vertices'] = st.newStack()
    
    localidad_vertices = req3[localidad]['vertices']
    localidad_tickets = req3[localidad]['tickets']

    most_tickets_queue = req3GetMostTickets(localidad_vertices, localidad_tickets, cameras)
    
    # version 1: Prim sencillo
    graph = gr.newGraph()
    req3MakeGraph(most_tickets_queue, graph, localidad_vertices)
    vertices = gr.vertices(graph)
    origin = lt.firstElement(vertices)
    mst = prim.PrimMST(graph)
    edges = prim.edgesMST(graph, mst)
    count['distance'] = prim.weightMST(graph, mst)
    count['cost'] = count['distance']*cost
    
    return edges, vertices, origin


def req3GetMostTickets(localidad_vertices, localidad_tickets, cameras):
    vertices_keylist = mp.keySet(localidad_vertices)
    for key in lt.iterator(vertices_keylist):
        entry = mp.get(localidad_vertices, key)
        vertex = me.getValue(entry)
        size = lt.size(vertex['tickets'])
        impq.insert(localidad_tickets, key, -size)
        
    most_tickets_queue = qu.newQueue()
    
    if impq.size(localidad_tickets) < cameras:
        for i in range(impq.size(localidad_tickets)):
            key = impq.min(localidad_tickets)
            qu.enqueue(most_tickets_queue, key)
            impq.delMin(localidad_tickets)
    else:
        for i in range(cameras):
            key = impq.min(localidad_tickets)
            qu.enqueue(most_tickets_queue, key)
            impq.delMin(localidad_tickets)
        
    return most_tickets_queue


def req3MakeGraph(most_tickets_queue, localidad_graph, localidad_vertices):
    while not qu.isEmpty(most_tickets_queue):
        vertex = int(qu.dequeue(most_tickets_queue))
        gr.insertVertex(localidad_graph, vertex)
    
    vertex_list = gr.vertices(localidad_graph)
    
    for vi_index in lt.iterator(vertex_list):
        entry = mp.get(localidad_vertices, vi_index)
        vi = me.getValue(entry)
        vi_lat = vi['coordinates']['lat']
        vi_long = vi['coordinates']['long']
        
        for vf_index in lt.iterator(vertex_list):
            if vi_index != vf_index:
                entry = mp.get(localidad_vertices, vf_index)
                vf = me.getValue(entry)
                vf_lat = vf['coordinates']['lat']
                vf_long = vf['coordinates']['long']
                
                distance = abs(haversineDistance(vi_lat, vf_lat, vi_long, vf_long))
                gr.addEdge(localidad_graph, vi_index, vf_index, distance)


# =============================================================================================================================================================================
# req4

def req_4(data_structures, cameras, cost, complete, counter):

    req4_data = data_structures['req4'][cameras]
    vertices_location, tickets_location = req4_data['vertices'], req4_data['tickets']
    tickets_queue = req4_get_best_selling_tickets(vertices_location, tickets_location, cameras)

    graph_location = gr.newGraph() if complete else req4_create_graph(tickets_queue, vertices_location)

    vertices = gr.vertices(graph_location)
    vertex_counter = req4_evaluate_vertices(graph_location, vertices)

    min_vertex = min(vertex_counter, key=lambda vertex: vertex_counter[vertex]['distancia'])
    paths = req4_compute_paths(graph_location, vertices, min_vertex, vertex_counter, complete, counter, cost)

    return paths, vertices, min_vertex


def req4_get_best_selling_tickets(vertices_location,cameras):
    sorted_vertices = sorted(vertices_location, key=lambda key: -lt.size(vertices_location[key]['tickets']))
    return qu.newQueue(sorted_vertices[:cameras])


def req4_create_graph(tickets_queue, vertices_location):
    graph_location = gr.newGraph()
    for vertex in qu.iterator(tickets_queue):
        gr.insert_vertex(graph_location, vertex)

    for vi_index in gr.vertices(graph_location):
        vi_coordinates = vertices_location[vi_index]['coordinates']
        for vf_index in gr.vertices(graph_location):
            if vi_index != vf_index:
                vf_coordinates = vertices_location[vf_index]['coordinates']
                gr.add_edge(graph_location, vi_index, vf_index)

    return graph_location


def req4_evaluate_vertices(graph_location,):
    vertex_counter = {}
    for vertex in gr.vertices(graph_location):
        vertex_counter[vertex] = {'busqueda': djk.Dijkstra(graph_location, vertex),
                                  'distancia': sum(djk.distance_to(vertex_counter[vertex]['busqueda'], idx)
                                                  for idx in gr.vertices(graph_location) if idx != vertex)}
    return vertex_counter


def req4_compute_paths(graph_location, vertices, min_vertex, vertex_counter, complete, counter, cost):
    if complete:
        paths = mp.newMap(loadfactor=4)
        search = vertex_counter[min_vertex]['busqueda']
        for vertex in gr.vertices(graph_location):
            if vertex != min_vertex:
                paths[vertex] = djk.path_to(search, vertex)
                counter['distancia'] += djk.distance_to(search, vertex)

        counter['costo'] = counter['distancia'] * cost
        return paths

    else:
        origin = lt.first_element(vertices)
        mst = prim.PrimMST(graph_location, origin)
        edges = prim.edges_MST(graph_location, mst)
        counter['distancia'] = prim.weight_MST(graph_location, mst)
        counter['costo'] = counter['distancia'] * cost
        return edges


# =============================================================================================================================================================================
# req5

def sort_infracciones_req5(data1, data2):
    if data1['total_infracciones'] != data2['total_infracciones']:
        return data1['total_infracciones'] < data2['total_infracciones']

def req_5(data_structs, M, vehicle ):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    #version 1 va hasta la línea 978
    '''req5 = data_structs['req5']
    grafo_distancia = data_structs['graph_distance']
    vehicle_entry = mp.get(req5, vehicle)
    vehicle_map = me.getValue(vehicle_entry)['vertex']
    vertices_vehiculo = mp.keySet(vehicle_map)
    lista_vertices =lt.newList('ARRAY_LIST') 
    for vertex in lt.iterator(vertices_vehiculo):
        entry_elemento = mp.get(vehicle_map, vertex)
        value_elemento = me.getValue(entry_elemento)
        cantidad_tickets = lt.size(value_elemento['tickets'])
        elemento = {'vertex':vertex,
                    'total_infracciones':cantidad_tickets}
        lt.addLast(lista_vertices,elemento)
    lista_vertices_ordenada = sa.sort(lista_vertices, sort_infracciones_req5)
    lista_M_vertices = lt.subList(lista_vertices_ordenada, lt.size(lista_vertices_ordenada)-M, M)
    
    #uso del algoritmo de ruta mínima
    
    search = prim.PrimMST(grafo_distancia, lt.lastElement(lista_M_vertices)['vertex'])
    pila = lt.newList('ARRAY_LIST')
    distTo = search['distTo']
    edgeTo = search['edgeTo']
    return distTo'''
    '''for vertice_revision in lt.iterator(lista_M_vertices):
        camino = prim.edgesMST(search, vertice_revision['vertex'])
        lt.addLast(cola, camino)
    arcos_total = lt.newList('ARRAY_LIST')
    for vertice_revisión_cola in lt.iterator(cola):
        for caminito in lt.iterator(vertice_revisión_cola):
            if lt.isPresent(arcos_total,caminito) == 0:
                lt.addLast(arcos_total, caminito)
    return arcos_total'''
    pass
    
def req5(data_structs, cameras, vehicle, cost, count):
    """Función que soluciona el requerimiento 3"""
    # Realizar el requerimiento 3
    distance_graph = data_structs['graph_distance']
    req5 = data_structs['req5']
    
    count['included_vertices'] = st.newStack()
    
    vehiculo_vertices = req5[vehicle]['vertices']
    vehiculo_tickets = req5[vehicle]['tickets']

    most_tickets_queue = req5GetMostTickets(vehiculo_vertices, vehiculo_tickets, cameras)
    
    # version 1: Prim sencillo
    graph = gr.newGraph()
    req5MakeGraph(most_tickets_queue, graph, vehiculo_vertices)
    vertices = gr.vertices(graph)
    origin = lt.firstElement(vertices)
    mst = prim.PrimMST(graph)
    edges = prim.edgesMST(graph, mst)
    count['distance'] = prim.weightMST(graph, mst)
    count['cost'] = count['distance']*cost
    
    return edges, vertices, origin


def req5GetMostTickets(vehiculo_vertices, vehiculo_tickets, cameras):
    vertices_keylist = mp.keySet(vehiculo_vertices)
    for key in lt.iterator(vertices_keylist):
        entry = mp.get(vehiculo_vertices, key)
        vertex = me.getValue(entry)
        size = lt.size(vertex['tickets'])
        impq.insert(vehiculo_tickets, key, -size)
        
    most_tickets_queue = qu.newQueue()
    
    if impq.size(vehiculo_tickets) < cameras:
        for i in range(impq.size(vehiculo_tickets)):
            key = impq.min(vehiculo_tickets)
            qu.enqueue(most_tickets_queue, key)
            impq.delMin(vehiculo_tickets)
    else:
        for i in range(cameras):
            key = impq.min(vehiculo_tickets)
            qu.enqueue(most_tickets_queue, key)
            impq.delMin(vehiculo_tickets)
        
    return most_tickets_queue


def req5MakeGraph(most_tickets_queue, vehiculo_graph, vehiculo_vertices):
    while not qu.isEmpty(most_tickets_queue):
        vertex = int(qu.dequeue(most_tickets_queue))
        gr.insertVertex(vehiculo_graph, vertex)
    
    vertex_list = gr.vertices(vehiculo_graph)
    
    for vi_index in lt.iterator(vertex_list):
        entry = mp.get(vehiculo_vertices, vi_index)
        vi = me.getValue(entry)
        vi_lat = vi['coordinates']['lat']
        vi_long = vi['coordinates']['long']
        
        for vf_index in lt.iterator(vertex_list):
            if vi_index != vf_index:
                entry = mp.get(vehiculo_vertices, vf_index)
                vf = me.getValue(entry)
                vf_lat = vf['coordinates']['lat']
                vf_long = vf['coordinates']['long']
                
                distance = abs(haversineDistance(vi_lat, vf_lat, vi_long, vf_long))
                gr.addEdge(vehiculo_graph, vi_index, vf_index, distance)

            


# =============================================================================================================================================================================
# req6

def req6(data_structs, tickets, count):
    """
    Función que soluciona el requerimiento 6
    """
    # Realizar el requerimiento 6
    req6 = data_structs['req6']
    req6_stations = req6['stations']
    req6_subgraphs = req6['subgraphs']
    req6_tickets = req6['tickets']
    req6_queue = req6['queue']
    
    count['included_vertices'] = st.newStack()
        
    paths = mp.newMap(loadfactor=4)
    dijkstra_set = mp.newMap(loadfactor=4)
    
    temp_grav_stack = st.newStack()
    ticket_q = qu.newQueue()
    ticket_count = 0
    while ticket_count < tickets:
        current_gravity = mpq.min(req6_queue)
        
        gravity_entry = mp.get(req6_tickets, current_gravity)
        gravity_stack = me.getValue(gravity_entry)
        
        while not st.isEmpty(gravity_stack) and ticket_count < tickets:
            info = st.pop(gravity_stack)
            st.push(temp_grav_stack, info)
            info_index = info['index']
            lat = info['coordinates']['lat']
            long = info['coordinates']['long']
            gravedad = info['gravedad']
            closest_station = info['closest_station']
            
            entry = mp.get(req6_subgraphs, closest_station)
            station = me.getValue(entry)
            
            station_graph = station['graph']
            station_index = station['index']
            station_info = station['station']
            name = station_info['EPONOMBRE']
            
            
            if not mp.contains(dijkstra_set, station_index):
                search = djk.Dijkstra(station_graph, station_index)
                mp.put(dijkstra_set, station_index, search)
                
            entry = mp.get(dijkstra_set, station_index)
            search = me.getValue(entry)
            
            path_to = djk.pathTo(search, info_index)
            dist_to = djk.distTo(search, info_index)
            
            v = {'index':info_index,
                 'path':path_to,
                 'dist':dist_to,
                 'gravedad':gravedad,
                 'station':name}
            
            mp.put(paths, info_index, v)
            qu.enqueue(ticket_q, info_index)
            ticket_count += 1
            
        mpq.delMin(req6_queue)
    
    req6Requeue(temp_grav_stack, req6_queue, req6_tickets)
    
    return paths, ticket_q


def req6Requeue(temp_stack, req6_queue, req6_tickets):
    while not st.isEmpty(temp_stack):
        info = st.pop(temp_stack)
        grav = info['gravedad']
        gravity_entry = mp.get(req6_tickets, grav)
        gravity_stack = me.getValue(gravity_entry)
        
        st.push(gravity_stack, info)
        mpq.insert(req6_queue, grav)


# =============================================================================================================================================================================
# req7

def req7(data_structs, vi, vf, count):
    """
    Función que soluciona el requerimiento 7
    """
    # Realizar el requerimiento 7
    tickets_graph = data_structs['graph_tickets']
    vertices_tree = data_structs['vertex_tree']
    vertices_map = data_structs['vertex_map']
    
    vi_index = searchClosestVertex(vertices_tree, vi['lat'], vi['long'])
    vf_index = searchClosestVertex(vertices_tree, vf['lat'], vf['long'])
    
    '''
    paths = bf.BellmanFord(tickets_graph, vi_index)
    if not bf.hasPathTo(paths, vf_index):
        temp_stack = st.newStack()
    else:
        temp_stack = bf.pathTo(paths, vf_index)
        count['tickets'] = bf.distTo(paths, vf_index)
    '''
    paths = djk.Dijkstra(tickets_graph, vi_index)
    if not djk.hasPathTo(paths, vf_index):
        temp_stack = st.newStack()
    else:
        temp_stack = djk.pathTo(paths, vf_index)
        count['tickets'] = djk.distTo(paths, vf_index)
    
    
    path_size = st.size(temp_stack)
    path_q = st.newStack()
    i = 0
    prev = None
    while not st.isEmpty(temp_stack):
        ai = st.pop(temp_stack)
        qu.enqueue(path_q, ai)
        vi = ai['vertexA']
        if i == 0:
            entry = mp.get(vertices_map, vi)
            vi_info = me.getValue(entry)
            vilat = vi_info['coordinates']['lat']
            vilong = vi_info['coordinates']['long']
            
            if prev is None:
                prev = {'index':vi,
                        'coordinates':{'lat':vilat,
                                       'long':vilong}}
            else:
                vflat = prev['coordinates']['lat']
                vflong = prev['coordinates']['long']
                
                count['distance'] += abs(haversineDistance(vilat, vflat, vilong, vflong))
                
                prev = {'index':vi,
                        'coordinates':{'lat':vilat,
                                       'long':vilong}}
            i+=1
        elif i == path_size-1:
            vf = ai['vertexB']
            
            entry = mp.get(vertices_map, vi)
            vi_info = me.getValue(entry)
            vilat = vi_info['coordinates']['lat']
            vilong = vi_info['coordinates']['long']
            
            entry = mp.get(vertices_map, vf)
            vf_info = me.getValue(entry)
            vflat = vi_info['coordinates']['lat']
            vflong = vi_info['coordinates']['long']
            
            count['distance'] += abs(haversineDistance(vilat, vflat, vilong, vflong))
            
        else:
            i = 0   
    
    return path_q


# =============================================================================================================================================================================
# req8

def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Funciones utilizadas para comparar elementos dentro de una lista
# =============================================================================================================================================================================
# =============================================================================================================================================================================

def compareGraphs(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    # Crear función comparadora de la lista
    if data_1 == data_2['key']:
        return 0
    elif data_1 > data_2['key']:
        return 1
    else:
        return -1

def compareVertexLatitudeAndLongitude(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    # Crear función comparadora de la lista
    lat1 = data_1
    #lat1 = int(lat1[0]+lat1[1])
    lat2 = data_2
    #lat2 = int(lat2[0]+lat2[1])
    
    if (lat1 == lat2):
        return 0
    elif (lat1 > lat2):
        return 1
    else:
        return -1
    
def compareLocalidad(data1, data2):
    data1 = int(data1)
    data2 = int(data2['key'])
    
    if (data1 == data2):
        return 0
    elif (data1 > data2):
        return 1
    else:
        return -1
    
def compareTickets(data1, data2):
    data1 = data1.split(',')
    data2 = data2.split(',')
    
    data1_type = data1[0]
    data2_type = data1[1]
    
    if (data1_type == data2_type):
        return 0
    elif (data1_type > data2_type):
        return 1
    else:
        return -1
    
def getGravity(data): 
    newstr = ''
    for c in data:
        newstr += c
        newstr += '-'

    lst = newstr.split('-')
    data_iminpq = []
    for elem in lst:
        if elem != '':
            value = ord(elem)
            data_iminpq.append(-value)
    return data_iminpq

def compareGravity(data1, data2):
    
    data1 = data1.split('-')
    data2 = data2.split('-')

    if data1 != 'F':
        g1 = getGravity(data1[0])
    else:
        g1 = [-ord('F'), -ord('0'), -ord('0')]
        
    if data2 != 'F':
        g2 = getGravity(data2[0])
    else:
        g2 = [-ord('F'), -ord('0'), -ord('0')]
    
    if data1[1] == 'Público':
        v1 = -3
    elif data1[1] == 'Privado':
        v1 = -2
    elif data1[1] == 'Particular':
        v1 = -1
    else:
        v1 = 0
        
    if data2[1] == 'Público':
        v2 = -3
    elif data2[1] == 'Privado':
        v2 = -2
    elif data2[1] == 'Particular':
        v2 = -1
    else:
        v2 = 0 
        
    if v1 > v2:
        return 1
    elif v1 < v2:
        return -1
    elif g1 == g2:
        return 0
    elif g1 > g2:
        return 1
    elif g1 < g2:
        return -1

# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Funciones de ordenamiento
# =============================================================================================================================================================================
# =============================================================================================================================================================================

def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass