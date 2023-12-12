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
import math

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
    model = {
        "bogota": None,
        "carga": None,
        "info": None,
        "localidad": None,
        "primeros_v": None,
        "ultimos_v": None,
        "primeros_c": None,
        "ultimos_c": None,
        "primeros_e": None,
        "ultimos_e": None,
        "estaciones": None
             }
    model["bogota"] = gr.newGraph(size=228050)
    model["carga"] = mp.newMap(numelements=228050)
    model["info"] = mp.newMap()
    model["localidad"] = mp.newMap()
    model["grafo_comparendos"] = gr.newGraph(directed=False, size=228050)
    model["primeros_v"] = lt.newList("ARRAY_LIST")
    model["ultimos_v"] = qu.newQueue()
    model["primeros_c"] = lt.newList("ARRAY_LIST")
    model["ultimos_c"] = qu.newQueue()
    model["primeros_e"] = lt.newList("ARRAY_LIST")
    model["ultimos_e"] = qu.newQueue()
    model["estaciones"] = lt.newList("ARRAY_LIST")
    return model


# Funciones para agregar informacion al modelo
    
def add_vertex(data_structs, vertex):
    """
    Función para agregar nuevos elementos a la lista
    """
    gr.insertVertex(data_structs["bogota"], vertex[0])
    coordenadas = (float(vertex[1]), float(vertex[2]))
    comparendos = lt.newList("ARRAY_LIST")
    estaciones = lt.newList("ARRAY_LIST")
    mapa = mp.newMap(numelements=3)
    mp.put(mapa, "coordenadas", coordenadas)
    mp.put(mapa, "comparendos", comparendos)
    mp.put(mapa, "estaciones", estaciones)
    mp.put(mapa, "id", vertex[0])
    mp.put(data_structs["info"], vertex[0], mapa)
    if lt.size(data_structs["primeros_v"]) < 5:
        lt.addLast(data_structs["primeros_v"], vertex)
        
    if qu.size(data_structs["ultimos_v"]) < 5:
        qu.enqueue(data_structs["ultimos_v"], vertex)
    else:
        qu.enqueue(data_structs["ultimos_v"], vertex)
        qu.dequeue(data_structs["ultimos_v"])

def cargar_comparendo(data, comparendo):
    vertice = comparendo["VERTICES"]
    lista = mp.get(mp.get(data["info"], vertice)["value"], "comparendos")["value"]
    lt.addLast(lista, comparendo)
    
    if mp.contains(data["localidad"], comparendo["LOCALIDAD"]):
        lista = mp.get(data["localidad"], comparendo["LOCALIDAD"])["value"]
        lt.addLast(lista, vertice)
    else:
        lista = lt.newList("ARRAY_LIST")
        lt.addLast(lista, vertice)
        mp.put(data["localidad"], comparendo["LOCALIDAD"], lista)
        
    if lt.size(data["primeros_c"]) < 5:
        lt.addLast(data["primeros_c"], comparendo)
        
    if qu.size(data["ultimos_c"]) < 5:
        qu.enqueue(data["ultimos_c"], comparendo)
    else:
        qu.enqueue(data["ultimos_c"], comparendo)
        qu.dequeue(data["ultimos_c"])
    
def cargar_estacion(data, estacion):
    vertice = estacion["VERTICES"]
    lista = mp.get(mp.get(data["info"], vertice)["value"], "estaciones")["value"]
    lt.addLast(lista, estacion)
    
    if lt.size(data["primeros_e"]) < 5:
        lt.addLast(data["primeros_e"], estacion)
        
    if qu.size(data["ultimos_e"]) < 5:
        qu.enqueue(data["ultimos_e"], estacion)
    else:
        qu.enqueue(data["ultimos_e"], estacion)
        qu.dequeue(data["ultimos_e"])
    lt.addLast(data["estaciones"], estacion)

def agregar_arco(data, arco):
    i = 1
    coord_1 = mp.get(mp.get(data["info"], arco[0])["value"], "coordenadas")["value"]
    comparendos_1 = lt.size(mp.get(mp.get(data["info"], arco[0])["value"], "comparendos")["value"])
    while i < len(arco):
        coord_2 = mp.get(mp.get(data["info"], arco[i])["value"], "coordenadas")["value"]
        distancia = 2 * math.asin(math.sqrt((math.sin( (coord_1[1] - coord_2[1]) * math.pi / 360 ) ** 2) + math.cos(coord_2[1] * math.pi / 180) * math.cos(coord_1[1] * math.pi / 180) * (math.sin( (coord_1[0] - coord_2[0]) * math.pi / 360 ) ** 2) )) * 6371
        comparendos = lt.size(mp.get(mp.get(data["info"], arco[i])["value"], "comparendos")["value"]) + comparendos_1
        gr.addEdge(data["bogota"], arco[0], arco[i], distancia)
        gr.addEdge(data["grafo_comparendos"],arco[0], arco[i], comparendos)
        i += 1
        
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


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

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


def req_1(model, latO, longO, latD, longD):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    
    totalV = 0
    totalD = 0 
    hashmap = model["info"]
    listahash = mp.valueSet(hashmap)
    
    sVertex = verticeCercano(listahash, latO, longO)
    eVertex = verticeCercano(listahash, latD, longD)
    bfsResult = bfs.BreathFirstSearch(model["bogota"], sVertex)
    totalV = 0 
    
    
    if bfs.hasPathTo(bfsResult, eVertex):
            
            path = bfs.pathTo(bfsResult, eVertex)

            
            path_list = list(lt.iterator(path))

            camino = path_list
            
    totalV = len(path_list)
    totalD = calcularDistanciaEnCamino(hashmap, camino)
    
    
    
    return camino, totalD, totalV

def verticeCercano(data, latO, longO):
    minDist = float('inf')
    nVert = None

    for submapa in lt.iterator(data):
        coordenadas = me.getValue(mp.get(submapa, 'coordenadas'))
        lat = coordenadas[1]
        long = coordenadas[0]
        distance = calculate_distancy(lat, long, latO, longO)
        
        if distance < minDist:
            minDist = distance
            nVert = me.getValue(mp.get(submapa, "id"))

    return nVert

def calcularDistanciaEnCamino(graph, path_list):
    """
    Retorna la distancia total en un camino. 
    IMPORTANTE: la el camino debe ser una lista.
    """
    tDistancia = 0.0

    for i in range(len(path_list) - 1):
        vertex1 = path_list[i]
        vertex2 = path_list[i + 1]
        zz = me.getValue(mp.get(graph, vertex1))
        yy = me.getValue(mp.get(graph, vertex2))
        coordinates1 = me.getValue(mp.get(zz, 'coordenadas'))
        coordinates2 = me.getValue(mp.get(yy, 'coordenadas'))

        lat1, lon1 = coordinates1[1], coordinates1[0]
        lat2, lon2 = coordinates2[1], coordinates2[0]

        distancia = calculate_distancy(lat1, lon1, lat2, lon2)
        tDistancia += distancia

    return tDistancia


def req_2(model, latO, longO, latD, longD):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    
    totalV = 0
    totalD = 0 
    hashmap = model["info"]
    listahash = mp.valueSet(hashmap)
    
    sVertex = verticeCercano(listahash, latO, longO)
    eVertex = verticeCercano(listahash, latD, longD)
    djResult = djk.Dijkstra(model["bogota"], sVertex)
    totalV = 0 
    
    
    if djk.hasPathTo(djResult, eVertex):
            
            path = djk.pathTo(djResult, eVertex)

            
            path_list = list(lt.iterator(path))

            camino = path_list
            
            
    totalV = len(path_list)
    
    for arco in camino:
        totalD += float(arco["weight"])
    nCamino = []    
    for arco in camino: 
        if not(arco["vertexA"] in nCamino):
            
            nCamino.append(arco["vertexA"])
        if not(arco["vertexB"] in nCamino):
            
            nCamino.append(arco["vertexB"])
    #totalD = calcularDistanciaEnCamino(hashmap, camino)
    
    #print(camino)
    
    return nCamino, totalD, totalV
    
    pass

def sort_heap(data_1, data_2):
    return data_1 < data_2

def req_3(data, n, localidad):
    """
    Función que soluciona el requerimiento 3
    """
    vertices = mp.get(data["localidad"], localidad)["value"]
    n_vertices = mpq.newMinPQ(sort_heap)
    
    for vertice in lt.iterator(vertices):
        comparendos = lt.size(mp.get(mp.get(data["info"], vertice)["value"], "comparendos")["value"])
        if mpq.size(n_vertices) < n:
            mpq.insert(n_vertices, (vertice, comparendos))
        elif comparendos > mpq.min(n_vertices)[1]:
            mpq.delMin(n_vertices)
            mpq.insert(n_vertices, (vertice, comparendos))
    
    source = mpq.delMin(n_vertices)[0]
    busqueda = djk.Dijkstra(data["bogota"], source)
    vertices_red = lt.newList("ARRAY_LIST")
    arcos_red = lt.newList("ARRAY_LIST")
    distance = 0
    lt.addLast(vertices_red, source)
    
    for element in range(n - 1):
        vertex = mpq.delMin(n_vertices)
        lt.addLast(vertices_red, vertex)
        path_to = djk.pathTo(busqueda, vertex)
        
        d_anterior = 0
        v_anterior = vertex
        for v in lt.iterator(path_to):
            if not lt.isPresent(vertices_red, v):
                d = djk.distTo(busqueda, v)
                distance += d - d_anterior
                lt.addLast(vertices_red, v)
                lt.addLast(arcos_red, v_anterior + "-" + v)
            d_anterior = d
            v_anterior = v
    costo = distance * 1000000
    total_v = lt.size(vertices_red)
    if total_v > 10:
        grupos_v = lt.newList("ARRAY_LIST")
        for i in range(1, total_v + 1, 10):
            final = i + 10
            if final > total_v:
                rango = lt.subList(vertices_red, i, total_v % 10)
            else:
                rango = lt.subList(vertices_red, i, final)
        lt.addLast(grupos_v, rango)
    else:
        grupos_v = lt.newList("ARRAY_LIST")
        lt.addLast(grupos_v, rango)
    return grupos_v, arcos_red, distance, costo, total_v


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass



def comparar_por_gravedad(elemento1, elemento2):
    
    gravedad = {'Público': 3, 'Oficial': 2, 'Particular': 1}
    gravedad1 = gravedad[elemento1['TIPO_SERVICIO']] 
    global_id1 = elemento1['INFRACCION']
    gravedad2 = gravedad[elemento2['TIPO_SERVICIO']] 
    global_id2 = elemento2['INFRACCION']

    if gravedad1 == gravedad2:
        return global_id1 < global_id2
        
    return gravedad1 < gravedad2
def req_6(data, n):
    listas = mp.keySet(data["localidad"])
    n_vertices = mpq.newMinPQ(comparar_por_gravedad)
    
    for localidad in lt.iterator(listas):
        vertices = mp.get(data["localidad"], localidad)["value"]
        for vertice in lt.iterator(vertices):
            comparendos = mp.get(mp.get(data["info"], vertice)["value"], "comparendos")["value"]
            for comparendo in lt.iterator(comparendos):
                if mpq.size(n_vertices) < n:
                    mpq.insert(n_vertices, comparendo)
                else:
                    mpq.insert(n_vertices, comparendo)
                    mpq.delMin(n_vertices)
    mas_graves = lt.newList("ARRAY_LIST")
    for i in range(n):
        lt.addLast(mas_graves, mpq.delMin(n_vertices))
    min_d = None
    estacion_c = None
    for estacion in lt.iterator(data["estaciones"]):
        for comparendo in lt.iterator(mas_graves):
            d = calculate_distancy(estacion["EPOLATITUD"], estacion["EPOLONGITU"], comparendo["LATITUD"], comparendo["LONGITUD"])
            if min_d is None:
                min_d = d
                estacion_c = estacion
            else:
                if d < min_d:
                    min_d = d
                    estacion_c = estacion
    
    source = estacion_c["VERTICES"]
    busqueda = djk.Dijkstra(data["bogota"], source)
    vertices_red = lt.newList("ARRAY_LIST")
    arcos_red = lt.newList("ARRAY_LIST")
    distance = 0
    lt.addLast(vertices_red, source)
    
    for element in range(n - 1):
        vertex = mpq.delMin(n_vertices)
        lt.addLast(vertices_red, vertex)
        path_to = djk.pathTo(busqueda, vertex)
        
        d_anterior = 0
        v_anterior = vertex
        for v in lt.iterator(path_to):
            if not lt.isPresent(vertices_red, v):
                d = djk.distTo(busqueda, v)
                distance += d - d_anterior
                lt.addLast(vertices_red, v)
                lt.addLast(arcos_red, v_anterior + "-" + v)
            d_anterior = d
            v_anterior = v
    
    total_v = lt.size(vertices_red)
    if total_v > 10:
        grupos_v = lt.newList("ARRAY_LIST")
        for i in range(1, total_v + 1, 10):
            final = i + 10
            if final > total_v:
                rango = lt.subList(vertices_red, i, total_v % 10)
            else:
                rango = lt.subList(vertices_red, i, final)
        lt.addLast(grupos_v, rango)
    else:
        grupos_v = lt.newList("ARRAY_LIST")
        lt.addLast(grupos_v, rango)
    return total_v, grupos_v, arcos_red, distance
                
        


def req_7(model, lato, longo, latd, longd):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    grafo = model["grafo_comparendos"]
    hashmap = model["info"]
    listahash = mp.valueSet(hashmap)
    distancia_origen = math.inf
    info_cercano_origen = None
    camino = []
    for submapa in lt.iterator(listahash):
        coordenadas = me.getValue(mp.get(submapa, 'coordenadas'))
        lat = coordenadas[1]
        long = coordenadas[0]
        distancy1 = calculate_distancy(lat, long, lato, longo)
        if distancy1 < distancia_origen:
            distancia_origen = distancy1
            info_cercano_origen = submapa
    distancia_destino = math.inf
    info_cercano_destino = None
    for submapa in lt.iterator(listahash):
        coordenadas = me.getValue(mp.get(submapa, 'coordenadas'))
        lat = coordenadas[1]
        long = coordenadas[0]
        distancy2 = calculate_distancy(lat, long, latd, longd)
        if distancy2 < distancia_destino:
            distancia_destino = distancy2
            info_cercano_destino = submapa

    origen = me.getValue(mp.get(info_cercano_origen, "id"))
    destino = me.getValue(mp.get(info_cercano_destino, "id"))
    print('Origen:', origen, '. Destino:', destino)
    search = djk.Dijkstra(grafo, origen)
    haspath = djk.hasPathTo(search, destino)
    print(haspath)
    if haspath:
        pathTo = djk.pathTo(search, destino)
        for minipath in lt.iterator(pathTo):
            if camino == []:
                camino.append(minipath['vertexA'])
            camino.append(minipath['vertexB'])
            
    return camino


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


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
