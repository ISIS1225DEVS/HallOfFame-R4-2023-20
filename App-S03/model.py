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
from haversine import haversine
import folium
from folium.plugins import MarkerCluster
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos
def newDataStructs():
    dataStructs = {}
    dataStructs['metaData'] = {}
    dataStructs['distanceGraph'] = gr.newGraph()
    dataStructs['infractionGraph'] = gr.newGraph()
    dataStructs['vertexMap'] = mp.newMap(230000, maptype='PROBING')
    dataStructs['localities'] = mp.newMap(23, maptype='PROBING')
    dataStructs['vehicles'] = mp.newMap(23, maptype='PROBING')
    dataStructs['infractions'] = lt.newList('ARRAY_LIST')
    dataStructs['stations'] = lt.newList('ARRAY_LIST')
    dataStructs['vertices'] = lt.newList('ARRAY_LIST')
    dataStructs['edges'] = lt.newList('ARRAY_LIST')
    dataStructs['mstGraph'] = None
    return dataStructs

# Funciones para agregar informacion al modelo
def addVertex(dataStructs, vertex):
    lt.addLast(dataStructs['vertices'], vertex)
    gr.insertVertex(dataStructs['distanceGraph'], vertex['id'])
    gr.insertVertex(dataStructs['infractionGraph'], vertex['id'])
    mp.put(dataStructs['vertexMap'], vertex['id'], newVertex(vertex))
    calculateArea(dataStructs, vertex)

def addInfraction(dataStructs, infraction):
    relateToVertex(dataStructs, infraction, 'infractions')
    addInfractionByAttribute(dataStructs['localities'], infraction, 'LOCALIDAD')
    addInfractionByAttribute(dataStructs['localities'], infraction, 'CLASE_VEHICULO')

def addInfractionByAttribute(attributeMap, infraction, attribute):
    attribute = infraction[attribute].title()
    entry = mp.get(attributeMap, attribute)
    if entry:
        vertexMap = me.getValue(entry)
    else:
        vertexMap = mp.newMap(230000, maptype='PROBING')
        mp.put(attributeMap, attribute, vertexMap)
    vertex = infraction['VERTICES']
    entry = mp.get(vertexMap, vertex)
    if entry:
        vertexNode = me.getValue(entry)
    else:
        vertexNode = {"vertex": vertex, "count": 1}
        mp.put(vertexMap, vertex, vertexNode)
    vertexNode['count'] += 1

def relateToVertex(dataStructs, datum, attribute):
    vertexMap = dataStructs['vertexMap']
    vertex = datum['VERTICES']
    entry = mp.get(vertexMap, vertex)
    if entry:
        vertexNode = me.getValue(entry)
        lt.addLast(vertexNode[attribute], datum)
    lt.addLast(dataStructs[attribute], datum)
    
def addEdge(dataStructs, edge):
    vertexA = edge['vertex']
    entry = mp.get(dataStructs['vertexMap'], vertexA)
    if entry:
        lt.addLast(dataStructs['edges'], edge)
        vertexANode = me.getValue(entry)
        for vertexB in edge['adjacentVertex']:
            entry = mp.get(dataStructs['vertexMap'], vertexB)
            if entry:
                vertexBNode = me.getValue(entry)
                distance = haversine(vertexANode['coordinates'], vertexBNode['coordinates'])
                gr.addEdge(dataStructs['distanceGraph'], vertexA, vertexB, distance)
                gr.addEdge(dataStructs['infractionGraph'], vertexA, vertexB, lt.size(vertexANode['infractions']) + lt.size(vertexBNode['infractions']))

def calculateArea(dataStructs, vertex):
    latitudes = dataStructs['metaData'].get('latitudes', [vertex['coordinates'][0], vertex['coordinates'][0]])
    longitudes = dataStructs['metaData'].get('longitudes', [vertex['coordinates'][1], vertex['coordinates'][1]])
    if vertex['coordinates'][0] < latitudes[0]:
        latitudes[0] = vertex['coordinates'][0]
    if vertex['coordinates'][0] > latitudes[1]:
        latitudes[1] = vertex['coordinates'][0]
    if vertex['coordinates'][1] < longitudes[0]:
        longitudes[0] = vertex['coordinates'][1]
    if vertex['coordinates'][1] > longitudes[1]:
        longitudes[1] = vertex['coordinates'][1]
    dataStructs['metaData']['latitudes'] = latitudes
    dataStructs['metaData']['longitudes'] = longitudes

def addSeismicEventToSimpleMap(featureMap, seismicEvent, feature):
    feature = seismicEvent[feature]
    entry = mp.get(featureMap, feature)
    if entry:
        featureList = me.getValue(entry)
    else:
        featureList = lt.newList('ARRAY_LIST')
        mp.put(featureMap, feature, featureList)
    lt.addLast(featureList, seismicEvent)

# Funciones para creacion de datos
def newVertex(vertex):
    # vertex = {'id': id, 'coordinates': coordinates}
    vertex['stations'] = lt.newList('ARRAY_LIST')
    vertex['infractions'] = lt.newList('ARRAY_LIST')
    return vertex

# Funciones de consulta
def req1(dataStructs, startPoint, arrivalPoint):
    filtered = lt.newList('ARRAY_LIST')
    foliumMap = lt.newList()
    drawPath = []
    metaData = {'totalVertex': 0, 'totalDistance': 0}
    if isInside(dataStructs, startPoint) and isInside(dataStructs, arrivalPoint):
        startPoint = getClosestVertex(dataStructs, startPoint)
        arrivalPoint = getClosestVertex(dataStructs, arrivalPoint)
        paths = dfs.DepthFirstSearch(dataStructs['distanceGraph'], startPoint['id'])
        path = dfs.pathTo(paths, arrivalPoint['id'])
        if path:
            metaData['totalVertex'] = st.size(path)
            datum = {'Starting Point': 'Satarting point', 'Arrival Point': st.top(path), 'Distance': startPoint['distance']}
            lt.addLast(filtered, datum)
            while st.size(path) > 1:
                startingVertex = st.pop(path)
                arrivalVertex = st.top(path)
                distance = gr.getEdge(dataStructs['distanceGraph'], startingVertex, arrivalVertex)['weight']
                metaData['totalDistance'] += distance
                datum = {'Starting Point': startingVertex, 'Arrival Point': arrivalVertex, 'Distance': distance}
                lt.addLast(filtered, datum)
                startingVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], startingVertex))
                arrivalVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], arrivalVertex))
                lt.addLast(foliumMap, startingVertexDetails)
                lt.addLast(foliumMap, arrivalVertexDetails)
                drawPath.append((startingVertexDetails['coordinates'], arrivalVertexDetails['coordinates']))
            datum = {'Starting Point': st.top(path), 'Arrival Point': 'Arrival point', 'Distance': arrivalPoint['distance']}
            lt.addLast(filtered, datum)
            metaData['totalDistance'] += startPoint['distance']
            metaData['totalDistance'] += arrivalPoint['distance']
    metaData["map"] = lt.size(foliumMap) > 0
    metaData["path"] = "req1"
    req8(foliumMap, "req1", drawPath)
    return filtered, metaData

def req2(dataStructs, startPoint, arrivalPoint):
    filtered = lt.newList('ARRAY_LIST')
    metaData = {'totalVertex': 0, 'totalDistance': 0}
    foliumMap = lt.newList()
    drawPath = []
    if isInside(dataStructs, startPoint) and isInside(dataStructs, arrivalPoint):
        startPoint = getClosestVertex(dataStructs, startPoint)
        arrivalPoint = getClosestVertex(dataStructs, arrivalPoint)
        paths = bfs.BreathFirstSearch(dataStructs['distanceGraph'], startPoint['id'])
        path = bfs.pathTo(paths, arrivalPoint['id'])
        if path:
            metaData['totalVertex'] = st.size(path)
            datum = {'Starting Point': 'Starting point', 'Arrival Point': st.top(path), 'Distance': startPoint['distance']}
            lt.addLast(filtered, datum)
            while st.size(path) > 1:
                startingVertex = st.pop(path)
                arrivalVertex = st.top(path)
                distance = gr.getEdge(dataStructs['distanceGraph'], startingVertex, arrivalVertex)['weight']
                metaData['totalDistance'] += distance
                datum = {'Starting Point': startingVertex, 'Arrival Point': arrivalVertex, 'Distance': distance}
                lt.addLast(filtered, datum)
                startingVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], startingVertex))
                arrivalVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], arrivalVertex))
                lt.addLast(foliumMap, startingVertexDetails)
                lt.addLast(foliumMap, arrivalVertexDetails)
                drawPath.append((startingVertexDetails['coordinates'], arrivalVertexDetails['coordinates']))
            datum = {'Starting Point': st.top(path), 'Arrival Point': 'Arrival point', 'Distance': arrivalPoint['distance']}
            lt.addLast(filtered, datum)
            metaData['totalDistance'] += startPoint['distance']
            metaData['totalDistance'] += arrivalPoint['distance']
    metaData["map"] = lt.size(foliumMap) > 0
    metaData["path"] = "req2"
    req8(foliumMap, "req2", drawPath)
    return filtered, metaData

def req3(dataStructs, locality, M):
    filtered = lt.newList('ARRAY_LIST')
    metaData = {'totalDistance': 0}
    foliumMap = lt.newList()
    drawPath = []
    entry = mp.get(dataStructs['localities'], locality)
    if entry:
        if not dataStructs['mstGraph']:
            mst = prim.PrimMST(dataStructs['distanceGraph'])
            prim.edgesMST(dataStructs['distanceGraph'], mst)
            mstGraph = createMstGraph(mst)
            dataStructs['mstGraph'] = mstGraph
        mstGraph = dataStructs['mstGraph']
        localityVertices = sortData(mp.valueSet(me.getValue(entry)), compareByCount)
        paths = bfs.BreathFirstSearch(mstGraph, lt.firstElement(localityVertices)['vertex'])
        arrivalVertexIndex = 2
        while lt.size(filtered) < M and arrivalVertexIndex <= lt.size(localityVertices):
            arrivalVertex = lt.getElement(localityVertices, arrivalVertexIndex)['vertex']
            if bfs.hasPathTo(paths, arrivalVertex):
                path = bfs.pathTo(paths, arrivalVertex)
                while st.size(path) > 1:
                    startingVertex = st.pop(path)
                    arrivalVertex = st.top(path)
                    distance = gr.getEdge(mstGraph, startingVertex, arrivalVertex)['weight']
                    datum = {'Starting Point': startingVertex, 'Arrival Point': arrivalVertex, 'Distance': round(distance, 4)}
                    if not existsStep(filtered, datum):
                        lt.addLast(filtered, datum)
                        metaData['totalDistance'] += distance
                        startingVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], startingVertex))
                        arrivalVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], arrivalVertex))
                        lt.addLast(foliumMap, startingVertexDetails)
                        lt.addLast(foliumMap, arrivalVertexDetails)
                        drawPath.append((startingVertexDetails['coordinates'], arrivalVertexDetails['coordinates']))
            arrivalVertexIndex += 1
    metaData['totalVertices'] = lt.size(filtered) + 1 if lt.size(filtered) > 0 else 0
    metaData["map"] = lt.size(foliumMap) > 0
    metaData["path"] = "req3"
    req8(foliumMap, "req3", drawPath)
    return filtered, metaData

def req4(dataStructs, M):
    filtered = lt.newList('ARRAY_LIST')
    metaData = {'totalDistance': 0}
    foliumMap = lt.newList()
    drawPath = []
    if not dataStructs['mstGraph']:
        mst = prim.PrimMST(dataStructs['distanceGraph'])
        prim.edgesMST(dataStructs['distanceGraph'], mst)
        mstGraph = createMstGraph(mst)
        dataStructs['mstGraph'] = mstGraph
    mstGraph = dataStructs['mstGraph']
    infractions = dataStructs['infractions']
    paths = bfs.BreathFirstSearch(mstGraph, lt.firstElement(infractions)['VERTICES'])
    visitedVertices = set()
    arrivalVertexIndex = 2
    while lt.size(filtered) < M and arrivalVertexIndex <= lt.size(infractions):
        arrivalVertex = lt.getElement(infractions, arrivalVertexIndex)['VERTICES']
        if arrivalVertex not in visitedVertices and bfs.hasPathTo(paths, arrivalVertex):
            visitedVertices.add(arrivalVertex)
            path = bfs.pathTo(paths, arrivalVertex)
            while st.size(path) > 1:
                startingVertex = st.pop(path)
                arrivalVertex = st.top(path)
                distance = gr.getEdge(mstGraph, startingVertex, arrivalVertex)['weight']
                datum = {'Starting Point': startingVertex, 'Arrival Point': arrivalVertex, 'Distance': round(distance, 4)}
                if not existsStep(filtered, datum):
                    lt.addLast(filtered, datum)
                    metaData['totalDistance'] += distance
                    startingVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], startingVertex))
                    arrivalVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], arrivalVertex))
                    lt.addLast(foliumMap, startingVertexDetails)
                    lt.addLast(foliumMap, arrivalVertexDetails)
                    drawPath.append((startingVertexDetails['coordinates'], arrivalVertexDetails['coordinates']))
        arrivalVertexIndex += 1
    metaData['totalVertices'] = lt.size(filtered) + 1 if lt.size(filtered) > 0 else 0
    metaData["map"] = lt.size(foliumMap) > 0
    metaData["path"] = "req4"
    req8(foliumMap, "req4", drawPath)
    return filtered, metaData

def req5(dataStructs, vehicle, M):
    filtered = lt.newList('ARRAY_LIST')
    metaData = {'totalDistance': 0}
    foliumMap = lt.newList()
    drawPath = []
    entry = mp.get(dataStructs['localities'], vehicle)
    if entry:
        if not dataStructs['mstGraph']:
            mst = prim.PrimMST(dataStructs['distanceGraph'])
            prim.edgesMST(dataStructs['distanceGraph'], mst)
            mstGraph = createMstGraph(mst)
            dataStructs['mstGraph'] = mstGraph
        mstGraph = dataStructs['mstGraph']
        vehicleVertices = sortData(mp.valueSet(me.getValue(entry)), compareByCount)
        paths = bfs.BreathFirstSearch(mstGraph, lt.firstElement(vehicleVertices)['vertex'])
        arrivalVertexIndex = 2
        while lt.size(filtered) < M and arrivalVertexIndex <= lt.size(vehicleVertices):
            arrivalVertex = lt.getElement(vehicleVertices, arrivalVertexIndex)['vertex']
            if bfs.hasPathTo(paths, arrivalVertex):
                path = bfs.pathTo(paths, arrivalVertex)
                while st.size(path) > 1:
                    startingVertex = st.pop(path)
                    arrivalVertex = st.top(path)
                    distance = gr.getEdge(mstGraph, startingVertex, arrivalVertex)['weight']
                    datum = {'Starting Point': startingVertex, 'Arrival Point': arrivalVertex, 'Distance': round(distance, 4)}
                    if not existsStep(filtered, datum):
                        lt.addLast(filtered, datum)
                        metaData['totalDistance'] += distance
                        startingVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], startingVertex))
                        arrivalVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], arrivalVertex))
                        lt.addLast(foliumMap, startingVertexDetails)
                        lt.addLast(foliumMap, arrivalVertexDetails)
                        drawPath.append((startingVertexDetails['coordinates'], arrivalVertexDetails['coordinates']))
            arrivalVertexIndex += 1
    metaData['totalVertices'] = lt.size(filtered) + 1 if lt.size(filtered) > 0 else 0
    metaData["map"] = lt.size(foliumMap) > 0
    metaData["path"] = "req5"
    req8(foliumMap, "req5", drawPath)
    return filtered, metaData

def req6(dataStructs, M):
    filtered = lt.newList('ARRAY_LIST')
    metaData = {}
    foliumMap = lt.newList()
    drawPath = []
    infractions = dataStructs['infractions']
    mostSeverityIndex = 1
    while lt.size(filtered) < M and mostSeverityIndex <= lt.size(infractions):
        pathDetails = lt.newList('ARRAY_LIST')
        mostSeverity = lt.getElement(infractions, mostSeverityIndex)
        metaData = {'totalDistance': 0, 'totalVertices': 0, 'infraction': lt.newList()}
        lt.addLast(metaData['infraction'], mostSeverity)
        paths = djk.Dijkstra(dataStructs['distanceGraph'], mostSeverity['VERTICES'])
        closestStation = getClosestStation(dataStructs, paths)
        if closestStation:
            path = djk.pathTo(paths, closestStation['VERTICES'])
            lt.addLast(pathDetails, {'Starting Point': 'Severitiest Infraction', 'Arrival Point': st.top(path)['vertexA'] if st.size(path) > 0 else closestStation['VERTICES'], 'Distance': 0})
            metaData['totalVertices'] = lt.size(path) + 1 if lt.size(path) > 0 else 0
            while not st.isEmpty(path):
                step = st.pop(path)
                datum = {'Starting Point': step['vertexA'], 'Arrival Point': step['vertexB'], 'Distance': round(step['weight'], 3)}
                lt.addLast(pathDetails, datum)
                startingVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], step['vertexA']))
                arrivalVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], step['vertexB']))
                lt.addLast(foliumMap, startingVertexDetails)
                lt.addLast(foliumMap, arrivalVertexDetails)
                drawPath.append((startingVertexDetails['coordinates'], arrivalVertexDetails['coordinates']))
            lt.addLast(pathDetails, {'Starting Point': closestStation['VERTICES'], 'Arrival Point': 'Closest Police Station', 'Distance': 0})
            metaData['totalDistance'] = djk.distTo(paths, closestStation['VERTICES'])
            pathDetails['metaData'] = metaData
            lt.addLast(filtered, pathDetails)
        mostSeverityIndex += 1
    metaData["map"] = lt.size(foliumMap) > 0
    metaData["path"] = "req6"
    req8(foliumMap, "req6", drawPath)
    return filtered, metaData

def req7(dataStructs, startPoint, arrivalPoint):
    filtered = lt.newList('ARRAY_LIST')
    metaData = {'totalDistance': 0, 'totalVertices': 0, 'totalInfractions': 0}
    foliumMap = lt.newList()
    drawPath = []
    if isInside(dataStructs, startPoint) and isInside(dataStructs, arrivalPoint):
        startPoint = getClosestVertex(dataStructs, startPoint)
        arrivalPoint = getClosestVertex(dataStructs, arrivalPoint)
        paths = djk.Dijkstra(dataStructs['infractionGraph'], startPoint['id'])
        path = djk.pathTo(paths, arrivalPoint['id'])
        if path:
            metaData['totalVertices'] = st.size(path) + 1 if st.size(path) > 0 else 0
            metaData['totalDistance'] += startPoint['distance']
            datum = {'Starting Point': 'Starting point', 'Arrival Point': st.top(path)['vertexA'], 'Num Infractions': 0, 'Distance': startPoint['distance']}
            lt.addLast(filtered, datum)
            while not st.isEmpty(path):
                step = st.pop(path)
                distance = gr.getEdge(dataStructs['distanceGraph'], step['vertexA'], step['vertexB'])['weight']
                datum = {'Starting Point': step['vertexA'], 'Arrival Point': step['vertexB'], 'Num Infractions': step['weight'], 'Distance': round(distance, 4)}
                lt.addLast(filtered, datum)
                metaData['totalDistance'] += distance
                startingVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], step['vertexA']))
                arrivalVertexDetails = me.getValue(mp.get(dataStructs['vertexMap'], step['vertexB']))
                lt.addLast(foliumMap, startingVertexDetails)
                lt.addLast(foliumMap, arrivalVertexDetails)
                drawPath.append((startingVertexDetails['coordinates'], arrivalVertexDetails['coordinates']))
            datum = {'Starting Point':arrivalPoint['id'], 'Arrival Point': 'Arrival point', 'Num Infractions': 0, 'Distance': arrivalPoint['distance']}
            metaData['totalDistance'] += arrivalPoint['distance']
            metaData['totalInfractions'] = djk.distTo(paths, arrivalPoint['id'])
            lt.addLast(filtered, datum)
    metaData["map"] = lt.size(foliumMap) > 0
    metaData["path"] = "req7"
    req8(foliumMap, "req7", drawPath)
    return filtered, metaData

def req8(events, path, drawPath):
    eventsMap = folium.Map((4.7110, -74.0721), zoom_start= 11)
    mark = MarkerCluster()
    for event in lt.iterator(events):
        mark.add_child(folium.Marker(event['coordinates'], popup= createPopUp(event)))
    eventsMap.add_child(mark)
    for draw in drawPath:
        folium.PolyLine(draw, color="red", weight=2.5, opacity=1).add_to(eventsMap)
    eventsMap.save(f'{path}.html')

def getClosestVertex(dataStructs, coordinates):
    closestVertex = None
    for vertex in lt.iterator(dataStructs['vertices']):
        distance = haversine(coordinates, vertex['coordinates'])
        if not closestVertex or distance < closestVertex['distance']:
            closestVertex = {'id': vertex['id'], 'distance': distance}
    return closestVertex

def isInside(dataStructs, coordinates):
    latitudes = dataStructs['metaData']['latitudes']
    longitudes = dataStructs['metaData']['longitudes']
    return latitudes[0] <= coordinates[0] <= latitudes[1] and longitudes[0] <= coordinates[1] <= longitudes[1]

def createMstGraph(mst):
    mstGraph = gr.newGraph()
    while not qu.isEmpty(mst['mst']):
        edge = qu.dequeue(mst['mst'])
        if not gr.containsVertex(mstGraph, edge['vertexA']):
            gr.insertVertex(mstGraph, edge['vertexA'])
        if not gr.containsVertex(mstGraph, edge['vertexB']):
            gr.insertVertex(mstGraph, edge['vertexB'])
        gr.addEdge(mstGraph, edge['vertexA'], edge['vertexB'], edge['weight'])
    return mstGraph

def existsStep(filtered, datum):
    for step in lt.iterator(filtered):
        if step['Starting Point'] == datum['Starting Point'] and step['Arrival Point'] == datum['Arrival Point']:
            return True
        if step['Starting Point'] == datum['Arrival Point'] and step['Arrival Point'] == datum['Starting Point']:
            return True
    return False

def getClosestStation(dataStructs, paths):
    closestStation = None
    for station in lt.iterator(dataStructs['stations']):
        if djk.hasPathTo(paths, station['VERTICES']):
            if not closestStation or djk.distTo(paths, station['VERTICES']) < djk.distTo(paths, closestStation['VERTICES']):
                closestStation = station
    return closestStation

def createPopUp(register):
    popUp = '<p class="fs-5" style="color: #03a7bb;">Details</p>'
    for key, value in register.items():
        popUp += f'<p><span class="fw-bold" style="color: #03a7bb;">{key.title()}:</span> {str(value).title() if value != "" else "Unavailable"}</p>'
    return f'<div style="width: 200px;">{popUp}</div>'

# Funciones utilizadas para comparar elementos dentro de una lista
def compareByCount(registerA, registerB):
    return registerA['count'] > registerB['count']

def compareByCode(registerA, registerB):
    return registerA['INFRACCION'] > registerB['INFRACCION']

def compareByServiceType(registerA, registerB):
    if registerA['TIPO_SERVICIO'] == 'Diplomático':
        return True
    elif registerA['TIPO_SERVICIO'] == 'Oficial' and registerB['TIPO_SERVICIO'] in ['Público', 'Particular']:
        return True
    elif registerA['TIPO_SERVICIO'] == 'Público' and registerB['TIPO_SERVICIO'] == 'Particular':
        return True
    return False

def compareBySeverity(registerA, registerB):
    if registerA['TIPO_SERVICIO'] == registerB['TIPO_SERVICIO']:
        return compareByCode(registerA, registerB)
    return compareByServiceType(registerA, registerB)

# Funciones de ordenamiento
def sortData(data, criteria):
    return sa.sort(data, criteria)

def sortInfractions(dataStructs):
    sortData(dataStructs['infractions'], compareBySeverity)

def getNData(data, N):
    if lt.size(data) <= N:
        return data
    return lt.subList(data, 1, N)

def firstAndLastNData(data, N):
    dataSize = lt.size(data)
    if dataSize <= N*2:
        return data
    filtered = lt.subList(data, 1, N)
    for register in lt.iterator(lt.subList(data, dataSize-N+1, N)):
        lt.addLast(filtered, register)
    return filtered
