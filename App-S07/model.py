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
import folium
import config as cf
import math
import time as t
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
from DISClib.Utils import error as error
assert cf
from tabulate import tabulate as tb

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
    analyzer = {}

    analyzer['intersections'] = mp.newMap(numelements=500000,
                                          maptype='PROBING',
                                          cmpfunction=compareIntersectionIds)
    
    analyzer['coordinates'] = mp.newMap(numelements=500000,
                                          maptype='PROBING',
                                          cmpfunction=compareIntersectionIds)
    
    analyzer['localities'] = mp.newMap(numelements=500000,
                                          maptype='PROBING',
                                          cmpfunction=compareIntersectionIds)

    analyzer['connectionsDistance'] = gr.newGraph(datastructure='ADJ_LIST',
                                                  directed=False,
                                                  size=500000)
        
    analyzer['connectionsComparendos'] = gr.newGraph(datastructure='ADJ_LIST',
                                                     directed=False,
                                                     size=500000)
    
    analyzer['policeStations'] = lt.newList("ARRAY_LIST")

    analyzer['infractions'] = lt.newList("ARRAY_LIST")

    analyzer['vertices'] = lt.newList("ARRAY_LIST")

    analyzer['edges'] = set()
    
    analyzer['cityLimits'] = {
                              "minLongitude": 1000000000,
                              "maxLongitude": -100000000,
                              "minLatitude": 1000000000,
                              "maxLatitude": -100000000
                             }

    return analyzer 

# Funciones para agregar informacion al modelo

def add_vertex(analyzer, vertexId, longitudeVertex, latitudeVertex, vertexDict):

    vertexInfo = {
                  "ID": vertexId,
                  "longitudeVertex": longitudeVertex,
                  "latitudeVertex": latitudeVertex
                 }

    lt.addLast(analyzer['vertices'], vertexInfo)
    mp.put(analyzer['intersections'], vertexId, vertexDict)

    coordinateMap = round(longitudeVertex, 5)
    infoID = {
              "ID": vertexId,
              "latitudeVertex": latitudeVertex,
             }

    if not mp.contains(analyzer['coordinates'], coordinateMap):
        coordinatesID = lt.newList("ARRAY_LIST")
        lt.addLast(coordinatesID, infoID)
        mp.put(analyzer['coordinates'], coordinateMap, coordinatesID)

    else: 
        coordinateEntry = mp.get(analyzer['coordinates'], coordinateMap)
        coordinatesID = me.getValue(coordinateEntry)
        lt.addLast(coordinatesID, infoID)

    gr.insertVertex(analyzer['connectionsDistance'], vertexId)
    gr.insertVertex(analyzer['connectionsComparendos'], vertexId)

    if longitudeVertex < (analyzer['cityLimits'])["minLongitude"]:
        (analyzer['cityLimits'])["minLongitude"] = longitudeVertex

    if longitudeVertex > (analyzer['cityLimits'])["maxLongitude"]:
        (analyzer['cityLimits'])["maxLongitude"] = longitudeVertex

    if latitudeVertex < (analyzer['cityLimits'])["minLatitude"]:
        (analyzer['cityLimits'])["minLatitude"] = latitudeVertex

    if latitudeVertex > (analyzer['cityLimits'])["maxLatitude"]:
        (analyzer['cityLimits'])["maxLatitude"] = latitudeVertex

    return analyzer

def add_police_station(analyzer, infoStation):

    vertexStation = {
                     "ID": infoStation["OBJECTID"],
                     "Name": infoStation["EPONOMBRE"],
                     "Latitude": infoStation["EPOLATITUD"],
                     "Longitude": infoStation["EPOLONGITU"],
                     "Description": infoStation["EPODESCRIP"],
                     "Address": infoStation["EPODIR_SITIO"],
                     "Service": infoStation["EPOSERVICIO"],
                     "Schedule": infoStation["EPOHORARIO"],
                     "Phone": infoStation["EPOTELEFON"],
                     "Email": infoStation["EPOCELECTR"],
                     "vertex": infoStation["VERTICES"]
                    }
    
    lt.addLast(analyzer['policeStations'], vertexStation)

    vertexEntry = mp.get(analyzer['intersections'], infoStation["VERTICES"])
    infoVertex = me.getValue(vertexEntry)

    if "policeStations" not in infoVertex:
        infoVertex["policeStations"] = lt.newList("ARRAY_LIST")
        lt.addLast(infoVertex["policeStations"], vertexStation)

    else:
        lt.addLast(infoVertex["policeStations"], vertexStation)

    return analyzer

def add_comparendo(analyzer, infoComparendo):

    vertexComparendo = {
                        "ID": infoComparendo["OBJECTID"],
                        "Latitude": infoComparendo["LATITUD"],
                        "Longitude": infoComparendo["LONGITUD"],
                        "Infraction Date": infoComparendo["FECHA_HORA"],
                        "Detection Method": infoComparendo["MEDIO_DETECCION"],
                        "Vehicle Class": infoComparendo["CLASE_VEHICULO"],
                        "Service Type": infoComparendo["TIPO_SERVICIO"],
                        "Infraction": infoComparendo["INFRACCION"],
                        "Infraction Description": infoComparendo["DES_INFRACCION"],
                        "locality": infoComparendo["LOCALIDAD"],
                        "vertex": infoComparendo["VERTICES"]
                       }
    
    lt.addLast(analyzer['infractions'], vertexComparendo)

    if not mp.contains(analyzer['localities'], infoComparendo["LOCALIDAD"]):
        localityInfractions = lt.newList("ARRAY_LIST")
        lt.addLast(localityInfractions, vertexComparendo)
        om.put(analyzer['localities'], infoComparendo["LOCALIDAD"], localityInfractions)

    else:
        localityEntry = mp.get(analyzer['localities'], infoComparendo["LOCALIDAD"])
        localityInfractions = me.getValue(localityEntry)
        lt.addLast(localityInfractions, vertexComparendo)

    vertexEntry = mp.get(analyzer['intersections'], infoComparendo["VERTICES"])
    infoVertex = me.getValue(vertexEntry)

    if "Infractions" not in infoVertex:
        infoVertex["Infractions"] = lt.newList("ARRAY_LIST")
        lt.addLast(infoVertex["Infractions"], vertexComparendo)

    else:
        lt.addLast(infoVertex["Infractions"], vertexComparendo)

    return analyzer

def add_edge(analyzer, outVertex, inVertex):

    analyzer['edges'].add(outVertex)

    outVertexEntry = mp.get(analyzer['intersections'], outVertex)
    infOutVertex = me.getValue(outVertexEntry)
    longitudeOutVertex = infOutVertex["longitudeVertex"]
    latitudeOutVertex = infOutVertex["latitudeVertex"]

    if "Infractions" in infOutVertex:
        infractionsOutVertex = lt.size(infOutVertex["Infractions"])

    else: 
        infractionsOutVertex = 0

    inVertexEntry = mp.get(analyzer['intersections'], inVertex)
    infoInVertex = me.getValue(inVertexEntry)
    longitudeInVertex = infoInVertex["longitudeVertex"]
    latitudeInVertex = infoInVertex["latitudeVertex"]

    if "Infractions" in infoInVertex:
        infractionsInVertex = lt.size(infoInVertex["Infractions"]) 

    else: 
        infractionsInVertex = 0

    distance = haversineFunction(latitudeOutVertex, longitudeOutVertex, latitudeInVertex, longitudeInVertex)
    Comparendos = infractionsOutVertex + infractionsInVertex

    gr.addEdge(analyzer['connectionsDistance'], outVertex, inVertex, distance)
    gr.addEdge(analyzer['connectionsComparendos'], outVertex, inVertex, Comparendos)

    return analyzer

def get_load_info(analyzer):

    totalInfractions = lt.size(analyzer['infractions'])
    InfractionsList = first_last_5(analyzer['infractions'])

    totalPoliceStations = lt.size(analyzer['policeStations'])
    policeStationsList = first_last_5(analyzer['policeStations'])

    totalVertices = gr.numVertices(analyzer['connectionsDistance'])
    verticesList = first_last_5(analyzer['vertices'])

    limits = analyzer['cityLimits']

    totalEdges = gr.numEdges(analyzer['connectionsDistance'])
    outVerticesList = lt.newList("ARRAY_LIST")
    edgesList = lt.newList("ARRAY_LIST")

    for outVertex in analyzer['edges']:
        lt.addLast(outVerticesList, outVertex)
        
    outVertices = first_last_5(outVerticesList)

    for printOutVertex in lt.iterator(outVertices):
        adyacentsList = lt.newList("ARRAY_LIST")
        adyacentsID = gr.adjacents(analyzer['connectionsDistance'], printOutVertex)

        for adyacentID in lt.iterator(adyacentsID):
            lt.addLast(adyacentsList, adyacentID)
        
        adyacentsInfo = {   
                         "ID": printOutVertex, 
                         "adyacentsID": adyacentsList["elements"]
                        }
        
        lt.addLast(edgesList, adyacentsInfo)
    
    return totalInfractions, InfractionsList, totalPoliceStations, policeStationsList, totalVertices, verticesList, limits, totalEdges, edgesList
    
def req_1(analyzer, longitud1, latitud1, longitud2, latitud2):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    longitud1 = round(longitud1,5)
    latitud1 = round(latitud1, 5)
    longitud2 = round(longitud2, 5)
    latitud2 = round(latitud2, 5)
    verticein = ""
    verticeto = ""
    menor1 = 9999999
    menor2 = 9999999
    if mp.contains(analyzer["coordinates"], longitud1):
        entryin = mp.get(analyzer["coordinates"], longitud1)
        verticeins = me.getValue(entryin)
        for i in lt.iterator(verticeins):
                resta = abs(latitud2-i["latitudeVertex"])
                if resta < menor1: 
                    menor1 = resta
                    verticein = i["ID"]
    if mp.contains(analyzer["coordinates"], longitud2):
        entryto = mp.get(analyzer["coordinates"], longitud2)
        verticetos = me.getValue(entryto)
        for o in lt.iterator(verticetos):
                resta = abs(latitud2-o["latitudeVertex"])
                if resta < menor2: 
                    menor2= resta
                    verticeto = o["ID"]
    search= dfs.DepthFirstSearch(analyzer['connectionsDistance'], verticein)
    camino = dfs.pathTo(search, verticeto)
    distancia = 0
    i = 0
    peso = None
    while i < lt.size(camino):
        verticea = lt.getElement(camino, i)
        verticeb = lt.getElement(camino, i+1)
        arco = gr.getEdge(analyzer['connectionsDistance'], verticea, verticeb)
        if arco != None: 
            peso = arco["weight"]
        if peso != None: 
            distancia += peso
        i += 1
    mapa = req_8(analyzer['intersections'], camino, 1)
    return distancia, lt.size(camino), camino

def req_2(analyzer, originLatiude, originLongitude, destinationLatitude, destinationLongitude):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    originCoordinate = round(originLongitude, 5)
    destinationCoordinate = round(destinationLongitude, 5)

    if mp.contains(analyzer['coordinates'], originCoordinate):
        originCoordinateEntry = mp.get(analyzer['coordinates'], originCoordinate)
        originCoordinatesID = me.getValue(originCoordinateEntry)

        minOriginDistance = 1000000
        originID = None
        
        for originCoordinateID in lt.iterator(originCoordinatesID):
            originDistance = abs(originLatiude - originCoordinateID["latitudeVertex"])

            if originDistance < minOriginDistance:
                minOriginDistance = originDistance
                originID = originCoordinateID["ID"]

    BFSearch = bfs.BreathFirstSearch(analyzer['connectionsDistance'], originID)

    if mp.contains(analyzer['coordinates'], destinationCoordinate):
        destinationCoordinateEntry = mp.get(analyzer['coordinates'], destinationCoordinate)
        destinationCoordinatesID = me.getValue(destinationCoordinateEntry)
        
        minDestinationDistance = 1000000
        destinationID = None
        
        for destinationCoordinateID in lt.iterator(destinationCoordinatesID):
            destinationDistance = abs(destinationLatitude - destinationCoordinateID["latitudeVertex"])

            if destinationDistance < minDestinationDistance:
                minDestinationDistance = destinationDistance
                destinationID = destinationCoordinateID["ID"]

    path = bfs.pathTo(BFSearch, destinationID)
    verticesPath = lt.size(path)

    routeVertices = (originID, destinationID)
    totalDistance = 0
    
    for i in range(1, lt.size(path)):
        firstVertex = lt.getElement(path, i)
        nextVertex = lt.getElement(path, i+1)
        
        edge = gr.getEdge(analyzer['connectionsDistance'], firstVertex, nextVertex)
        totalDistance += edge["weight"]

    mapa = req_8(analyzer['intersections'], path, 2)

    return path, verticesPath, totalDistance, routeVertices

def req_3(analyzer, cameras, locality):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    verticesLocality = set()

    localityEntry = mp.get(analyzer['localities'], locality)
    localityInfractions = me.getValue(localityEntry)

    for infraction in lt.iterator(localityInfractions):
        verticesLocality.add(infraction["vertex"])

    condiHeap = mpq.newMinPQ(sortComparendos)

    for vertexLocality in verticesLocality:
        vertexEntry = mp.get(analyzer['intersections'], vertexLocality)
        infoVertex = me.getValue(vertexEntry)
        mpq.insert(condiHeap, infoVertex)

    camerasVertices = lt.newList("ARRAY_LIST")

    for _ in range(cameras):

        if not mpq.isEmpty(condiHeap):
            maxInfractions = mpq.delMin(condiHeap) 
            lt.addLast(camerasVertices, maxInfractions["ID"])

    print(camerasVertices["elements"])
    originVertex = lt.firstElement(camerasVertices)
    communicationRed = prim.PrimMST(analyzer['connectionsDistance'], originVertex)

    DistanceRed = 0
    routesRed = mp.newMap(numelements=500000,
                                          maptype='PROBING',
                                          cmpfunction=compareIntersectionIds)

    for i in range(2, lt.size(camerasVertices)):

        routeVertex = lt.newList("ARRAY_LIST")
        actualVertex = lt.getElement(camerasVertices, i)
        lt.addLast(routeVertex, actualVertex)

        while actualVertex != originVertex:

            VertexEntry = mp.get(communicationRed["edgeTo"], actualVertex)
            previousEdge = me.getValue(VertexEntry)
            previousVertex = ed.other(previousEdge, actualVertex)
            lt.addLast(routeVertex, previousVertex)
        
            VertexEntry2 = mp.get(communicationRed["distTo"], actualVertex)
            distanceCost = me.getValue(VertexEntry2)
            DistanceRed += distanceCost

            actualVertex = previousVertex

        lt.addLast(routeVertex, originVertex)
        om.put(routesRed, lt.getElement(camerasVertices, i), routeVertex)

    totalCost = 1000000 * DistanceRed

    mapa = req_8(analyzer['intersections'], camerasVertices, 3)
    
    return camerasVertices, originVertex, routesRed, DistanceRed, totalCost

def req_4(analyzer, m):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    start = float(t.perf_counter()*1000)
    costo_fibra = 1000000
    kms = 0
    lista_ordenada = mpq.newMinPQ(cmp_gravedad_2)
    listaf = lt.newList("ARRAY_LIST")
    for infraccion in lt.iterator(analyzer["infractions"]):
        mpq.insert(lista_ordenada, infraccion)
    while lt.size(listaf) < m:
        elemento = mpq.delMin(lista_ordenada)
        lt.addLast(listaf, elemento["ID"])
    red = prim.PrimMST(analyzer['connectionsDistance'], lt.getElement(listaf, 1))
    mapaderutas = mp.newMap(numelements=500000,
                                          maptype='PROBING',
                                          cmpfunction=compareIntersectionIds)
    for i in range(2, lt.size(listaf)):
        ruta = lt.newList("ARRAY_LIST")
        actualVertex = lt.getElement(listaf, i)
        lt.addLast(ruta, actualVertex)
        while actualVertex != lt.getElement(listaf, 1):
            Entry = mp.get(red["edgeTo"], actualVertex)
            arco = me.getValue(Entry)
            vertice = ed.other(arco, actualVertex)
            lt.addLast(ruta, vertice)
            Entry2 = mp.get(red["distTo"], actualVertex)
            costo= me.getValue(Entry2)
            kms += costo
            lt.addLast(ruta, lt.getElement(listaf, 1))
            om.put(mapaderutas, lt.getElement(listaf, i), ruta)
    costo_total = kms * costo_fibra
    end = float(t.perf_counter()*1000)
    time = float(end-start)
    mapa = req_8(analyzer['intersections'], listaf, 4)
    return time, lt.size(listaf), listaf, mapaderutas, kms, costo_total

def req_5(grafo_d, data, m, clase_v):
    """
    Función que soluciona el requerimiento 5
    """
    costo_fibra = 1000000
    ids = mp.keySet(data)
    lista = lt.newList("ARRAY_LIST")
    max_comparendos = mpq.newMinPQ(cmp_n_comparendos)
    vertices_red = lt.newList("ARRAY_LIST")
    kms = 0

    for i in lt.iterator(ids):
        dict_c = {}
        entry = mp.get(data, i)
        info = me.getValue(entry)
        if len(info) >= 5:
            comparendos = info["Infractions"]
            contador = 0
            
            for j in lt.iterator(comparendos):
                if j["Vehicle Class"] == clase_v:
                    contador += 1
            dict_c["id"] = i
            dict_c["n"] = contador
            mpq.insert(max_comparendos, dict_c)
    
    
    for _ in range(m):
        max = mpq.delMin(max_comparendos)
        lt.addLast(lista, max)

    red = prim.PrimMST(grafo_d, lt.getElement(lista, 1)["id"])
    lt.addLast(vertices_red, lt.getElement(lista, 1)["id"])
    n_c = mp.newMap(numelements=200, maptype='PROBING')
    
    for i in range(2, m+1):
        valor, vertice_1, vertice_2 = distancia_total(red, lt.getElement(lista, i)["id"])
        kms += valor
        mp.put(n_c, vertice_1, 1)
        mp.put(n_c, vertice_2, 1)
        

    vertices_red = mp.keySet(n_c)
    
        
    costo_total = kms * costo_fibra

    mapa = req_8(data, vertices_red, 5)
    
    return m, vertices_red, kms, costo_total

def req_6(grafo, data, m, estaciones, estacion):
    """
    Función que soluciona el requerimiento 6
    """
    partida = ""
    for s in lt.iterator(estaciones):
        if s["ID"] == estacion:
            partida = s["vertex"]

    ids = mp.keySet(data)
    lista = lt.newList("ARRAY_LIST")
    for i in lt.iterator(ids):
        dict_c = {}
        entry = mp.get(data, i)
        info = me.getValue(entry)
        if len(info) >= 5:
            comparendos = info["Infractions"]
            for j in lt.iterator(comparendos):
                dict_c["id"] = i
                dict_c["Service Type"] = j["Service Type"]
                dict_c["Infraction"] = j["Infraction"]
                lt.addLast(lista, dict_c)

    sorted_list = merg.sort(lista, cmp_gravedad)
    sorted_list = lt.subList(sorted_list, 1, m)
    coordenadas = lt.newList("ARRAY_LIST")
    red = djk.Dijkstra(grafo, partida)
    rta = lt.newList("ARRAY_LIST")
    for j in lt.iterator(sorted_list):
        if djk.hasPathTo(red, j["id"]):
            camino = djk.pathTo(red, j["id"])
            n_c = mp.newMap(numelements=200, maptype='PROBING')
            for c in lt.iterator(camino):
                mp.put(n_c, c["vertexA"], 1)
                mp.put(n_c, c["vertexB"], 1)
                lt.addLast(coordenadas, c["vertexA"])
                lt.addLast(coordenadas, c["vertexB"])
            vertices = mp.keySet(n_c)
            cadena = ""
            for v in lt.iterator(vertices):
                cadena += v + ", "
            cadena.strip(" ,")
            data_camino = {}
            data_camino["vertices totales"] = mp.size(n_c)
            data_camino["vertices"] = cadena
            data_camino["kilometros"] = djk.distTo(red, j["id"])
            lt.addLast(rta, data_camino)
    mapa = req_8(data, coordenadas, 6)
    return rta 

def req_7(analyzer, originLatiude, originLongitude, destinationLatitude, destinationLongitude):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    originCoordinate = round(originLongitude, 5)
    destinationCoordinate = round(destinationLongitude, 5)

    if mp.contains(analyzer['coordinates'], originCoordinate):
        originCoordinateEntry = mp.get(analyzer['coordinates'], originCoordinate)
        originCoordinatesID = me.getValue(originCoordinateEntry)

        minOriginDistance = 1000000
        originID = None
        
        for originCoordinateID in lt.iterator(originCoordinatesID):
            originDistance = abs(originLatiude - originCoordinateID["latitudeVertex"])

            if originDistance < minOriginDistance:
                minOriginDistance = originDistance
                originID = originCoordinateID["ID"]

    print(originID)
    DJKsearch = djk.Dijkstra(analyzer['connectionsComparendos'], originID)

    if mp.contains(analyzer['coordinates'], destinationCoordinate):
        destinationCoordinateEntry = mp.get(analyzer['coordinates'], destinationCoordinate)
        destinationCoordinatesID = me.getValue(destinationCoordinateEntry)
        
        minDestinationDistance = 1000000
        destinationID = None
        
        for destinationCoordinateID in lt.iterator(destinationCoordinatesID):
            destinationDistance = abs(destinationLatitude - destinationCoordinateID["latitudeVertex"])

            if destinationDistance < minDestinationDistance:
                minDestinationDistance = destinationDistance
                destinationID = destinationCoordinateID["ID"]

    path = djk.pathTo(DJKsearch, destinationID)
    verticesPath = lt.size(path)

    totalInfractions = djk.distTo(DJKsearch, destinationID)
    totalDistance = 0

    for i in range(1, lt.size(path)):
        firstVertex = lt.getElement(path, i)
        nextVertex = lt.getElement(path, i+1)

        edgeDistance = gr.getEdge(analyzer['connectionsDistance'], firstVertex["vertexB"], nextVertex["vertexB"])
        totalDistance += edgeDistance["weight"]

    bonoList = lt.newList("ARRAY_LIST")
    for vertexRoute in lt.iterator(path):
        lt.addLast(bonoList, vertexRoute["vertexB"])
    mapa = req_8(analyzer['intersections'], bonoList, 8)

    return path, verticesPath, totalInfractions, totalDistance

def req_8(data, vertices, req):
    """
    Función que soluciona el requerimiento 8
    """
    mapa = folium.Map(location=[4.6097, -74.0817], zoom_start=12)

    coordenadas = []
    for v in lt.iterator(vertices):
        entry = mp.get(data, v)
        info = me.getValue(entry)
        punto = [info["latitudeVertex"], info["longitudeVertex"]]
        coordenadas.append(punto)

    folium.PolyLine(
    locations=coordenadas,
    color='red',
    weight=3,
    opacity=1
    ).add_to(mapa)  
    mapa.save("req"+ str(req) +".html")

# Funciones utilizadas para comparar elementos dentro de una lista

def compareIntersectionIds(intersection, results):
    """
    Compara dos estaciones
    """
    resultentry = me.getKey(results)
    if (intersection == resultentry):
        return 0
    elif (intersection > resultentry):
        return 1
    else:
        return -1

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

def haversineFunction(lat1, lon1, lat2, lon2):

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    lambda1 = math.radians(lon1)
    lambda2 = math.radians(lon2)

    radius = 6371

    delta_phi = phi2 - phi1
    delta_lambda = lambda2 - lambda1

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = c * radius

    return distance

def first_last_5(list):

    subList = lt.newList("ARRAY_LIST")
    first3 = lt.subList(list, 1, 5)
    last3 = lt.subList(list, (lt.size(list))-4, 5)

    for i in lt.iterator(first3):
        lt.addLast(subList, i)

    for j in lt.iterator(last3):
        lt.addLast(subList, j)

    return subList

def cmp_n_comparendos(entry1, entry2):

    if entry1["n"] < entry2["n"]:
        return True
    else:
        return False

def cmp_gravedad(comparendo1, comparendo2):
    
    if valor(comparendo1) > valor(comparendo2):
        return True
    elif valor(comparendo1) == valor(comparendo2):
        if comparendo1["Infraction"] > comparendo2["Infraction"]:
            return True
    else:
        return False
    
def valor(comparendo):
    if comparendo["Service Type"] == "Público":
        return 10
    elif comparendo["Service Type"] == "Oficial":
        return 8
    elif comparendo["Service Type"] == "Particular":
        return 5
    else:
        return 1
def valor2(comparendo): 
    if comparendo["Service Type"] == "Diplomatico":
        return 10
    elif comparendo["Service Type"] == "Oficial":
        return 8
    elif comparendo["Service Type"] == "Público":
        return 5
    else:
        return 1
def cmp_gravedad_2(comparendo1, comparendo2):
    rta = False
    if valor2(comparendo1) < valor2(comparendo2):
        rta = True
    elif valor2(comparendo1) == valor2(comparendo2):
        if comparendo1["Infraction"] < comparendo2["Infraction"]:
            rta = True
    return rta
def sortComparendos(info1, info2):
    rta = False
    comparendos1 = lt.size(info1["Infractions"])
    comparendos2 = lt.size(info2["Infractions"])

    if comparendos1 < comparendos2:
        rta = True

    elif comparendos1 == comparendos2:
        if int(info1["ID"]) > int(info2["ID"]):
            rta = True

    return rta

def distancia_total(mst, id):
    kms = 0
    entry = mp.get(mst["edgeTo"], id)
    camino =me.getValue(entry)
    vertex_a = camino["vertexA"]
    vertex_b = camino["vertexB"]
    entry_1 = mp.get(mst["distTo"], camino["vertexA"])
    valor_1 = me.getValue(entry_1)
    kms += valor_1
    entry_2 = mp.get(mst["distTo"], camino["vertexB"])
    valor_2 = me.getValue(entry_2)
    kms += valor_2

    return kms, vertex_a, vertex_b
