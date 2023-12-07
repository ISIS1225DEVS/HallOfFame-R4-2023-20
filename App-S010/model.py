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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import edge as e
from math import radians, cos, sin, asin, sqrt
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
    data_structs={
        "grafo_km": gr.newGraph(),
        "grafo_com":gr.newGraph(),
        "hash_map_num_loc": mp.newMap(maptype='CHAINING'),
        "hash_map_comparendos": mp.newMap(maptype='CHAINING'),
        "hash_map_estaciones": mp.newMap(maptype='CHAINING'),
        "hash_map_localides_comparendos": mp.newMap(maptype='CHAINING'),
        "lista_comparendos_grave": lt.newList(datastructure='ARRAY_LIST')
    }
    return data_structs


# Funciones para agregar informacion al modelo

def add_vertice(data_structs, vertice):
    """
    Función para agregar nuevos elementos a la lista
    """
    if gr.containsVertex(data_structs["grafo_km"],vertice) == False:
        gr.insertVertex(data_structs["grafo_km"],vertice)
    if gr.containsVertex(data_structs["grafo_com"],vertice) == False:
        gr.insertVertex(data_structs["grafo_com"],vertice)
    return gr.numVertices(data_structs["grafo_km"])


def add_arcos(data_structs, arco):
        arco_list = arco.split(' ')
        v_origen = arco_list[0]
        llv_coords_origen = mp.get(data_structs["hash_map_num_loc"], v_origen)
        coords_origen = me.getValue(llv_coords_origen)
        
        longitud_org = float(coords_origen[0])
        latitud_org = float(coords_origen[1])


        num_c_origen = 0
        if mp.contains(data_structs["hash_map_comparendos"], v_origen):
            llv_comparendos = mp.get(data_structs["hash_map_comparendos"], v_origen)
            lista = me.getValue(llv_comparendos)
            num_c_origen = lt.size(lista)
            
        for v_destino in arco_list:
            num_c_destino = 0
            if mp.contains(data_structs["hash_map_comparendos"], v_destino):
                llv_comparendos = mp.get(data_structs["hash_map_comparendos"], v_destino)
                lista = me.getValue(llv_comparendos)
                num_c_destino = lt.size(lista)
            peso_com = num_c_origen + num_c_destino
            gr.addEdge(data_structs['grafo_com'], v_origen, v_destino, peso_com)

            llv_coords_des = mp.get(data_structs["hash_map_num_loc"], v_destino)
            coords_des = me.getValue(llv_coords_des)

            longitud_des = float(coords_des[0])
            latitud_des = float(coords_des[1])

            dist = haversine(longitud_org, latitud_org, longitud_des, latitud_des)

            gr.addEdge(data_structs['grafo_km'], v_origen, v_destino, dist)



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


def req_1(data_structs, punto_origen_lat, punto_origen_lon, punto_destino_lat, punto_destino_lon):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1

    coords_origen = (punto_origen_lat, punto_origen_lon, data_structs)
    coords_destino = (punto_destino_lat, punto_destino_lon, data_structs)
    lista_ver = gr.vertices(data_structs['grafo_km'])
    mas_cercano_origen = encontrar_mas_cercano(lista_ver, coords_origen, data_structs)
    mas_cercano_destino = encontrar_mas_cercano(lista_ver, coords_destino, data_structs)
    print(mas_cercano_origen)
    print(mas_cercano_destino)
    BFS = bfs.BreathFirstSearch(data_structs['grafo_km'], mas_cercano_origen)
    if bfs.hasPathTo(BFS, mas_cercano_destino):
        camino = bfs.pathTo(BFS, mas_cercano_destino)
        dist = 0
        lista_nodos_camino = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(lista_nodos_camino, mas_cercano_destino)
        i = 1
        while st.isEmpty(camino) == False:
            nodo = st.pop(camino)
            lt.addLast(lista_nodos_camino, nodo)
        nodo1 = lt.getElement(lista_nodos_camino, 1)
        for nodo in lt.iterator(lista_nodos_camino):
            if nodo1 != nodo:
                edge = gr.getEdge(data_structs['grafo_km'], nodo1, nodo)
                nodo1 = nodo
                if edge != None:
                    dist += edge['weight']
    return dist, lt.size(lista_nodos_camino), lista_nodos_camino

def encontrar_mas_cercano(lista_ver, coordenadas, data_structs):
    cercano = None
    dist_min = float('inf')
    for vertice in lt.iterator(lista_ver):
        llv_cords_vertice = mp.get(data_structs['hash_map_num_loc'], vertice)
        coords_vertice = me.getValue(llv_cords_vertice)
        dist_nuevo_vert = haversine(float(coordenadas[1]), float(coordenadas[0]), float(coords_vertice[0]), float(coords_vertice[1]))
        if dist_nuevo_vert < dist_min:
            dist_min = dist_nuevo_vert
            cercano = vertice
    return cercano


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs, localidad, cantidad_cams):


    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    llv_mapa_vertices = mp.get(data_structs['hash_map_localides_comparendos'], localidad)
    mapa_vertices_localidad = me.getValue(llv_mapa_vertices)
    lista_vertices_valor = lt.newList(datastructure='ARRAY_LIST')
    key_set = mp.keySet(mapa_vertices_localidad)
    for key in lt.iterator(key_set):
        llv_lista_comparendos_vertice = mp.get(mapa_vertices_localidad, key)
        lista_comparendos_vertice = me.getValue(llv_lista_comparendos_vertice)
        num_comparendos = lt.size(lista_comparendos_vertice)
        lt.addLast(lista_vertices_valor, (key, num_comparendos))
    merg.sort(lista_vertices_valor, sort_tuple_mayor_menor)
    m_mayores = lt.subList(lista_vertices_valor, 1, cantidad_cams)
    print('ENTRE A PRIM')
    MST = prim.PrimMST(data_structs['grafo_km'], lt.getElement(m_mayores, 1)[0])
    print('SALI DE PRIM')
    map_edgeto = MST['edgeTo']
    map_distto = MST['distTo']

    lista_vertices = set()
    lista_arcos = lt.newList(datastructure='ARRAY_LIST')
    dist_total = 0


    for pos_vertice in range(2, lt.size(m_mayores)):
        vertice = lt.getElement(m_mayores, pos_vertice)
        vertice_a_buscar = vertice[0]
        while vertice_a_buscar != lt.getElement(m_mayores, 1)[0]:
            vertice_string = str(vertice_a_buscar)
            llv_camino_a = mp.get(map_edgeto, vertice_string)
            camino_a = me.getValue(llv_camino_a)
            lista_vertices.add(camino_a['vertexA'])
            lista_vertices.add(camino_a['vertexB'])
            llv_costo_a = mp.get(map_distto, str(vertice_a_buscar))
            costo_a = me.getValue(llv_costo_a)

            tupla_camino = (camino_a['vertexA'], camino_a['vertexB'])
            if lt.isPresent(lista_arcos, tupla_camino) == False:
                lt.addLast(lista_arcos, tupla_camino)
                dist_total += float(costo_a)
        
            vertice_a_buscar = e.other(camino_a, vertice_a_buscar)
    return len(lista_vertices), lista_vertices, lista_arcos, dist_total

    
def sort_tuple_mayor_menor(v1, v2):
    if v1[1] > v2[1]:
        return True
    else:
        return False
    
    

def req_4(data_structs, cantidad_cams):
    """
    Función que soluciona el requerimiento 4
    """
    comp_ordenados=data_structs['lista_comparendos_grave']
    m_mayores = lt.subList(comp_ordenados, 1, cantidad_cams)
    merg.sort(m_mayores, sort_tuple_mayor_menor)
    print("Iniciando Árbol de Expansión Mínima... \n")
    MST = prim.PrimMST(data_structs['grafo_km'], lt.getElement(m_mayores, 1)[0])
    map_edgeto = MST['edgeTo']
    map_distto = MST['distTo']
    lista_vertices = set()
    lista_arcos = lt.newList(datastructure='ARRAY_LIST')
    dist_total = 0

    for pos_vertice in range(2, lt.size(m_mayores)):
        vertice = lt.getElement(m_mayores, pos_vertice)
        vertice_a_buscar = vertice[0]
        while vertice_a_buscar != lt.getElement(m_mayores, 1)[0]:
            vertice_string = str(vertice_a_buscar)
            llv_camino_a = mp.get(map_edgeto, vertice_string)
            camino_a = me.getValue(llv_camino_a)
            lista_vertices.add(camino_a['vertexA'])
            lista_vertices.add(camino_a['vertexB'])
            llv_costo_a = mp.get(map_distto, str(vertice_a_buscar))
            costo_a = me.getValue(llv_costo_a)

            tupla_camino = (camino_a['vertexA'], camino_a['vertexB'])
            if lt.isPresent(lista_arcos, tupla_camino) == False:
                lt.addLast(lista_arcos, tupla_camino)
                dist_total += float(costo_a)
        
            vertice_a_buscar = e.other(camino_a, vertice_a_buscar)
    return len(lista_vertices), lista_vertices, lista_arcos, dist_total


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs, num_comparendos_graves):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    sublista = lt.subList(data_structs['lista_comparendos_grave'], 1, num_comparendos_graves)
    keyset = mp.keySet(data_structs['hash_map_estaciones'])
    mapa_comp_est = mp.newMap(maptype='CHAINING')
    for comparendo in lt.iterator(sublista):
        search = djk.Dijkstra(data_structs['grafo_km'], comparendo[0])
        mejor =  float('inf')
        path = None
        vertices_camino = set()
        arcos_camino = set()
        for estacion_vertice in lt.iterator(keyset):
            if djk.hasPathTo(search, estacion_vertice) and float(djk.distTo(search, estacion_vertice)) < float(mejor):
                mejor = estacion_vertice
                path = djk.pathTo(search, estacion_vertice)
                distancia = djk.distTo(search, estacion_vertice)
        dicc = {'mejor_vert_est': mejor, 'distancia_estacion': distancia, 'vertices': path}
        for camino in lt.iterator(dicc['vertices']):
            vertices_camino.add(camino['vertexA'])
            vertices_camino.add(camino['vertexB'])
            arco = (camino['vertexA'], camino['vertexB'])
            arcos_camino.add(arco)
        dicc['vertices'] = vertices_camino
        dicc['arcos'] = arcos_camino
        mp.put(mapa_comp_est, comparendo[0], dicc)
    return mapa_comp_est



def req_7(data_structs, punto_origen_lat, punto_origen_lon, punto_destino_lat, punto_destino_lon):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    coords_origen = (punto_origen_lat, punto_origen_lon, data_structs)
    coords_destino = (punto_destino_lat, punto_destino_lon, data_structs)
    lista_ver = gr.vertices(data_structs['grafo_com'])
    mas_cercano_origen = encontrar_mas_cercano(lista_ver, coords_origen, data_structs)
    mas_cercano_destino = encontrar_mas_cercano(lista_ver, coords_destino, data_structs)
    search = djk.Dijkstra(data_structs['grafo_com'], mas_cercano_origen)
    if djk.hasPathTo(search, mas_cercano_destino):
        camino = djk.pathTo(search, mas_cercano_destino)
        cant_comparendos = djk.distTo(search, mas_cercano_destino)
        dist_km = 0
        lista_arcos = lt.newList(datastructure='ARRAY_LIST')
        lista_vertices = lt.newList(datastructure='ARRAY_LIST')
        while st.isEmpty(camino) == False:
            arco = st.pop(camino)
            lt.addLast(lista_arcos, arco)
            vertex_a = arco['vertexA']
            vertex_b = arco['vertexB']
            if lt.isPresent(lista_vertices, vertex_a) == False:
                lt.addLast(lista_vertices, vertex_a)
            if lt.isPresent(lista_vertices, vertex_b) == False:
                lt.addLast(lista_vertices, vertex_b)
            edge_km = gr.getEdge(data_structs['grafo_km'], vertex_a, vertex_b)
            dist_km += edge_km
        return lt.size(lista_vertices), lista_vertices, lista_arcos, cant_comparendos, dist_km
    else:
        print('No hay camino')




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


def sort_comparendos_mas_graves(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    merg.sort(data_structs['lista_comparendos_grave'], sort_crit_grave)

def sort_crit_grave(v1, v2):
    lista = ['Diplomatico', 'Público', 'Oficial', 'Particular', '-', 'Field was not enabled']
    if v1[1] == v2[1]:
        if v2[2][0] < v1[2][0]:
            return True
        elif v2[2][0] > v1[2][0]:
            return False
        else:
            if len(str(v2[2])) > 1 and len(str(v1[2])) > 1:
                if int(v2[2][1:]) > int(v1[2][1:]):
                    return True
                else:
                    return False
            elif len(str(v2[2])) == len(str(v1[2])):
                return False
    elif lista.index(v1[1]) < lista.index(v2[1]):
        return False
    else:
        return True


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r
