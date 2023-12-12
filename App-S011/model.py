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
import sys

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import edge as ed
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
    #TOD: Inicializar las estructuras de datos
    analyzer = {
        "map_comparendos": None,
        "map_arcos": None,
        "map_geo": None,
        "malla_vial_com_dis": None,
        "map_div_long":None,
        "lst_comparendos":None,
        "lst_estaciones": None,
        "lst_vertices":None,
        "recorrido_sobre_el_grafo":None,
        "grafo_req_7":None,
        "comparendos_gravedad": None
    }


    analyzer["comparendos_gravedad"] = om.newMap(omaptype="RBT", cmpfunction=compareGravedad)
    analyzer["comparendos_gravedad_2"] = om.newMap(omaptype="RBT", cmpfunction=compareGravedad2)
    analyzer["comparendos_vehiculo"] = mp.newMap(numelements=100, maptype="PROBING")
    analyzer["comparendos_localidad"] = mp.newMap(numelements=150, maptype="PROBING")


    # key: Vertice | value:[{comparendos: info, estaciones: info}]
    analyzer['map_comparendos_estaciones'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     cmpfunction=compareStopIds)
    
    # key: Arcos (1-2)== (2-1) |  value: {dist: None, estaciones: None} 
    """analyzer['map_arcos'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     cmpfunction=compareStopIds)"""
    # mapa geolocalizacion
    analyzer['map_geo'] = mp.newMap(numelements=14000)
    # mapa seccionado por longitudes para agilizar busqueda
    # key: 4.1234| value:vertices

    """analyzer["map_div_long"]= mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     cmpfunction=compareStopIds)"""
    


    # grafo por comparendo o distancia como peso
    analyzer['malla_vial_dis'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000)
    analyzer['malla_vial_comp'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              cmpfunction=compareStopIds)
    
    #lista_comparendos
    analyzer["lst_comparendos"] = lt.newList()
    #lista_estaciones
    analyzer["lst_estaciones"] = lt. newList()
    #lista vertices
    analyzer["lst_vertices"]= lt.newList()
    

    return analyzer



# Funciones para agregar informacion al modelo

def add_vertice(analyzer,vertice):
    if not gr.containsVertex(analyzer["malla_vial_dis"],vertice["id"]):
        gr.insertVertex(analyzer["malla_vial_dis"], vertice["id"])
        
    id = vertice["id"]
    dict_geo= {"longitud": vertice["longitud"] , "latitud": vertice["latitud"]}
    mp.put(analyzer["map_geo"],id, dict_geo)

    lt.addLast(analyzer["lst_vertices"],vertice)


    return analyzer


def addEstacion(analyzer, estacion):

    vertice_cercano = estacion["VERTICES"]
 
    if mp.contains(analyzer["map_comparendos_estaciones"], vertice_cercano):
        lt.addLast(mp.get(analyzer["map_comparendos_estaciones"],vertice_cercano)["value"]["estacion"], estacion)
        
    else:
        dict_comparendos_estaciones= {"estacion": lt.newList(), "comparendo": lt.newList()}
        mp.put(analyzer["map_comparendos_estaciones"],vertice_cercano, dict_comparendos_estaciones )
        lt.addLast(mp.get(analyzer["map_comparendos_estaciones"],vertice_cercano)["value"]["estacion"], estacion)

    lt.addLast(analyzer["lst_estaciones"], estacion)
  
    return analyzer

def addComparendo(analyzer, comparendo):
    vertice_cercano = comparendo["VERTICES"]
 
    if mp.contains(analyzer["map_comparendos_estaciones"], vertice_cercano):
        lt.addLast(mp.get(analyzer["map_comparendos_estaciones"],vertice_cercano)["value"]["comparendo"], comparendo)
        
    else:
        dict_comparendos_estaciones= {"estacion": lt.newList(), "comparendo": lt.newList()}
        mp.put(analyzer["map_comparendos_estaciones"],vertice_cercano, dict_comparendos_estaciones )
        lt.addLast(mp.get(analyzer["map_comparendos_estaciones"],vertice_cercano)["value"]["comparendo"], comparendo)

    llave_gravedad = {"tipo": comparendo["TIPO_SERVICIO"], "codigo": comparendo["INFRACCION"]}

    entry = om.get(analyzer["comparendos_gravedad"], llave_gravedad)
    entry2 = om.get(analyzer["comparendos_gravedad_2"], llave_gravedad)

    if entry is None:
        lst = lt.newList()
        lst2 = lt.newList()
        lt.addLast(lst, comparendo)
        lt.addLast(lst2, comparendo)
        om.put(analyzer["comparendos_gravedad"], llave_gravedad, lst)
        om.put(analyzer["comparendos_gravedad_2"], llave_gravedad, lst2)
    else:
        lst = me.getValue(entry)
        lt.addLast(lst, comparendo)
        lst2 = me.getValue(entry2)
        lt.addLast(lst2, comparendo)

    entry = mp.get(analyzer["comparendos_localidad"], comparendo["LOCALIDAD"])

    if entry is None:
        mapa = mp.newMap(20000, maptype="PROBING")
        mp.put(mapa, vertice_cercano, 1)
        mp.put(analyzer["comparendos_localidad"], comparendo["LOCALIDAD"], mapa)
    else:
        mapa = me.getValue(entry)
        e = mp.get(mapa, vertice_cercano)
        actual = 0 if e is None else me.getValue(e)
        mp.put(mapa, vertice_cercano, actual + 1)

    entry = mp.get(analyzer["comparendos_vehiculo"], comparendo["CLASE_VEHICULO"])

    if entry is None:
        mapa = mp.newMap(20000, maptype="PROBING")
        mp.put(mapa, vertice_cercano, 1)
        mp.put(analyzer["comparendos_vehiculo"], comparendo["CLASE_VEHICULO"], mapa)
    else:
        mapa = me.getValue(entry)
        e = mp.get(mapa, vertice_cercano)
        actual = 0 if e is None else me.getValue(e)
        mp.put(mapa, vertice_cercano, actual + 1)

    lt.addLast(analyzer["lst_comparendos"], comparendo)
    
    return analyzer



def addArco(analyzer, id,x ):
    """
    Adiciona un arco entre dos estaciones
    """
    #meter peso y crear arco
    long1= mp.get(analyzer["map_geo"],id)["value"]["longitud"]
    lati1= mp.get(analyzer["map_geo"],id)["value"]["latitud"]
    long2= mp.get(analyzer["map_geo"],x)["value"]["longitud"]
    lati2= mp.get(analyzer["map_geo"],x)["value"]["latitud"]
    distancia= haversine_distance(long1, lati1, long2, lati2)

    edge = gr.getEdge(analyzer["malla_vial_dis"],id, x)
    if edge is None:
        gr.addEdge(analyzer["malla_vial_dis"],id,x,distancia)
   
    return analyzer





# Funciones para creacion de datos
def printData(analyzer):
    len_estacioines=lt.size(analyzer["lst_estaciones"])
    primerasEstaciones= lt.subList(analyzer["lst_estaciones"],1,5)
    ultimasEstaciones= lt.subList(analyzer["lst_estaciones"],len_estacioines-4,5)
    len_comparendos= lt.size(analyzer["lst_comparendos"])
    primerosComparendos= lt.subList(analyzer["lst_comparendos"],1,5)
    ultimasComparendos= lt.subList(analyzer["lst_comparendos"],len_comparendos-4,5)

    

    res=[len_estacioines, primerasEstaciones,ultimasEstaciones,len_comparendos,primerosComparendos,ultimasComparendos ]

    return res





def req_1(analyzer,longI,latiI, longDes, latitudDes):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1

    #Hallar el vertice mas cercano a ini
    distancia_menorIni=999999
    id_menorIni=None
    for x in lt.iterator(analyzer["lst_vertices"]):
        distancia_Ini= haversine_distance(longI, latiI, x["longitud"],x["latitud"])
        if distancia_Ini< distancia_menorIni:
            distancia_menorIni=distancia_Ini
            id_menorIni= x["id"]


    #Hallar el vertice mas cercano a ini
    distancia_menorDest=999999
    id_menorDest=None
    for x in lt.iterator(analyzer["lst_vertices"]):
        distancia_Dest= haversine_distance(longDes, latitudDes, x["longitud"],x["latitud"])
        if distancia_Dest< distancia_menorDest:
            distancia_menorDest=distancia_Dest
            id_menorDest= x["id"]

    # Hago una estructura con el recorrido del grafo
    
    #analyzer['recorrido_sobre_el_grafo'] = dfs.DepthFirstSearch(analyzer["malla_vial_dis"],id_menorIni)
    analyzer['recorrido_sobre_el_grafo'] = bfs.BreathFirstSearch(analyzer['malla_vial_dis'], id_menorIni)

    # Encuentro un camino
    #resp= dfs.pathTo(analyzer['recorrido_sobre_el_grafo'],id_menorDest)
    resp= bfs.pathTo(analyzer['recorrido_sobre_el_grafo'],id_menorDest)
    data=[haversine_distance(longI, latiI,longDes, latitudDes), lt.size(resp), resp]
    return data





def req_2(analyzer,longI,latiI, longDes, latitudDes):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    distancia_menorIni=999999
    id_menorIni=None
    for x in lt.iterator(analyzer["lst_vertices"]):
        distancia_Ini= haversine_distance(longI, latiI, x["longitud"],x["latitud"])
        if distancia_Ini< distancia_menorIni:
            distancia_menorIni=distancia_Ini
            id_menorIni= x["id"]


    #Hallar el vertice mas cercano a ini
    distancia_menorDest=999999
    id_menorDest=None
    for x in lt.iterator(analyzer["lst_vertices"]):
        distancia_Dest= haversine_distance(longDes, latitudDes, x["longitud"],x["latitud"])
        if distancia_Dest< distancia_menorDest:
            distancia_menorDest=distancia_Dest
            id_menorDest= x["id"]

    # Hago una estructura con el recorrido del grafo
    
    #analyzer['recorrido_sobre_el_grafo'] = dfs.DepthFirstSearch(analyzer["malla_vial_dis"],id_menorIni)
    analyzer['recorrido_sobre_el_grafo'] = bfs.BreathFirstSearch(analyzer['malla_vial_dis'], id_menorIni)

    # Encuentro un camino
    #resp= dfs.pathTo(analyzer['recorrido_sobre_el_grafo'],id_menorDest)
    resp= bfs.pathTo(analyzer['recorrido_sobre_el_grafo'],id_menorDest)
    data=[haversine_distance(longI, latiI,longDes, latitudDes), lt.size(resp), resp]
    return data

def req_3(data_structs, localidad, m):
    """
    Función que soluciona el requerimiento 3
    """
    comparendos = mp.get(data_structs["comparendos_localidad"], localidad.upper())

    if comparendos is None:
        return None
    comparendos = me.getValue(comparendos)

    cantidadComparendos = lt.newList(datastructure="ARRAY_LIST")

    for comparendo in lt.iterator(mp.keySet(comparendos)):
        lt.addLast(cantidadComparendos, {"vertice": comparendo, "cantidad": mp.get(comparendos, comparendo)["value"]})

    merg.sort(cantidadComparendos, ordenar_cantidad)

    seleccionados = cantidadComparendos
    if lt.size(cantidadComparendos) > m:
        seleccionados = lt.subList(cantidadComparendos, 1, m)

    verticesSeleccionados = lt.newList(datastructure="ARRAY_LIST")

    for v in lt.iterator(seleccionados):
        lt.addLast(verticesSeleccionados, int(v["vertice"]))

    print("CREANDO RED...")
    red, kms = crear_red(data_structs, verticesSeleccionados)

    return verticesSeleccionados, gr.vertices(red), gr.edges(red), kms, kms * 1000000


def bfsSencillo(analyzer, desde, hasta, cola = qu.newQueue(datastructure="SINGLE_LINKED"), prev = mp.newMap(numelements=14000)):
    """
    Aplica BFS para encontrar un posible camino más corto entre los vertices desde y hasta.
    Una vez encuentra el camino, detiene la busqueda y lo retorna.
    """

    if qu.isEmpty(cola):
        qu.enqueue(cola, desde)
        mp.put(prev, desde, -1)

    while not qu.isEmpty(cola):
        if mp.contains(prev, hasta):
            break

        cabeza = qu.dequeue(cola)
        vecinos = gr.adjacents(analyzer["malla_vial_dis"], cabeza)

        for vecino in lt.iterator(vecinos):
            if not mp.contains(prev, vecino):
                mp.put(prev, vecino, cabeza)
                qu.enqueue(cola, vecino)


    # NO existe un camino
    if not mp.contains(prev, hasta):
        print(f"Camino desde {desde} hasta {hasta} NO encontrado", file=sys.stderr)
        return None, -1, cola, prev

    caminoVertices = lt.newList(datastructure="ARRAY_LIST")
    actual = {"value": hasta}

    while actual is not None:
        lt.addLast(caminoVertices, actual["value"])
        actual = mp.get(prev, actual["value"])

    lt.removeLast(caminoVertices)

    camino = lt.newList(datastructure="SINGLE_LINKED")
    distancia = 0

    for v in range(lt.size(caminoVertices), 1, -1):
        a = lt.getElement(caminoVertices, v)
        b = lt.getElement(caminoVertices, v - 1)
        arco = gr.getEdge(analyzer["malla_vial_dis"], a, b)
        distancia += ed.weight(arco)
        lt.addFirst(camino, arco)

    return camino, distancia, cola, prev


def crear_red(data_structs, verticesSeleccionados):
    red = gr.newGraph()
    kms = 0

    for numVertice in range(1, lt.size(verticesSeleccionados)):
        verticeActual = lt.getElement(verticesSeleccionados, numVertice)
        siguiente = lt.getElement(verticesSeleccionados, numVertice + 1)

        caminoActual, distanciaActual, busqueda, mapa = bfsSencillo(data_structs, siguiente, verticeActual)

        if not lt.isEmpty(gr.vertices(red)):
            for vertice in lt.iterator(gr.vertices(red)):
                camino, distancia, busqueda, mapa = bfsSencillo(data_structs, siguiente, vertice, cola=busqueda,
                                                                prev=mapa)
                if distancia < distanciaActual:
                    caminoActual = camino
                    distanciaActual = distancia

        for arco in lt.iterator(caminoActual):
            desde = ed.either(arco)
            hasta = ed.other(arco, desde)
            dist = ed.weight(arco)
            kms += dist
            if not gr.containsVertex(red, desde):
                gr.insertVertex(red, desde)
            if not gr.containsVertex(red, hasta):
                gr.insertVertex(red, hasta)
            gr.addEdge(red, desde, hasta, dist)

    return red, kms


def req_4(data_structs, m):
    comparendos = om.valueSet(data_structs["comparendos_gravedad"])

    seleccionados = mp.newMap(numelements=m, maptype="PROBING")

    for lstComparendos in lt.iterator(comparendos):
        for comparendo in lt.iterator(lstComparendos):
            mp.put(seleccionados, int(comparendo["VERTICES"]), comparendo)
            if mp.size(seleccionados) == m: break
        if mp.size(seleccionados) == m: break

    vS = mp.keySet(seleccionados)
    verticesSeleccionados = lt.newList(datastructure="ARRAY_LIST")

    for vertice in lt.iterator(vS):
        lt.addLast(verticesSeleccionados, vertice)

    print("CREANDO RED...")
    red, kms = crear_red(data_structs, verticesSeleccionados)

    # Vertices identificados, vertices utilizados para la conexión, arcos utilizados, kms, precio
    return verticesSeleccionados, gr.vertices(red), gr.edges(red), kms, kms * 1000000



def req_5(data_structs, m, vehiculo):
    comparendos = mp.get(data_structs["comparendos_vehiculo"], vehiculo.upper())

    if comparendos is None:
        return None
    comparendos = me.getValue(comparendos)

    cantidadComparendos = lt.newList(datastructure="ARRAY_LIST")

    for comparendo in lt.iterator(mp.keySet(comparendos)):
        lt.addLast(cantidadComparendos, {"vertice": comparendo, "cantidad": mp.get(comparendos, comparendo)["value"]})

    merg.sort(cantidadComparendos, ordenar_cantidad)

    seleccionados = cantidadComparendos
    if lt.size(cantidadComparendos) > m:
        seleccionados = lt.subList(cantidadComparendos, 1, m)

    verticesSeleccionados = lt.newList(datastructure="ARRAY_LIST")

    for v in lt.iterator(seleccionados):
        lt.addLast(verticesSeleccionados, int(v["vertice"]))

    print("CREANDO RED...")
    red, kms = crear_red(data_structs, verticesSeleccionados)

    return verticesSeleccionados, gr.vertices(red), gr.edges(red), kms, kms * 1000000




def req_6(data_structs, m): #
    comparendos = om.valueSet(data_structs["comparendos_gravedad_2"]) # Criterio distinto

    seleccionados = mp.newMap(numelements=m, maptype="PROBING")

    for lstComparendos in lt.iterator(comparendos):
        for comparendo in lt.iterator(lstComparendos):
            mp.put(seleccionados, int(comparendo["VERTICES"]), comparendo)
            if mp.size(seleccionados) == m: break
        if mp.size(seleccionados) == m: break

    vS = mp.keySet(seleccionados)
    caminosComparendos = lt.newList(datastructure="ARRAY_LIST")

    posicion_estaciones = {}

    for vertice in lt.iterator(vS):
        infoVertice = mp.get(data_structs["map_geo"], vertice)["value"]
        estacionCercana = None
        estacionDist = math.inf
        for estacion in lt.iterator(data_structs["lst_estaciones"]):
            posicionEstacion = posicion_estaciones.get(estacion["OBJECTID"], int(estacion["VERTICES"]))
            verticeEstacion = mp.get(data_structs["map_geo"], posicionEstacion)["value"]
            dist = haversine_distance(infoVertice["longitud"], infoVertice["latitud"], verticeEstacion["longitud"], verticeEstacion["latitud"])
            if dist < estacionDist:
                estacionCercana = estacion
        posicionEstacion = posicion_estaciones.get(estacionCercana["OBJECTID"], int(estacionCercana["VERTICES"]))
        posicion_estaciones[estacionCercana["OBJECTID"]] = vertice

        camino, distancia, _, _ = bfsSencillo(data_structs, posicionEstacion, vertice)

        info = {"estacion": estacionCercana["OBJECTID"], "atendiendo": vertice, "desde": posicionEstacion, "camino": camino, "distancia": distancia}

        lt.addLast(caminosComparendos, info)

    return caminosComparendos


def req_7(analyzer):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    print(analyzer["lst_vertices"])

    """if not gr.containsVertex(analyzer["malla_vial_comp"],  ):
        gr.insertVertex(analyzer["malla_vial_comp"], vertice["id"])"""
    """comparendos = om.valueSet(analyzer["comparendos_gravedad_2"]) # Criterio distinto

    seleccionados = mp.newMap(numelements=m, maptype="PROBING")

    for lstComparendos in lt.iterator(comparendos):
        for comparendo in lt.iterator(lstComparendos):
            mp.put(seleccionados, int(comparendo["VERTICES"]), comparendo)
            if mp.size(seleccionados) == m: break
        if mp.size(seleccionados) == m: break

    vS = mp.keySet(seleccionados)
    caminosComparendos = lt.newList(datastructure="ARRAY_LIST")

    posicion_estaciones = {}"""
    """if not gr.containsVertex(analyzer["malla_vial_comp"],  ):
        gr.insertVertex(analyzer["malla_vial_comp"], vertice["id"])"""
    
    """for vertice in lt.iterator(vS):
        infoVertice = mp.get(analyzer["map_geo"], vertice)["value"]
        estacionCercana = None
        estacionDist = math.inf
        for estacion in lt.iterator(analyzer["lst_estaciones"]):
            posicionEstacion = posicion_estaciones.get(estacion["OBJECTID"], int(estacion["VERTICES"]))
            verticeEstacion = mp.get(analyzer["map_geo"], posicionEstacion)["value"]
            dist = haversine_distance(infoVertice["longitud"], infoVertice["latitud"], verticeEstacion["longitud"], verticeEstacion["latitud"])
            if dist < estacionDist:
                estacionCercana = estacion
        posicionEstacion = posicion_estaciones.get(estacionCercana["OBJECTID"], int(estacionCercana["VERTICES"]))
        posicion_estaciones[estacionCercana["OBJECTID"]] = vertice"""


    pass


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

def ordenar_cantidad(data_1, data_2):
    return data_2["cantidad"] < data_1["cantidad"]



def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareGravedad(comparendo1, comparendo2):
    tipo_servicio = {
        "Diplomatico": 4,
        "Oficial": 3,
        "Público": 2,
        "Particular": 1
    }

    tipo1 = tipo_servicio.get(comparendo1["tipo"], None)
    tipo2 = tipo_servicio.get(comparendo2["tipo"], None)

    if tipo1 is None and tipo2 is None:
        codigo1 = comparendo1["codigo"]
        codigo2 = comparendo2["codigo"]

        if codigo1 < codigo2:
            return -1
        elif codigo1 > codigo2:
            return 1
        else:
            return 0
    if tipo1 is None:
        return 1
    if tipo2 is None:
        return -1

    if tipo1 > tipo2:
        return -1
    elif tipo1 < tipo2:
        return 1
    else:
        codigo1 = comparendo1["codigo"]
        codigo2 = comparendo2["codigo"]

        if codigo1 < codigo2:
            return -1
        elif codigo1 > codigo2:
            return 1
        else:
            return 0

def compareGravedad2(comparendo1, comparendo2):
    tipo_servicio = {
        "Diplomatico": 4,
        "Público": 3,
        "Oficial": 2,
        "Particular": 1
    }

    tipo1 = tipo_servicio.get(comparendo1["tipo"], None)
    tipo2 = tipo_servicio.get(comparendo2["tipo"], None)

    if tipo1 is None and tipo2 is None:
        codigo1 = comparendo1["codigo"]
        codigo2 = comparendo2["codigo"]

        if codigo1 < codigo2:
            return -1
        elif codigo1 > codigo2:
            return 1
        else:
            return 0
    if tipo1 is None:
        return 1
    if tipo2 is None:
        return -1

    if tipo1 > tipo2:
        return -1
    elif tipo1 < tipo2:
        return 1
    else:
        codigo1 = comparendo1["codigo"]
        codigo2 = comparendo2["codigo"]

        if codigo1 < codigo2:
            return -1
        elif codigo1 > codigo2:
            return 1
        else:
            return 0



def MENOR_MAYOR(mag1, mag2):
    if (mag1 == mag2):
        return 0
    elif (mag1 < mag2):
        return 1
    else:
        return -1


def haversine_distance(long1, lati1, long2, lati2):
    
    r = 6371.0
    
    long1_rad = math.radians(long1)
    lati1_rad = math.radians(lati1)
    long2_rad = math.radians(long2)
    lati2_rad = math.radians(lati2)
    dlong = long2_rad - long1_rad
    dlati = lati2_rad - lati1_rad
    
    a = math.sin(dlati/2)**2 + math.cos(lati1_rad) * math.cos(lati2_rad) * math.sin(dlong/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    distance = r * c
    
    return distance
