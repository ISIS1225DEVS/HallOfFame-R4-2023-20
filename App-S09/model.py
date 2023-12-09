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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import math
import folium
from folium.plugins import MarkerCluster
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
    #TODO: Inicializar las estructuras de datos
    data_structs = {
        'lst_comparendos': None,
        'lst_estaciones': None,
        'lst_vertices': None,
        'lst_arcos': None,
        'graph_distance': None,
        'graph_fee': None,
        'hashmap_vertex': None,
        'search': None,
        'localidades': None,
        'ordered_fees': None,
        'square_coords': None,
        'borders': {}
    }
    #Listas para la carga de datos
    data_structs['lst_comparendos'] = lt.newList('ARRAY_LIST')
    data_structs['lst_estaciones'] = lt.newList('ARRAY_LIST')
    data_structs['lst_vertices'] = lt.newList('ARRAY_LIST')
    data_structs['lst_arcos'] = lt.newList('ARRAY_LIST')
    #Grafos para buscar caminos
    data_structs['graph_distance'] = gr.newGraph('ADJ_LIST', directed=False, cmpfunction=compare_id, size=230000)
    data_structs['graph_fee'] = gr.newGraph('ADJ_LIST', directed=False, cmpfunction=compare_id, size=230000)
    #Tablas de hash para obtener la información
    data_structs['hashmap_vertex'] = mp.newMap(numelements=230000, maptype='PROBING', loadfactor=0.5, cmpfunction=compare_id)
    data_structs['graph_stations'] = mp.newMap(numelements=21, maptype='PROBING', loadfactor=0.5, cmpfunction=compare_id)
    data_structs['djk_stations'] = mp.newMap(numelements=21, maptype='PROBING', loadfactor=0.5, cmpfunction=compare_id)
    data_structs['localidades'] = mp.newMap(numelements=50, maptype='PROBING', loadfactor=0.5, cmpfunction=compare_id)
    #Lista con multas ordenadas por gravedad
    data_structs['ordered_fees'] = lt.newList('ARRAY_LIST')
    #Matriz para optimizar la búsqueda del más cercano
    data_structs['square_coords'] = mp.newMap(numelements=50000, maptype='PROBING', loadfactor=0.5, cmpfunction=compare_id)
    return data_structs


# Funciones para agregar informacion al modelo

def load_data(model, info):
    #Crear los vértices en ambos grafos
    add_vertex(model['graph_distance'], info)
    add_vertex(model['graph_fee'], info)
    #Crear el cuadro en la matriz con lat y long
    #load_matrix(model, info)

    #Añadir en ADT's auxiliares
    clos_station = closest_station(model, info['lat'], info['long'])
    info['closest_station'] = clos_station
    lt.addLast(model['lst_vertices'], info)
    mp.put(model['hashmap_vertex'], info['id'], info)
    subgraph = me.getValue(mp.get(model['graph_stations'], clos_station['EPONOMBRE']))
    add_vertex(subgraph, info)

def add_vertex(data_structs, info):
    contains = gr.containsVertex(data_structs, info['id']) 
    if not contains:
        gr.insertVertex(data_structs, info['id'])
    return data_structs

def load_matrix(data_structs, info):
    """
    Función para crear un cuadro de una matriz implementado en un mapa
    Args:
        data_structs: El modelo
        info: La información del vértice
    """
    matrix = data_structs['square_coords']
    lat = info['lat']
    long = info['long']
    name = calc_name_area(lat, long)
    entry = mp.get(matrix, name)
    if entry:
        lst = me.getValue(entry)
        lt.addLast(lst, info)
    else:
        lst = lt.newList('ARRAY_LIST')
        lt.addLast(lst, info)
        mp.put(matrix, name, lst)

def load_edges(data_structs, list_edges):
    """Función para añadir los arcos por distancia al grafo
    Args:
        data_structs: Modelo
        list_edges: Lista con los nodos adyacentes
    """
    adyacentes = []
    if len(list_edges) > 1:
        edge1 = list_edges[0]
        info_e1 = me.getValue(mp.get(data_structs['hashmap_vertex'], edge1))
        for i in range (1, len(list_edges)):
            edge2 = list_edges[i]
            lt.addLast(data_structs['lst_arcos'], {'vertexA': edge1, 'vertexB': edge2})
            adyacentes.append(edge2)
            info_e2 = me.getValue(mp.get(data_structs['hashmap_vertex'], edge2))
            lat1 = info_e1['lat']
            long1 = info_e1['long']
            lat2 = info_e2['lat']
            long2 = info_e2['long']
            distancy = calculate_distancy(lat1, long1, lat2, long2) * 1000
            add_edge(data_structs['graph_distance'], edge1, edge2, distancy)
            add_edge_stations(data_structs, info_e1, info_e2, distancy)
            fees1 = lt.size(info_e1['fees'])
            fees2 = lt.size(info_e2['fees'])
            weight = fees1 + fees2
            add_edge(data_structs['graph_fee'], edge1, edge2, weight)

    info = {
        'id': list_edges[0],
        'edges': adyacentes
    }

def add_edge_stations(model, infoe1, infoe2, distancy):
    if infoe1['closest_station']['EPONOMBRE'] == infoe2['closest_station']['EPONOMBRE']:
        subgraph = me.getValue(mp.get(model['graph_stations'], infoe1['closest_station']['EPONOMBRE']))
        add_edge(subgraph, infoe1['id'], infoe2['id'], distancy)

def add_edge(data_structs, e1, e2, weight):
    edge_entry = gr.getEdge(data_structs, e1, e2)
    if edge_entry is None:
        gr.addEdge(data_structs, e1, e2, weight)
    return data_structs

def stations_first(model, info):
    lt.addLast(model['lst_estaciones'], info)
    mp.put(model['graph_stations'], info['EPONOMBRE'], gr.newGraph(datastructure='ADJ_LIST', directed=False, cmpfunction=compare_id))

def calculate_distancy(lat, long, datalat, datalong):
    conversion = math.pi/180
    lat *= conversion
    datalat *= conversion
    long *= conversion
    datalong *= conversion
    
    dlat = (datalat) - lat
    dlong = datalong - long
    a = (math.sin(dlat/2))**2 + (math.cos(lat) * math.cos(datalat) * (math.sin(dlong/2))**2)
    c = 2 * math.asin(math.sqrt(a))
    d = 6371 * c
    return d

def add_fee(model, info):
    lt.addLast(model['lst_comparendos'], info)
    lt.addLast(model['ordered_fees'], info)
    info_vertex = me.getValue(mp.get(model['hashmap_vertex'], info['VERTICES']))
    lst_fees = info_vertex['fees']
    lt.addLast(lst_fees, info)
    entry = mp.get(model['localidades'], info['LOCALIDAD'])
    if entry:
        lst = me.getValue(entry)
        lt.addLast(lst, info)
    else:
        lst = lt.newList('ARRAY_LIST')
        lt.addLast(lst, info)
        mp.put(model['localidades'], info['LOCALIDAD'], lst)

def add_station(model, info):
    info_vertex = me.getValue(mp.get(model['hashmap_vertex'], info['VERTICES']))
    info_vertex['station'] = info
    mp.put(model['hashmap_vertex'], info_vertex['id'], info_vertex)

def closest_station(model, lat, long):
    stations = model['lst_estaciones']
    mindistance = math.inf
    infomin = None
    for s in lt.iterator(stations):
        slat = s['EPOLATITUD']
        slong = s['EPOLONGITU']
        distancy = calculate_distancy(slat, slong, lat, long) * 1000
        if distancy < mindistance:
            mindistance = distancy
            infomin = s
    return infomin


def calc_name_area(lat, long):
    """Funciión que calcula el nombre en el hash del cuadro en el que entra un comparendo en la matriz

    Args:
        lat (_type_): _description_
        long (_type_): _description_

    Returns:
        _type_: _description_
    """
    name_lat = str(math.floor(lat*2000))
    name_long = str(math.floor(long*2000))
    name = name_lat + '_' + name_long
    return name

def closest_vertex(model, info, lat, long, low, high):
    """Función que encuentra el vértice más cercano en la matriz recorriendo un cuadro 3x3 y si no
    encuentra nada amplía el rango recursivamente

    Args:
        model (): Modelo
        info (dict): Diccionario con la información del comparendo/estación
        lat (float): Latitud
        long (float): Longitud
        low (int): Casillas hacia la izquierda
        high (int): Casillas hacia la derecha + 1 (Porque el range es exclusivo en el final)

    Returns:
        infoclosest: La información del vértice más cercano
    """
    name = calc_name_area(lat, long)
    lstname = name.split('_')
    latname = int(lstname[0])
    longname = int(lstname[1])
    closest = math.inf
    infoclosest = None
    for i in range(low, high):
        namei = latname + i
        for j in range(low, high):
            if low == -1 or j == low or j == (high-1) or i == low or i == (high-1):
                namej = longname + j
                subname = str(namei) + '_' + str(namej)
                entry = mp.get(model['square_coords'], subname)
                if entry:
                    lst = me.getValue(entry)
                    for element in lt.iterator(lst):
                        distancy = calculate_distancy(lat, long, element['lat'], element['long'])
                        if distancy < closest:
                            closest = distancy
                            infoclosest = element
    if infoclosest == None:
        infoclosest, closest = closest_vertex(model, info, lat, long, low -1, high+1)
    return infoclosest, closest

def closest_vertice(model, lat, long):
    closest = math.inf
    closestinfo = None
    for vertex in lt.iterator(model['lst_vertices']):
        distancy = calculate_distancy(lat, long, vertex['lat'], vertex['long'])
        if distancy < closest:
            closest = distancy
            closestinfo = vertex
    return closestinfo

# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_first_last_five(list):
    """
    Retorna una lista con los tres primeros y tres últimos elementos
    """
    size = lt.size(list)
    if size <= 10:
        return list
    else:
        filtered = lt.newList("ARRAY_LIST")
        for i in range(1, 6):
            lt.addLast(filtered, lt.getElement(list, i))
        for i in range(size - 4, size + 1):
            lt.addLast(filtered, lt.getElement(list, i))

        return filtered

def get_first_last_three(list):
    """
    Retorna una lista con los tres primeros y tres últimos elementos
    """
    size = lt.size(list)
    if size <= 6:
        return list
    else:
        filtered = lt.newList("ARRAY_LIST")
        for i in range(1, 4):
            lt.addLast(filtered, lt.getElement(list, i))
        for i in range(size - 2, size + 1):
            lt.addLast(filtered, lt.getElement(list, i))

        return filtered

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(model, lat_origin, long_origin, lat_dest, long_dest, bono):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    graph = model['graph_distance']
    vertex_origin = closest_vertice(model, lat_origin, long_origin)
    vertex_dest = closest_vertice(model, lat_dest, long_dest)
    model['search'] = dfs.DepthFirstSearch(graph, vertex_origin['id'])
    haspath = dfs.hasPathTo(model['search'], vertex_dest['id'])
    total_distancy = 0
    total_vertex = 0
    path = lt.newList('ARRAY_LIST')
    list_bono = []
    prev_coords = []
    if haspath:
        model['search'] = dfs.pathTo(model['search'], vertex_dest['id'])
        prev = None
        for vertex in lt.iterator(model['search']):
            total_vertex += 1
            lt.addLast(path, {'vertices': vertex})
            if prev is not None:
                edge = gr.getEdge(graph, vertex, prev)
                weight = edge['weight']
                total_distancy += weight
            if bono:
                v_info = me.getValue(mp.get(model['hashmap_vertex'], vertex))
                lat = v_info['lat']
                long = v_info['long']
                info = [lat, long]
                if prev_coords != []:
                    double_coords = [prev_coords, info]
                    list_bono.append(double_coords)
                prev_coords = info
            prev = vertex
        if bono:
            req_8(model, list_bono, 1)
    return total_distancy, total_vertex, path


def req_2(model, lat_origin, long_origin, lat_dest, long_dest, bono):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    graph = model['graph_distance']
    vertex_origin = closest_vertice(model, lat_origin, long_origin)
    vertex_dest = closest_vertice(model, lat_dest, long_dest)
    model['search'] = bfs.BreathFirstSearch(graph, vertex_origin['id'])
    haspath = bfs.hasPathTo(model['search'], vertex_dest['id'])
    total_distancy = 0
    total_vertex = 0
    path = lt.newList('ARRAY_LIST')
    list_bono = []
    prev_coords = []
    if haspath:
        model['search'] = bfs.pathTo(model['search'], vertex_dest['id'])
        prev = None
        for vertex in lt.iterator(model['search']):
            total_vertex += 1
            lt.addLast(path, {'vertices': vertex})
            if prev is not None:
                edge = gr.getEdge(graph, vertex, prev)
                weight = edge['weight']
                total_distancy += weight
            if bono:
                v_info = me.getValue(mp.get(model['hashmap_vertex'], vertex))
                lat = v_info['lat']
                long = v_info['long']
                info = [lat, long]
                if prev_coords != []:
                    double_coords = [prev_coords, info]
                    list_bono.append(double_coords)
                prev_coords = info
            prev = vertex
        if bono:
            req_8(model, list_bono, 2)
    return total_distancy, total_vertex, path


def req_3(model, localidad, num_cam):
    """
    Función que soluciona el requerimiento 3
    """
    map_localidad = model["localidades"]
    parejas_localidad = mp.get(map_localidad, localidad)
    values_localidad = me.getValue(parejas_localidad)
    mapa_vertices = model["hashmap_vertex"]

    lista_vertices = lt.newList("ARRAY_LIST")
    for multa in lt.iterator(values_localidad):
        vertice = multa["VERTICES"]
        if not lt.isPresent(lista_vertices, vertice):
            lt.addLast(lista_vertices, vertice)

    lista_fees = lt.newList("ARRAY_LIST")
    mapa_vertices_info = mp.newMap(numelements=230000, maptype='PROBING', loadfactor=0.5, cmpfunction=compare_id)
    for vertice in lt.iterator(lista_vertices):
        num_fees = lt.size(me.getValue(mp.get(mapa_vertices, vertice))["fees"])
        info  = me.getValue(mp.get(mapa_vertices, vertice))
        lt.addLast(lista_fees, (vertice, num_fees))
        mp.put(mapa_vertices_info, vertice, info)

    merg.sort(lista_fees, cmp_fees)
    sub_n = lt.subList(lista_fees, 1, num_cam)
    origen = lt.getElement(sub_n, 1)

    dist = 0
    for i in range(1, lt.size(sub_n)):
        vertexA = lt.getElement(sub_n, i)[0]
        info_vertexA = me.getValue(mp.get(mapa_vertices_info, vertexA))
        lata = info_vertexA["lat"]
        longa = info_vertexA["long"]
        vertexB = lt.getElement(sub_n, i+1)[0]
        info_vertexB = me.getValue(mp.get(mapa_vertices_info, vertexB))
        latb = info_vertexB["lat"]
        longb = info_vertexB["long"]

        dist += calculate_distancy(lata, longa, latb, longb)

    return sub_n, dist


def req_4(model, camaras, bono):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    i = 2
    graph = model['graph_distance']
    sorted_list = model['ordered_fees']
    most_important = lt.firstElement(sorted_list)
    arcos = lt.newList('ARRAY_LIST')
    vertices = lt.newList('ARRAY_LIST')
    print('Cargando MST...')
    model['search'] = prim.PrimMST(graph, most_important['VERTICES'])
    weight = prim.weightMST(graph, model['search'])
    lst_bono = []
    cluster_bono = []
    infobono = {
        'lat': most_important['LATITUD'],
        'long': most_important['LONGITUD'],
        'info': most_important
    }
    cluster_bono.append(infobono)
    subgraph = gr.newGraph(datastructure='ADJ_LIST', directed=False, cmpfunction=compare_id)
    mst = model['search']['mst']
    print('Reconstruyendo grafo...')
    for minipath in lt.iterator(mst):
        add_vertex(subgraph, {'id': minipath['vertexA']})
        add_vertex(subgraph, {'id': minipath['vertexB']})
        add_edge(subgraph, minipath['vertexA'], minipath['vertexB'], minipath['weight'])
    subdjk = bfs.BreathFirstSearch(subgraph, most_important['VERTICES'])
    graph_cameras = gr.newGraph(datastructure='ADJ_LIST', directed=False, cmpfunction=compare_id)
    print('Filtrando las M cámaras')
    while i <= camaras:
        info_v = lt.getElement(sorted_list, i)
        infobono = {
            'lat': info_v['LATITUD'],
            'long': info_v['LONGITUD'],
            'info': info_v
        }
        cluster_bono.append(infobono)
        pathTo = bfs.pathTo(subdjk, info_v['VERTICES'])
        prev =None
        for vertex in lt.iterator(pathTo):
            if prev == None:
                lt.addLast(vertices, {'vertices': vertex})
                prev = vertex
            else:
                minipath = {
                    'vertexA': prev,
                    'vertexB': vertex,
                    'weight': 0
                }
                prev = vertex
                v1 = minipath['vertexA']
                v2 = minipath['vertexB']
                v_info1 = me.getValue(mp.get(model['hashmap_vertex'], v1))
                v_info2 = me.getValue(mp.get(model['hashmap_vertex'], v2))
                lat1 = v_info1['lat']
                long1 = v_info1['long']
                lat2 = v_info2['lat']
                long2 = v_info2['long']
                minipath['weight'] = calculate_distancy(lat1, long1, lat2,  long2)
                if not gr.getEdge(graph_cameras, minipath['vertexA'], minipath['vertexB']):
                    lt.addLast(arcos, minipath)
                    weight += minipath['weight']
                if not gr.containsVertex(graph_cameras, minipath['vertexA']):
                    lt.addLast(vertices, minipath['vertexA'])
                if not gr.containsVertex(graph_cameras, minipath['vertexB']):
                    lt.addLast(vertices, minipath['vertexB'])
                add_vertex(graph_cameras, {'id': minipath['vertexA']})
                add_vertex(graph_cameras, {'id': minipath['vertexB']})
                add_edge(graph_cameras, minipath['vertexA'], minipath['vertexB'], minipath['weight'])
                if bono:
                    lst_bono.append([[lat1, long1], [lat2, long2]])
        i += 1
    print('Cálculos finales...')
    if bono:
        req_8(model, lst_bono, 4, cluster_bono)
    return vertices, arcos, weight


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(model, comparendos, bono):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    i = 1
    lst_bono = []
    cluster_bono = []
    lst_pathTo = lt.newList('ARRAY_LIST')
    while i <= comparendos:
        print('Obteniendo camino de comparendo #' + str(i))
        info_comparendo = lt.getElement(model['ordered_fees'], i)
        if bono:
            infobono = {
                'lat': info_comparendo['LATITUD'],
                'long': info_comparendo['LONGITUD'],
                'info': info_comparendo
            }
            cluster_bono.append(infobono)
        vertex_comparendo = info_comparendo['VERTICES']
        info_vertex_comparendo = me.getValue(mp.get(model['hashmap_vertex'], vertex_comparendo))
        closest_station = info_vertex_comparendo['closest_station']
        entry = mp.get(model['djk_stations'], closest_station['EPONOMBRE'])
        if entry:
            search = me.getValue(entry)
        else:
            if bono:
                infobono = {
                    'lat': closest_station['EPOLATITUD'],
                    'long': closest_station['EPOLONGITU'],
                    'info': closest_station
                }
                cluster_bono.append(infobono)
            subgraph = me.getValue(mp.get(model['graph_stations'], closest_station['EPONOMBRE']))
            search = djk.Dijkstra(subgraph, closest_station['VERTICES'])
            mp.put(model['djk_stations'], closest_station['EPONOMBRE'], search)
        pathTo = djk.pathTo(search, info_comparendo['VERTICES'])
        info_path = {
            'station': closest_station['EPONOMBRE'],
            'fee': info_comparendo,
            'vertex_fee': vertex_comparendo,
            'total_vertex': 0,
            'identificadores': [],
            'arcos': lt.newList('ARRAY_LIST'),
            'km': 0
        }
        lt.addLast(lst_pathTo, info_path)
        if pathTo != None:
            for minipath in lt.iterator(pathTo):
                info_path['total_vertex'] += 1
                if len(info_path['identificadores']) == 0:
                    info_path['identificadores'].append(minipath['vertexA'])
                info_path['identificadores'].append(minipath['vertexB'])
                info_path['km'] += minipath['weight']
                lt.addLast(info_path['arcos'], minipath)
                if bono:
                    v1 = minipath['vertexA']
                    v2 = minipath['vertexB']
                    v_info1 = me.getValue(mp.get(model['hashmap_vertex'], v1))
                    v_info2 = me.getValue(mp.get(model['hashmap_vertex'], v2))
                    lat1 = v_info1['lat']
                    long1 = v_info1['long']
                    lat2 = v_info2['lat']
                    long2 = v_info2['long']
                    lst_bono.append([[lat1, long1], [lat2, long2]])
        i += 1
    if bono:
        req_8(model, lst_bono, 6, cluster_bono)
    return lst_pathTo


def req_7(model, lat_origin, long_origin, lat_dest, long_dest, bono):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    graph = model['graph_fee']
    vertex_origin = closest_vertice(model, lat_origin, long_origin)
    vertex_dest = closest_vertice(model, lat_dest, long_dest)
    model['search'] = djk.Dijkstra(graph, vertex_origin['id'])
    print('Ya se completó la búsqueda con BellmanFord')
    print('Ciclos negativos:')
    haspath = djk.hasPathTo(model['search'], vertex_dest['id'])
    print('Camino', haspath)
    total_fees = 0
    total_distancy = 0
    total_vertex = 0
    path = lt.newList('ARRAY_LIST')
    list_bono = []
    prev_coords = []
    if total_distancy==0:
        pathTo = djk.pathTo(model['search'], vertex_dest['id'])
        if pathTo == None:
            print('NONE MAMAWEBO')
        prev = None
        for vertex in lt.iterator(pathTo):
            total_vertex += 1
            lt.addLast(path, vertex)
            total_fees += vertex['weight']
            v1 = vertex['vertexA']
            v2 = vertex['vertexB']
            v_info1 = me.getValue(mp.get(model['hashmap_vertex'], v1))
            v_info2 = me.getValue(mp.get(model['hashmap_vertex'], v2))
            distance = calculate_distancy(v_info1['lat'], v_info1['long'], v_info2['lat'], v_info2['long'])
            total_distancy += distance
            if bono:
                lat1 = v_info1['lat']
                long1 = v_info1['long']
                lat2 = v_info2['lat']
                long2 = v_info2['long']
                list_bono.append([[lat1, long1], [lat2, long2]])
            prev = vertex
        if bono:
            req_8(model, list_bono, 7)
    else:
        print('No hay camino')
    return total_distancy, total_vertex, path
    


def req_8(data_structs, list, req, cluster=None):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    mapObj = folium.Map(location=[4.656184209192183, -74.10225554997007], zoom_start=12)
    str_name = 'Req ' + str(req) + ' Map.html'
    if req in [1, 2, 4, 6, 7]:
        for pair in list:
            folium.PolyLine(
                locations=pair,
                color='green',
                opacity=0.8
            ).add_to(mapObj)
    if cluster != None:
        mCluster = MarkerCluster(name='Markers').add_to(mapObj)
        for info in cluster:
            lat = info['lat']
            long = info['long']
            folium.Marker(location=[lat, long], popup=info['info']).add_to(mCluster)
    folium.LayerControl().add_to(mapObj)
    mapObj.save(str_name)


# Funciones utilizadas para comparar elementos dentro de una lista

def compare_id(data1, data2):
    if data1 > me.getKey(data2):
        return 1
    elif data1 < me.getKey(data2):
        return -1
    else:
        return 0

# Funciones de ordenamiento


def sort_num_fees(v1, v2):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    size_v1 = lt.size(v1['fees'])
    size_v2 = lt.size(v2['fees'])
    if size_v1 > size_v2:
        return True
    else:
        return False

def sort_fees(f1, f2):
    priority = {
        'Diplomatico': 4,
        'Oficial': 3,
        'Público': 2,
        'Particular': 1
    }
    if f1['INFRACCION'] in (None, '', ' ', 'Unknown') or f2['INFRACCION'] in (None, '', ' ', 'Unknown'):
        return False
    letter1 = f1['INFRACCION'][0]
    letter2 = f2['INFRACCION'][0]
    cod1 = int(f1['INFRACCION'].replace(letter1, ''))
    cod2 = int(f2['INFRACCION'].replace(letter2, ''))
    type1 = priority.get(f1['TIPO_SERVICIO'], 0)
    type2 = priority.get(f2['TIPO_SERVICIO'], 0)
    if type1 > type2:
        return True
    elif type1 < type2:
        return False
    else:
        if letter1 > letter2:
            return True
        elif letter1 < letter2:
            return False
        else:
            if cod1 > cod2:
                return True
            else:
                return False

def cmp_fees(v1,v2):
    if v1[1] > v2[1]:
        return True
    else:
        return False
