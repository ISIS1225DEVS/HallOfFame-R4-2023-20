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
    lt.addLast(data_structs['lst_arcos'], info)

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


def req_1(model, lat_origin, long_origin, lat_dest, long_dest):
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
    if haspath:
        model['search'] = dfs.pathTo(model['search'], vertex_dest['id'])
        prev = None
        for vertex in lt.iterator(model['search']):
            total_vertex += 1
            lt.addLast(path, vertex)
            if prev is not None:
                edge = gr.getEdge(graph, vertex, prev)
                weight = edge['weight']
                total_distancy += weight
            prev = vertex
    return total_distancy, total_vertex, path


def req_2(model, lat_origin, long_origin, lat_dest, long_dest):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    graph = model['graph_distance']
    vertex_origin = closest_vertice(model, lat_origin, long_origin)
    vertex_dest = closest_vertice(model, lat_dest, long_dest)
    model['search'] = bfs.BreadhtFisrtSearch(graph, vertex_origin['id'])
    haspath = bfs.hasPathTo(model['search'], vertex_dest['id'])
    total_distancy = 0
    total_vertex = 0
    path = lt.newList('ARRAY_LIST')
    if haspath:
        model['search'] = bfs.pathTo(model['search'], vertex_dest['id'])
        prev = None
        for vertex in lt.iterator(model['search']):
            total_vertex += 1
            lt.addLast(path, vertex)
            if prev is not None:
                edge = gr.getEdge(graph, vertex, prev)
                weight = edge['weight']
                total_distancy += weight
            prev = vertex

    return total_distancy, total_vertex, path
    pass


def req_3(dataStructs, M, locality):
    filtered = lt.newList('ARRAY_LIST')
    graph = dataStructs['graph_distance']
    map_auxiliar = mp.newMap(maptype='CHAINING')
    llaves = []
    llaves2 = []
    vertices = 0
    vertini = None
    entry = mp.get(dataStructs['localidades'], locality)
    if entry:
        facto = me.getValue(entry)
        if facto != None:
            for i in lt.iterator(facto):
                if vertini == None:
                    vertini = i['VERTICES']
                else:
                    factores = mp.contains(map_auxiliar, i['VERTICES'])
                    if factores:
                        contador_acci = mp.get(map_auxiliar, i['VERTICES'])
                        contador_acci = me.getValue(contador_acci)
                        contador_acci[i['VERTICES']] += 1
                        vertices += 1
                    else:
                        mp.put(map_auxiliar, i['VERTICES'],  {i['VERTICES'] : 0}) 
                        llaves.append(i['VERTICES'])
                        contador_acci = mp.get(map_auxiliar, i['VERTICES'])
                        contador_acci = me.getValue(contador_acci)
                        contador_acci[i['VERTICES']] += 1
                        vertices += 1
            cosas = None   
            siuuu = []  
            for cosas in llaves:
                if cosas == None:
                    vertini = cosas
                final = mp.get(map_auxiliar, cosas)
                final = me.getValue(final)
                lt.addLast(filtered, final)
                siuuu.append(final)
            lista_ordenada = sorted(siuuu, key=lambda x: list(x.values())[0])
    lista_volteada = list(reversed(lista_ordenada))
    i = M
    listafinal= []
    while i > 0:
        for respi in lista_volteada:
            a  =  respi.keys()
            if vertini != None:
                vertini = respi.keys()
            llaves = respi.keys()
            listafinal.append(llaves)
            i -= 1
    vertfinal = listafinal[M]
    dataStructs['search'] = bfs.BreadhtFisrtSearch(graph, vertini)
    haspath = bfs.hasPathTo(dataStructs['search'], vertfinal)
    path = lt.newList('ARRAY_LIST')
    total_distancy = 0

    if haspath:
        dataStructs['search'] = dfs.pathTo(dataStructs['search'], vertfinal)
        prev = None
        for vertex in lt.iterator(dataStructs['search']):
            lt.addLast(path, vertex)
            if prev is not None:
                edge = gr.getEdge(graph, vertex, prev)
                weight = edge['weight']
                total_distancy += weight
    return total_distancy, vertices
 #   print(llaves2)
   # sorted(llaves2['VERTICES'])
   # print(llaves2)

def req_4(model, m):
    """
    Función que soluciona el requerimiento 4
    """
    faltas = model['localidades']
    
    grafo = None
    if mp.size(faltas["TIPO_SERVICIO"]) == m:
        
        grafo = mp.keySet(faltas["TIPO_SERVICIO"])
    elif mp.size(faltas["TIPO_SERVICIO"]) < m: 
        grafo = lt.newList("ARRAY_LIST")
        i = 1
        llaves = mp.keySet(faltas["TIPO_SERVICIO"])
        while i <= m:
            lt.addLast(grafo, llaves)
            i += 1
            comparendos = lt.newList("ARRAY_LIST")
            size = lt.size(comparendos)
            z = faltas["TIPO_SERVICIO"]
    elif i <= size and z == "Particular":

            comparendos = lt.getElement(comparendos,i)
            
            x = mp.get(grafo, comparendos)
            
            if x == size: 
                z = "Publico"
                i = 0
            i+=1
            
    elif i <= size and z == "publico":
                
            comparendos = lt.getElement(comparendos,i)
            
            x = mp.get(grafo, comparendos)
            
            if x == size: 
                z = "completado"
                i = 0
            i+=1
        
    return comparendos

def req_5(control, camaras, vehiculo):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    graph = control['graph_distance']
    miedo = control['ordered_fees']
    llaves = []
    datos = 0
    lits_aux = lt.newList('ARRAY_LIST')
    vertex = mp.newMap(maptype='CHAINING')
    for clase_v in lt.iterator(miedo):
        if clase_v['CLASE_VEHICULO'] == vehiculo:
            lt.addLast(lits_aux, clase_v)
            facto = mp.contains(vertex, clase_v['VERTICES'])
            if not facto:
                mp.put(vertex, clase_v['VERTICES'], 0)
                vertices = mp.get(vertex, clase_v['VERTICES'])
                datos = me.getValue(vertices)
                datos += 1
                llaves.append(clase_v['VERTICES'])
                cantidad_vertices += 1
            else:
                vertices = mp.get(vertex, clase_v['VERTICES'])
                datos = me.getValue(vertices)
                datos += 1
    lista_aux = []
    for verticcees in llaves:
        cosa = mp.get(vertex, verticcees)
        cosa = me.getValue(cosa)
        print(verticcees)
        lista_aux.append({verticcees: cosa})
    lista_ordenada = sorted(lista_aux, key=lambda x: list(x.values())[0])
    lista_ordenada = list(reversed(lista_ordenada))
    momento = camaras
    llaves_final = []
    vertini = None
    while momento >= 0:
        for u in lista_ordenada:
            vertini = u.keys()
            llaves_final.append(vertini)
            momento -= 1
    vertfinal = llaves_final[camaras]
    control['search'] = bfs.BreadhtFisrtSearch(graph, vertini)
    haspath = bfs.hasPathTo(control['search'], vertfinal)
    path = lt.newList('ARRAY_LIST')
    total_distancy = 0

    if haspath:
        control['search'] = dfs.pathTo(control['search'], vertfinal)
        prev = None
        for vertex in lt.iterator(control['search']):
            lt.addLast(path, vertex)
            if prev is not None:
                edge = gr.getEdge(graph, vertex, prev)
                weight = edge['weight']
                total_distancy += weight
    return total_distancy, datos



def req_6(model, comparendos):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    i = 1
    lst_pathTo = lt.newList('ARRAY_LIST')
    while i <= comparendos:
        print('Obteniendo camino de comparendo #' + str(i))
        info_comparendo = lt.getElement(model['ordered_fees'], i)
        vertex_comparendo = info_comparendo['VERTICES']
        info_vertex_comparendo = me.getValue(mp.get(model['hashmap_vertex'], vertex_comparendo))
        closest_station = info_vertex_comparendo['closest_station']
        entry = mp.get(model['djk_stations'], closest_station['EPONOMBRE'])
        if entry:
            search = me.getValue(entry)
        else:
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
            'arcos': [],
            'km': 0
        }
        lt.addLast(lst_pathTo, info_path)
        for minipath in lt.iterator(pathTo):
            info_path['total_vertex'] += 1
            if len(info_path['identificadores']) == 0:
                info_path['identificadores'].append(minipath['vertexA'])
            info_path['identificadores'].append(minipath['vertexB'])
            info_path['km'] += minipath['weight']
            info_path['arcos'].append(minipath)
            
        i += 1
    return lst_pathTo


def req_7(model, lat_origin, long_origin, lat_dest, long_dest):
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
    if total_distancy==0:
        pathTo = djk.pathTo(model['search'], vertex_dest['id'])
        if pathTo == None:
            print('NONE MAMAWEBO')
        prev = None
        for vertex in lt.iterator(pathTo):
            total_vertex += 1
            if prev == None:
                lt.addLast(path, vertex['vertexA'])
            lt.addLast(path, vertex['vertexB'])
            total_fees += vertex['weight']
            v1 = vertex['vertexA']
            v2 = vertex['vertexB']
            v_info1 = me.getValue(mp.get(model['hashmap_vertex'], v1))
            v_info2 = me.getValue(mp.get(model['hashmap_vertex'], v2))
            distance = calculate_distancy(v_info1['lat'], v_info1['long'], v_info2['lat'], v_info2['long'])
            total_distancy += distance
            prev = vertex
    else:
        print('No hay camino')
    return total_distancy, total_vertex, path

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
        'Diplomatico': 1,
        'Oficial': 3,
        'Público': 4,
        'Particular': 2
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





def sort (dicc):
    diccionario_ordenado = dict(sorted(dicc.items(), key=lambda x: int(x[0]), reverse=True))
    return diccionario_ordenado