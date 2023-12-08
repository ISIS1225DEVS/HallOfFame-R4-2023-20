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
from math import radians, sin, cos, sqrt, atan2
import sys
from datetime import datetime, timedelta
import re
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    analyzer={
        "Grafo_Malla_Vial":None,
        "Malla_Vial":None,
        "comparendo_mapa":None,
        "distancias_mapa":None,
        "Comparendos":None,
        "Estaciones de policia":None,
    }
    analyzer['Grafo_distancias'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed= False,
                                              size=228046,
                                              cmpfunction=compare)
    analyzer['Grafo_comparendos'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=228046,
                                              cmpfunction=compare)
    analyzer['Malla_Vial'] = mp.newMap(numelements=228046,
                                     maptype='PROBING',
                                     cmpfunction=compare)
    analyzer['Comparendos'] = lt.newList(datastructure='ARRAY_LIST')
    analyzer['Estaciones de policia'] = lt.newList(datastructure='ARRAY_LIST')
    analyzer['vertices'] = mp.newMap(numelements=228046,
                                     maptype='PROBING',
                                     cmpfunction=compare)
    
    analyzer['MapComparendos_clases'] = mp.newMap(numelements=228046, 
                                            maptype='PROBING',
                                            cmpfunction=compare)
    analyzer["Gravedad_comparendos"] = mp.newMap(numelements=228046, 
                                            maptype='PROBING')
    return analyzer


# Funciones para agregar informacion al modelo

def add_vertex(model, vertice):
    """
    Función para agregar nuevos elementos a la lista
    """
    Grafo_Malla_Vial = model['Grafo_distancias']
    Grafo_comparendos = model['Grafo_comparendos']
    Malla_Vial = model['Malla_Vial']
    lista = vertice.split(',')
    id = lista[0]
    long = float(lista[1])
    lat = float(lista[2])
    gr.insertVertex(Grafo_Malla_Vial, id)
    gr.insertVertex(Grafo_comparendos, id)
    mp.put(Malla_Vial, id, {'id': id, 'lat': lat, 'long': long, 'distancia': lt.newList(datastructure='ARRAY_LIST'), 'comparendos': lt.newList(datastructure='ARRAY_LIST'), 'estaciones': lt.newList(datastructure='ARRAY_LIST')})
    mp.put(model['vertices'], vertice, id)
    
def add_MapClases(model, comparendo, clase):
    dates = model['MapComparendos_clases']
    ExistDate = mp.contains(dates, clase)
    if ExistDate == True:
        entry = mp.get(dates, clase)
        torneo_i = me.getValue(entry)
    else:
        torneo_i = newClaseEntry(clase)
        mp.put(dates, clase , torneo_i)
    lt.addLast(torneo_i['datos'], comparendo)

def newClaseEntry(clase):
    entry = {}
    entry['clase'] = clase
    entry['datos'] = lt.newList('ARRAY_LIST')
    return entry
# Agrega los comparendos a la malla vial

def add_comparendo(model, comparendo):
    Malla_Vial = model['Malla_Vial']
    vertice = comparendo['VERTICES']
    vertice_cercano = mp.get(Malla_Vial, vertice)
    vertice_cercano = me.getValue(vertice_cercano)
    lt.addLast(vertice_cercano['comparendos'], comparendo)
    lt.addLast(model['Comparendos'], comparendo)

    
def add_estacion(model, estacion):
    Malla_Vial = model['Malla_Vial']
    vertice = estacion['VERTICES']
    vertice_cercano = mp.get(Malla_Vial, vertice)
    vertice_cercano = me.getValue(vertice_cercano)
    lt.addLast(vertice_cercano['estaciones'], estacion)
    lt.addLast(model['Estaciones de policia'], estacion)
    
# Funciones para creacion de datos

def add_arco(model, lista_adj):
    lista_adj = lista_adj.split(' ')
    nodo_principal = lista_adj[0]
    if len(lista_adj) > 1:
        for i in range(1, len(lista_adj)):
            nodo = lista_adj[i]
            nodo = replace(nodo)
            nodo_principal = replace(nodo_principal)
            peso_c = peso_comparendos(model, nodo_principal, nodo)
            gr.addEdge(model['Grafo_comparendos'], nodo_principal, nodo, peso_c)
            peso_d = peso_distancias(model, nodo_principal, nodo)
            gr.addEdge(model['Grafo_distancias'], nodo_principal, nodo, peso_d)

def peso_comparendos(model, nodo_principal, nodo):
    mapa = model['Malla_Vial']
    comparendos_principal = mp.get(mapa, nodo_principal)
    comparendos_principal = me.getValue(comparendos_principal)
    comparendos_principal = lt.size(comparendos_principal['comparendos'])
    comparendos_nodo = mp.get(mapa, nodo)
    comparendos_nodo = me.getValue(comparendos_nodo)
    comparendos_nodo = lt.size(comparendos_nodo['comparendos'])
    peso = comparendos_principal + comparendos_nodo
    return peso
        
def peso_distancias(model, nodo_principal, nodo):
    mapa = model['Malla_Vial']
    lat_principal = mp.get(mapa, nodo_principal)
    lat_principal = me.getValue(lat_principal) 
    lat_principal = lat_principal['lat']
    long_principal = mp.get(mapa, nodo_principal)
    long_principal = me.getValue(long_principal)
    long_principal = long_principal['long']
    lat_nodo = mp.get(mapa, nodo)
    lat_nodo = me.getValue(lat_nodo) #ACA ESTA EL ERROR
    lat_nodo = lat_nodo['lat']
    long_nodo = mp.get(mapa, nodo)
    long_nodo = me.getValue(long_nodo)
    long_nodo = long_nodo['long']
    peso = haversine(lat_principal, long_principal, lat_nodo, long_nodo)
    return peso

def replace(nodo):
    nodo = nodo.replace('\n', '')  
    return nodo

def add_gravedad(model, comparendo):
    comparendos = model['Gravedad_comparendos']
    ExistDate = mp.contains(comparendos, comparendo["TIPO_SERVICIO"])
    if ExistDate == True:
        entry = mp.get(comparendos, comparendo["TIPO_SERVICIO"])
        torneo_i = me.getValue(entry)
        lt.addLast(torneo_i, comparendo)
    else:
        torneo_i = lt.newList("ARRAY_LIST")
        lt.addLast(torneo_i, comparendo)
        mp.put(comparendos, comparendo["TIPO_SERVICIO"] , torneo_i)
    
    
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


def req_1(model, lat1, long1, lat2, long2)  :
    """
    Función que soluciona el requerimiento 1
    """
    Malla_Vial = model['Malla_Vial']
    Grafo_distancias = model['Grafo_distancias']
    vertices = model['vertices']
    lat1 = float(lat1)
    long1 = float(long1)
    lat2 = float(lat2)
    long2 = float(long2)
    distancia_minima_1 = 1000000
    distancia_minima_2 = 1000000
    vertice1 = None
    vertice2 = None
    vertices = mp.keySet(vertices)
    for vertice in lt.iterator(vertices):
        vertice_i = vertice.split(",")
        long_i = float(vertice_i[1])
        lat_i = float(vertice_i[2])
        distancia1 = haversine(lat1, long1, lat_i, long_i)
        distancia2 = haversine(lat2, long2, lat_i, long_i)
        if distancia1 < distancia_minima_1:
            distancia_minima_1 = distancia1
            vertice1 = vertice_i[0]
        if distancia2 < distancia_minima_2:
            distancia_minima_2 = distancia2
            vertice2 = vertice_i[0]

    search = bfs.BreathFirstSearch(Grafo_distancias, vertice1)
      
    if bfs.hasPathTo(search, vertice2):
        respuesta = bfs.pathTo(search, vertice2)
    
    lista = lt.newList(datastructure='ARRAY_LIST')
    for i in lt.iterator(respuesta):
        lt.addFirst(lista, i)
    i = 1
    peso = 0
    
    for vertice in lt.iterator(lista):
        if i < lt.size(lista):
            prox_vertice = lt.getElement(lista, i+1)
            peso = peso + float(gr.getEdge(Grafo_distancias, vertice, prox_vertice)['weight'])
        i += 1
    totalVertices = lt.size(respuesta)  
    return respuesta, totalVertices, peso, vertice1, vertice2
    
    
def req_2(data_structs, lat_inicio, long_inicio, lat_destino, long_destino):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    grafo = data_structs["Grafo_distancias"]
    vertices = data_structs['vertices']
    vertices = mp.keySet(vertices)
    distancia_minima_1 = 100000000
    distancia_minima_2 = 100000000
    for vertice in lt.iterator(vertices):
        vertice_i = vertice.split(",")
        long_i = float(vertice_i[1])
        lat_i = float(vertice_i[2])
        distancia1 = haversine(lat_inicio, long_inicio, lat_i, long_i)
        distancia2 = haversine(lat_destino, long_destino, lat_i, long_i)
        if distancia1 < distancia_minima_1:
            distancia_minima_1 = distancia1
            vertice_inicio = vertice_i[0]
        if distancia2 < distancia_minima_2:
            distancia_minima_2 = distancia2
            vertice_final = vertice_i[0]
    busqueda = bfs.BreathFirstSearch(grafo, vertice_inicio)
    if bfs.hasPathTo(busqueda,vertice_final):
        pasos = bfs.pathTo(busqueda,vertice_final)
        
    lista = lt.newList(datastructure='ARRAY_LIST')
    for i in lt.iterator(pasos):
        lt.addFirst(lista, i)
    i = 1
    peso = 0    
    for vertice in lt.iterator(lista):
        if i < lt.size(lista):
            prox_vertice = lt.getElement(lista, i+1)
            peso = peso + float(gr.getEdge(grafo, vertice, prox_vertice)['weight'])
        i += 1
    return peso,lt.size(pasos),lista["elements"]
    


def req_3(model, M, localidad):
    """
    Función que soluciona el requerimiento 1
    """
    vertices_localidad = lt.newList(datastructure='ARRAY_LIST')
    Malla_Vial = model['Malla_Vial']
    Grafo_distancias = model['Grafo_distancias']
    lista_vertices = mp.valueSet(Malla_Vial)
    for vertice in lt.iterator(lista_vertices):
        if lt.size(vertice['comparendos']) > 0:
            dict = {}
            dict['comparendos'] = 0
            for comparendo in lt.iterator(vertice['comparendos']):  
                if comparendo['LOCALIDAD'] == localidad:
                    dict['id'] = vertice['id']
                    dict['comparendos'] = dict['comparendos'] + 1
            if dict['comparendos'] > 0:
                lt.addLast(vertices_localidad, dict)
                
    vertices_localidad = sort_comparendos(vertices_localidad)

    nodo_origen = lt.getElement(vertices_localidad, 1)['id']
    search = prim.PrimMST(Grafo_distancias, nodo_origen)
    i = 1
    arcos_camino = lt.newList(datastructure='ARRAY_LIST')
    for vertice in lt.iterator(vertices_localidad):
        if 1 < i < int(M):
            try:
                arcos = prim.edgesMST(search, vertice['id'])
                lt.addLast(arcos_camino, arcos)
            except Exception:
                print('No hay camino')
        i += 1
    return vertices_localidad, arcos_camino


def req_4(data_structs,M):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    grafo_distancias = data_structs["Grafo_distancias"]
    comparendos_graves= data_structs["Gravedad_comparendos"]
    lista_vertices_graves = lt.newList("ARRAY_LIST")
    dato_o = me.getValue(mp.get(comparendos_graves,"Oficial"))
    dato_o = quk.sort(dato_o,comparendos_iguales)
    for i in lt.iterator(dato_o):
        if lt.isPresent(lista_vertices_graves,i["VERTICES"])==0 and lt.size(lista_vertices_graves)<=int(M):
            lt.addLast(lista_vertices_graves,i["VERTICES"])  
    if lt.size(lista_vertices_graves)<=int(M):
        dato_pu = me.getValue(mp.get(comparendos_graves,"Público"))
        dato_pu = quk.sort(dato_pu,comparendos_iguales)
        for i in lt.iterator(dato_pu):
            if lt.isPresent(lista_vertices_graves,i["VERTICES"])==0 and lt.size(lista_vertices_graves)<=int(M):
                lt.addLast(lista_vertices_graves,i["VERTICES"])  
    
    if lt.size(lista_vertices_graves)<=int(M):
        dato_pa = me.getValue(mp.get(comparendos_graves,"Particular"))
        dato_pa = quk.sort(dato_pa,comparendos_iguales)
        for i in lt.iterator(dato_pa):
            if lt.isPresent(lista_vertices_graves,i["VERTICES"])==0 and lt.size(lista_vertices_graves)<=int(M):
                lt.addLast(lista_vertices_graves,i["VERTICES"])  
            
                        
    grafo_distancia_optima = djk.Dijkstra(grafo_distancias,lt.getElement(lista_vertices_graves,1))
    lt.deleteElement(lista_vertices_graves,1)
    kilometros = 0
    vertices_red = lt.newList("ARRAY_LIST")
    arcos_red = lt.newList("ARRAY_LIST")
    for i in lt.iterator(lista_vertices_graves):
        kilometros += djk.distTo(grafo_distancia_optima, i)
        camino = djk.pathTo(grafo_distancia_optima, i)
        for o in lt.iterator(camino):
            verticeA = o['vertexA']
            verticeB = o['vertexB']
            if lt.isPresent(vertices_red, verticeA) == 0:
                lt.addLast(vertices_red, verticeA)
            if lt.isPresent(vertices_red, verticeB) == 0:
                lt.addLast(vertices_red, verticeB)
            opcion_1 = str(verticeA) + '-' + str(verticeB)
            if lt.isPresent(arcos_red, opcion_1) == 0:
                lt.addLast(arcos_red, opcion_1)
    costo = 1000000*kilometros
    return lt.size(vertices_red),vertices_red["elements"],kilometros,costo

def comparendos_iguales(comparendo1,comparendo2):
    if comparendo1["INFRACCION"]>comparendo2["INFRACCION"]:
        return True
    else:
        return False
    
def req_5(data_structs, m, clase):

    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    
    # obtencion vertices con mayor numero de comparendos
    MapClases = data_structs['MapComparendos_clases']
    entry = mp.get(MapClases, clase)
    listaComparendos = me.getValue(entry)['datos']
    
    mapVertices = mp.newMap(numelements=228046, maptype='PROBING', cmpfunction=compare)
    for comparendo in lt.iterator(listaComparendos):
        vertice = comparendo['VERTICES']
        vertice_cercano = mp.get(mapVertices, vertice)
        if vertice_cercano == None:
            entry = entryREQ5(vertice)
            mp.put(mapVertices, vertice, entry)
        else:
            entry = me.getValue(vertice_cercano)
            
        lt.addLast(entry['comparendos'], comparendo)
        entry['Tcomparendos'] += 1
    lstEntrys = lt.newList(datastructure='ARRAY_LIST')
    listaVertices = mp.keySet(mapVertices)
    
    for vertice in lt.iterator(listaVertices):
        entry = me.getValue(mp.get(mapVertices, vertice))
        lt.addLast(lstEntrys, entry)
    
    sortedlst = se.sort(lstEntrys, sort_criteriaREQ5)

    SubListaVertices = lt.subList(sortedlst, 1,int(m))
    
    # Creacion red de comunicaciones
    
    origen = lt.getElement(SubListaVertices, 1)['vertice']
    search = djk.Dijkstra(data_structs['Grafo_distancias'], origen)
    distancia_total = 0
    sublistaSinOrigen = lt.subList(SubListaVertices, 2, lt.size(SubListaVertices) - 1)
    
    listaVerticesRed = lt.newList('ARRAY_LIST')
    listaArcosRed = lt.newList('ARRAY_LIST')
    
    for vertice in lt.iterator(sublistaSinOrigen):
            verticeD = vertice['vertice']
            comparendos = vertice['comparendos']
            Tcomparendos = vertice['Tcomparendos']
            distancia = djk.distTo(search, verticeD)
            distancia_total += distancia
            camino = djk.pathTo(search, verticeD)
            for verticeID in lt.iterator(camino):
                verticeA = verticeID['vertexA']
                verticeB = verticeID['vertexB']
                if lt.isPresent(listaVerticesRed, verticeA) == 0:
                    lt.addLast(listaVerticesRed, verticeA)
                if lt.isPresent(listaVerticesRed, verticeB) == 0:
                    lt.addLast(listaVerticesRed, verticeB)
                aeco = str(verticeA) + '-' + str(verticeB)
                if lt.isPresent(listaArcosRed, aeco) == 0:
                    lt.addLast(listaArcosRed, aeco)
    
    precio = 1000000 * distancia_total
    formato ="${:,.2f}".format(float(precio))
    return listaVerticesRed, listaArcosRed, distancia_total, formato, SubListaVertices


def entryREQ5(vertice):
    entry = {}
    entry['vertice'] = vertice
    entry['comparendos'] = lt.newList(datastructure='ARRAY_LIST')
    entry['Tcomparendos'] = 0
    return entry

def sort_criteriaREQ5(entry1, entry2):
    entry1 = entry1['Tcomparendos']
    entry2 = entry2['Tcomparendos']
    if entry1 > entry2:
        return True
    else: 
        return False



def req_6(data_structs, m):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    solucion = lt.newList(datastructure='ARRAY_LIST')
    lista_comparendos  = data_structs['Comparendos']
    lista_comisarias = data_structs['Estaciones de policia']
    grafo_distancias = data_structs['Grafo_distancias']
    sorted_comaprendos = sa.sort(lista_comparendos, sort_criteriaREQ6)
    seleccionComparendos = lt.subList(sorted_comaprendos, 1, int(m))
    mapaaux = mp.newMap(numelements=100, maptype='PROBING', cmpfunction=compare)
    
    for comparendo in lt.iterator(seleccionComparendos):
        estacionCercana = comisaria_cercanas(data_structs, comparendo)
        if not(mp.contains(mapaaux, estacionCercana['VERTICES'])):
            entry = entryREQ6(estacionCercana)
            mp.put(mapaaux, estacionCercana['VERTICES'], entry)
        else:
            entry = me.getValue(mp.get(mapaaux, estacionCercana['VERTICES']))
        lt.addLast(entry['comparendos'], comparendo)

    listaEstaciones = mp.keySet(mapaaux)
    for estacion in lt.iterator(listaEstaciones):
        search = djk.Dijkstra(grafo_distancias, estacion)
        entry = mp.get(mapaaux, estacion)
        listaComp = me.getValue(entry)['comparendos']
        for comparendo in lt.iterator(listaComp):
            formato = {}
            vertice = comparendo['VERTICES']
            camino = djk.pathTo(search, vertice)
            vertextotal = lt.size(camino)
            distancia = djk.distTo(search, vertice)
            formato['verticesTotales'] = vertextotal
            listaVerticesCamino = lt.newList('ARRAY_LIST')
            listaArcosCamino = lt.newList('ARRAY_LIST')
            for verticeID in lt.iterator(camino):
                verticeA = verticeID['vertexA']
                verticeB = verticeID['vertexB']
                if lt.isPresent(listaVerticesCamino, verticeA) == 0:
                    lt.addLast(listaVerticesCamino, verticeA)
                if lt.isPresent(listaVerticesCamino, verticeB) == 0:
                    lt.addLast(listaVerticesCamino, verticeB)
                aeco = str(verticeA) + '-' + str(verticeB)
                if lt.isPresent(listaArcosCamino, aeco) == 0:
                    lt.addLast(listaArcosCamino, aeco)
            formato['listaVerticesCamino'] = listaVerticesCamino
            formato['listaArcosCamino'] = listaArcosCamino
            formato['distancia'] = distancia
            formato['comparendo'] = comparendo
            lt.addLast(solucion, formato)
    return solucion
            
        
            
                     

def entryREQ6(estacion):
    entry = {}
    entry['estacion'] = estacion
    entry['comparendos'] = lt.newList(datastructure='ARRAY_LIST')
    return entry

def comisaria_cercanas(data_structs, comparendo):
    listacomisarias = data_structs['Estaciones de policia']
    distancia_minima = 100000000
    comisaria_cercana = None
    for comisaria in lt.iterator(listacomisarias):
        latComi = float(comisaria['EPOLATITUD'])
        longComi = float(comisaria['EPOLONGITU'])
        latComp = float(comparendo['LATITUD'])
        longComp = float(comparendo['LONGITUD'])
        distancia = haversine(latComi, longComi, latComp, longComp)
        if distancia < distancia_minima:
            distancia_minima = distancia
            comisaria_cercana = comisaria
            
    return comisaria_cercana
        

def ddsort_criteriaREQ6(entry1, entry2):
    tipoServicio1 = entry1['TIPO_SERVICIO']
    tipoServicio2 = entry2['TIPO_SERVICIO']
    tipoServicio1 = 3 if tipoServicio1 == 'Público' else 2 if tipoServicio1 == 'Oficial' else 1 if tipoServicio1 == 'Particular' else 0
    tipoServicio2 = 3 if tipoServicio2 == 'Público' else 2 if tipoServicio2 == 'Oficial' else 1 if tipoServicio2 == 'Particular' else 0
    
    mayor = comparar_infracciones(entry1['INFRACCION'], entry2['INFRACCION'])
    
    if tipoServicio1 > tipoServicio2:
        return True
    elif tipoServicio1 == tipoServicio2:
        if mayor == -1:
            return True
        else:
            return False
    
    return False

    
def comparar_infracciones(codigo1, codigo2):
    letra1, numero1_str = codigo1[0], codigo1[1:]
    letra2, numero2_str = codigo2[0], codigo2[1:]

    # Eliminar ceros iniciales y manejar cadena vacía
    numero1 = int(numero1_str.lstrip('0')) if numero1_str else 0
    numero2 = int(numero2_str.lstrip('0')) if numero2_str else 0
    
    if letra1 < letra2:
        return 1
    elif letra1 > letra2:
        return -1
    else:
        if numero1 < numero2:
            return 1
        elif numero1 > numero2:
            return -1
        else:
            return 0


def req_7(data_structs,lat_inicio, long_inicio, lat_destino, long_destino):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    grafo = data_structs["Grafo_distancias"]
    grafo_busqueda = data_structs["Grafo_comparendos"]
    vertices = data_structs['vertices']
    vertices = mp.keySet(vertices)
    distancia_minima_1 = 100000000
    distancia_minima_2 = 100000000
    for vertice in lt.iterator(vertices):
        vertice_i = vertice.split(",")
        long_i = float(vertice_i[1])
        lat_i = float(vertice_i[2])
        distancia1 = haversine(lat_inicio, long_inicio, lat_i, long_i)
        distancia2 = haversine(lat_destino, long_destino, lat_i, long_i)
        if distancia1 < distancia_minima_1:
            distancia_minima_1 = distancia1
            vertice_inicio = vertice_i[0]
        if distancia2 < distancia_minima_2:
            distancia_minima_2 = distancia2
            vertice_final = vertice_i[0]
            
    busqueda = djk.Dijkstra(grafo_busqueda, vertice_inicio)
    if djk.hasPathTo(busqueda,vertice_final):
        pasos = djk.pathTo(busqueda,vertice_final)

    vertices = lt.newList("ARRAY_LIST")
    arcos = lt.newList("ARRAY_LIST")
    cantidad_comparendos = djk.distTo(busqueda,vertice_final)
    for o in lt.iterator(pasos):
        verticeA = o['vertexA']
        verticeB = o['vertexB']
        if lt.isPresent(vertices, verticeA) == 0:
            lt.addLast(vertices, verticeA)
        if lt.isPresent(vertices, verticeB) == 0:
            lt.addLast(vertices, verticeB)
        opcion_1 = str(verticeA) + '-' + str(verticeB)
        if lt.isPresent(arcos, opcion_1) == 0:
            lt.addLast(arcos, opcion_1)
    total_vertices = lt.size(vertices)
    cantidad_kilometros = 0
    
    for edge in lt.iterator(arcos):
        arco = gr.getEdge(grafo, edge.split("-")[0], edge.split("-")[1])
        distancia = arco["weight"]
        cantidad_kilometros += distancia
        
    return total_vertices,vertices["elements"],arcos["elements"],cantidad_comparendos,cantidad_kilometros


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass

def haversine(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    R = 6371.0
    
    # Convierte las coordenadas de grados a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Diferencias de coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Fórmula de Haversine
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distancia en kilómetros
    distance = R * c

    return distance

# Funciones utilizadas para comparar elementos dentro de una lista

def compare(stop, keyvaluestop):
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

def compareLatLong(date1, date2):
    date1 = float(date1)
    date2 = float(date2)
    
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
    
# Funciones de ordenamiento


def sort_criteria(date_1, date_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    date_1 = date_1["FECHA_HORA"]
    date_2 = date_2["FECHA_HORA"]
    if date_1 < date_2:
        return True
    else: 
        return False
     
def sort_criteria_comparendos(comp_1, comp_2):
    comp_1 = comp_1["comparendos"]
    comp_2 = comp_2["comparendos"]
    if comp_1 > comp_2:
        return True
    else: 
        return False

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    sub_list = lt.subList(data_structs["Comparendos"],1,lt.size(data_structs["Comparendos"]))
    quk.sort(sub_list, sort_criteria)
    data_structs["Comparendos"] = sub_list

def sort_comparendos(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    sub_list = lt.subList(data_structs,1,lt.size(data_structs))
    quk.sort(sub_list, sort_criteria_comparendos)
    data_structs = sub_list
    return data_structs

