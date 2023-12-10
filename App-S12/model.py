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


def newCatalog():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    catalog = { "comparendos": None,
               "estaciones_policias": None,
               "vertices": None,
               "arcos": None,
               "hash_ids" : None,
               "malla_vial" : None,
               "grafo_comparendo":None
               }

    catalog["comparendos"] = lt.newList("ARRAY_LIST")
    catalog["estaciones_policias"] = lt.newList("ARRAY_LIST")
    catalog["vertices"] = lt.newList("ARRAY_LIST")
    catalog["arcos"] = lt.newList("ARRAY_LIST")
    catalog["hash_ids"] = mp.newMap(numelements=228046,
                                     maptype='PROBING')
    
    catalog["malla_vial"] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=228046,
                                        cmpfunction= compare_id
                                        )
    catalog["grafo_comparendos"] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=228046,
                                        )
    catalog["djk_estaciones"] = mp.newMap(numelements=21, maptype="PROBING", loadfactor=0.5, cmpfunction=compare_id)
    catalog["grafo_estaciones"] = mp.newMap(numelements=21, maptype="PROBING", loadfactor=0.5, cmpfunction=compare_id)
    
    return catalog
# Funciones para agregar informacion al modelo

#Funciones para la carga de datos, en especifico para las tablas, es decir, los array_list.
def add_comparendo(catalog, ticket):
    
    lt.addLast(catalog["comparendos"], ticket)
    return catalog

def add_estacion(catalog, estacion):
    lt.addLast(catalog["estaciones_policias"], estacion)
    mp.put(catalog["grafo_estaciones"], estacion["OBJECTID"], gr.newGraph(datastructure="ADJ_LIST", directed = False, cmpfunction = compare_id))
    return catalog
    
    
def add_vertice_array(catalog, fila, longitud, latitud):
    vertice  = ({"ID": fila[0], "Longitud": longitud , "Latitud": latitud})
    lt.addLast(catalog["vertices"],vertice)
    return catalog


def add_arco_array(catalog, arco):
    lt.addLast(catalog["arcos"],arco)
    return catalog
    


#Funciones para la creacion del grafo 

def add_hash(catalog, info):
    vertice = info[0]
    info_vertx = {'info':info[1:],'comparendos':[],'estaciones':[], "closest_estacion":None}
    info_vertx["closest_estacion"] = closest_estacion(catalog, info[2], info[1])
    entry = mp.get(catalog['hash_ids'], vertice)
    if entry is None:
        mp.put(catalog['hash_ids'], vertice, info_vertx)
    return catalog
    

            
def add_vertice_malla(catalog,info):
    
    try:
        add_hash(catalog, info)
        vertice = formatVertex(info)
        if not gr.containsVertex(catalog['malla_vial'], vertice):
            gr.insertVertex(catalog['malla_vial'], vertice)
        return catalog
    except :
        print("Error al agregar el vertice a la malla vial")

def add_vertice_comparendos(catalog,info):
    try:
        vertice = formatVertex(info)
        if not gr.containsVertex(catalog['grafo_comparendos'], vertice):
            gr.insertVertex(catalog['grafo_comparendos'], vertice)
        return catalog
    except :
        print("Error al agregar el vertice a la malla vial")

def add_grafo_comparendo(catalog,vertice):
    
    info = {
    "LOCALIDAD": vertice["LOCALIDAD"],
    "LATITUD": vertice['LATITUD'],
    "LONGITUD": vertice['LONGITUD'],
    "FECHA_HORA": vertice['FECHA_HORA'],
    "MEDIO_DETECCION": vertice['MEDIO_DETECCION'],
    "CLASE_VEHICULO": vertice['CLASE_VEHICULO'],
    "TIPO_SERVICIO": vertice['TIPO_SERVICIO'],
    "INFRACCION": vertice['INFRACCION'],
    "DES_INFRACCION": vertice['DES_INFRACCION']
    }
    entry = mp.get(catalog['hash_ids'], vertice['VERTICES'])
    info_vertx = me.getValue(entry)
    info_vertx['comparendos'].append(info)
    
    return catalog
    
def add_grafo_estacion(catalog,vertice):
    
    info = {
    "LATITUD": vertice["EPOLATITUD"],
    "LONGITUD": vertice["EPOLONGITU"],
    "DESCRIPCION": vertice["EPODESCRIP"],
    "SITIO": vertice["EPODIR_SITIO"],
    "HORARIO": vertice["EPOHORARIO"],
    "TELEFONO": vertice["EPOTELEFON"],
    "CORREO": vertice["EPOCELECTR"],
    }
    entry = mp.get(catalog['hash_ids'], vertice['VERTICES'])
    info_vertx = me.getValue(entry)
    info_vertx['estaciones'].append(info)
    
    return catalog

def add_arco(catalog, info):
    size =len(info)
    if size > 1:
        #Calcula el vertice de inicio, y la longitud y latitud del mismo
        vertx_inicio = info[0]
        longitud1, latitud1, estacion1 = lat_long_vertx(catalog, vertx_inicio)
        #Pasa longitud y latitud a radianes
        longitud_1r = float(longitud1) * math.pi / 180
        latitud_1r = float(latitud1) * math.pi / 180
        #Calcula las conecciones con los demas vertices
        conexiones = info[1:]
        for vertx in conexiones:
            longitud2, latitud2, estacion2 = lat_long_vertx(catalog, vertx)
            longitud_2r = float(longitud2) * math.pi / 180
            latitud_2r = float(latitud2) * math.pi / 180
            #Calcula la distancia Haversine 
            distancia = distance( latitud_1r, latitud_2r, longitud_1r, longitud_2r )
            #Añade el arco con el peso, que en esta caso es la distancia entre los dos vertices
            add_edge(catalog["malla_vial"], vertx_inicio, vertx, distancia)
            #Calcula el total de comparendos
            t_comparendos = comparendos_entre_vertices(catalog, vertx_inicio, vertx)
            #Anade el arco con el peso de los comparendos
            add_edge(catalog["grafo_comparendos"],vertx_inicio, vertx, t_comparendos)
            add_edge_estaciones(catalog, vertx_inicio, vertx, estacion1, estacion2, distancia)
            
    return catalog





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


def req_1(catalog, vertices, lat1, long1, lat2, long2):
    """
    Función que soluciona el requerimiento 1
    """
    try:
        mapa_ids = catalog["hash_ids"]
        malla_vial = catalog["malla_vial"]
        distancia_total = 0 
        total_vertx = 0
        camino_total = lt.newList("ARRAY_LIST")
        lista_bono = []
        vertice_destino = closest_vertx(vertices, lat1, long1)
        vertice_origen = closest_vertx(vertices, lat2, long2)
        search = dfs.DepthFirstSearch(malla_vial, vertice_origen)
        haspath = dfs.hasPathTo(search, vertice_destino)

        if haspath:
            camino = dfs.pathTo(search, vertice_destino)
            prev = None
            for vertice in lt.iterator(camino):
                lat, long = lat_long_bono(mapa_ids,vertice)
                lista_bono.append((lat,long))
                total_vertx +=1
                lt.addLast(camino_total,vertice)
                if prev is not None:
                    arco = gr.getEdge(malla_vial, vertice, prev)
                    peso = arco["weight"]
                    distancia_total += peso
                prev = vertice
        
        req_8(lista_bono, 1)
    except:
        print("Error, revise nuevamente los datos")
    return camino_total,distancia_total,total_vertx 

            
def req_2(catalog, vertices, lat1, long1, lat2, long2):
    """
    Función que soluciona el requerimiento 2
    """
   
    mapa_ids = catalog["hash_ids"]
    malla_vial = catalog["malla_vial"]
    distancia_total = 0 
    total_vertx = 0
    camino_total = lt.newList("ARRAY_LIST")
    lista_bono = []
    
    vertice_origen = closest_vertx(vertices, lat1, long1)
    vertice_destino = closest_vertx(vertices, lat2, long2)
    search = bfs.BreathFirstSearch(malla_vial, vertice_origen)
    haspath = bfs.hasPathTo(search, vertice_destino)

    if haspath:
        camino = bfs.pathTo(search, vertice_destino)
        prev = None
        for vertice in lt.iterator(camino):
            lat, long = lat_long_bono(mapa_ids,vertice)
            lista_bono.append((lat,long))
            total_vertx +=1
            lt.addLast(camino_total,vertice)
            if prev is not None:
                arco = gr.getEdge(malla_vial, vertice, prev)
                peso = arco["weight"]
                distancia_total += peso
            prev = vertice
    
    req_8(lista_bono, 2)
    return camino_total,distancia_total,total_vertx
   


def req_3(catalog,vertices,cantidadCamaras,localidad):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    mapa_ids = catalog["hash_ids"]
    graf= catalog["grafo_comparendos"]
    camino_Total= lt.newList("ARRAY_LIST")
    lista=catalog["comparendos"]
    Latitud=[]
    Longitud=[]
    lista_bono=[]
    distancia_total = 0 
    total_vertx = 0
    for i in lt.iterator(lista):
        if i["LOCALIDAD"]== localidad:
            Latitud.append(i["LATITUD"])
            Longitud.append(i["LONGITUD"])
 
    vertice_origen = closest_vertx(vertices, Latitud[0], Longitud[0])
    vertice_final= closest_vertx(vertices, Latitud[len(Latitud)-1], Longitud[len(Latitud)-1])
    search = bfs.BreathFirstSearch(graf, vertice_origen)
    haspath = bfs.hasPathTo(search, vertice_final)
    if haspath:
        camino = bfs.pathTo(search, vertice_final)
        prev = None
        for vertice in lt.iterator(camino):
            lat, long = lat_long_bono(mapa_ids,vertice)
            lista_bono.append((lat,long))
            total_vertx +=1
            lt.addLast(camino_Total,vertice)
            if prev is not None:
                arco = gr.getEdge(graf, vertice, prev)
                peso = arco["weight"]
                distancia_total += peso
            prev = vertice
    req_8(lista_bono,3)   
    return camino_Total
    

  
    


def req_4(catalog, comparendos_ordenados, camaras, bono):
    """
    Función que soluciona el requerimiento 4
    """
    lista_bono = []
    arcos = lt.newList("ARRAY_LIST")
    vertices = lt.newList("ARRAY_LIST")
    i = 2
    g_distancia = catalog["malla_vial"]
    mayor_gravedad = lt.firstElement(comparendos_ordenados)
    print("Cargando MST...")
    search = prim.PrimMST(g_distancia, mayor_gravedad["VERTICES"])
    peso = prim.weightMST(g_distancia, search)
    
    subgrafo = gr.newGraph(datastructure="ADJ_LIST", directed = False, cmpfunction = compare_id)
    mst = search["mst"]
    print("Reconstruyendo el grafo...")
    for minicamino in lt.iterator(mst):
        add_vertx(subgrafo, minicamino["vertexA"])
        add_vertx(subgrafo, minicamino["vertexB"])
        add_edge(subgrafo, minicamino["vertexA"], minicamino["vertexB"], minicamino["weight"])
    
    sub_bfs = bfs.BreathFirstSearch(subgrafo, mayor_gravedad["VERTICES"])
    grafo_camaras = gr.newGraph(datastructure="ADJ_LIST", directed = False, cmpfunction = compare_id)
    print("Filtrando las  M camaras...")
    
    while i <= camaras:
        info_c = lt.getElement(comparendos_ordenados, i)
        camino = bfs.pathTo(sub_bfs, info_c["VERTICES"])
        prev = None
        for vertice in lt.iterator(camino):
            if prev == None:
                lt.addLast(vertices, vertice)
                prev = vertice
            else:
                minipath = {"vertexA" : prev, "vertexB": vertice,"weight" : 0 }
                prev = vertice
                v1 = minipath["vertexA"]
                v2 = minipath["vertexB"]
                v1_info = me.getValue(mp.get(catalog["hash_ids"], v1))["info"]
                v2_info = me.getValue(mp.get(catalog["hash_ids"], v2))["info"]
                lat1_bono = float(v1_info[1])
                long1_bono = float(v1_info[0])
                lat2_bono = float(v2_info[1])
                long2_bono = float(v2_info[0])
                minipath["weight"] = distance(lat1_bono, long1_bono ,lat2_bono, long2_bono)

                if not gr.getEdge(grafo_camaras, minipath["vertexA"], minipath["vertexB"]):
                    lt.addLast(arcos, minipath)
                    peso += minipath["weight"]
                if not gr.containsVertex(grafo_camaras, minipath["vertexA"]):
                    lt.addLast(vertices, minipath["vertexA"])
                if not gr.containsVertex(grafo_camaras, minipath["vertexB"]):
                    lt.addLast(vertices, minipath["vertexB"])
                add_vertx(grafo_camaras, minipath["vertexA"])
                add_vertx(grafo_camaras, minipath["vertexB"])
                add_edge(grafo_camaras, minipath["vertexA"], minipath["vertexB"], minipath["weight"])
                if bono:
                    lista_bono.append([[lat1_bono,long1_bono], [lat2_bono,long2_bono]])
        i +=1
    if bono:
        req_8(lista_bono, 4)
    return vertices, arcos, peso
                
def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(catalog, numero_comparendos, comparendos_ordenados, bono):
    """
    Función que soluciona el requerimiento 6
    """
    bono = bono_check(bono)
    map_stations = catalog["djk_estaciones"]
    i = 0
    lista_bono = []
    camino_total = lt.newList("ARRAY_LIST")
    while i <= numero_comparendos:
        print("Obteniendo  camino de comparendo #" + str(i))
        info_comparendo = lt.getElement(comparendos_ordenados, i)
        
        vertx_comparendo = info_comparendo["VERTICES"]
        info_vertx_comparendo = me.getValue(mp.get(catalog["hash_ids"], vertx_comparendo))
        closest_estacion_info= info_vertx_comparendo["closest_estacion"]
        if closest_estacion_info["EPONOMBRE"] is not None:
            entry = mp.get(map_stations, closest_estacion_info["EPONOMBRE"])
            if entry:
                search = me.getValue(entry)
            else:
                subgrafo = me.getValue(mp.get(catalog["grafo_estaciones"], closest_estacion_info["OBJECTID"]))
                search = djk.Dijkstra(subgrafo, closest_estacion_info["VERTICES"])
                mp.put(map_stations, closest_estacion_info["OBJECTID"], search)
            camino = djk.pathTo(search, info_comparendo["VERTICES"])
            info_camino = {
                "estacion": closest_estacion_info["EPONOMBRE"],
                "comparendo" : info_comparendo,
                "vertice_comparendo" : vertx_comparendo,
                "total_vertx" : 0,
                "identificadores" : [],
                "arcos" : [],
                "km" : 0       
            }
            lt.addLast(camino_total, info_camino)
            for minipath in lt.iterator(camino):
                info_camino["total_vertx"] += 1
                if len(info_camino["identificadores"]) == 0:
                    info_camino["identificadores"].append(minipath["vertexA"])
                info_camino["identificadores"].append(minipath["vertexB"])
                info_camino["km"] += minipath["weight"]
                info_camino["arcos"].append(minipath)
                if bono:
                    v1 = minipath["vertexA"]
                    v2 = minipath["vertexB"]
                    v1_info = me.getValue(mp.get(catalog["hash_ids"], v1))["info"]
                    v2_info = me.getValue(mp.get(catalog["hash_ids"], v2))["info"]
                    lat1_bono = v1_info[1]
                    long1_bono = v1_info[0]
                    lat2_bono = v2_info[1]
                    long2_bono = v2_info[0]
                    lista_bono.append([[lat1_bono,long1_bono], [lat2_bono,long2_bono]])
            
            i +=1
    if bono:
            req_8(lista_bono, 6)
    return camino_total
       

def req_7(catalog, vertices,  lat1, long1, lat2, long2, bono):
    """
    Función que soluciona el requerimiento 7
    """
    bono = bono_check(bono)
    total_multas = 0
    distancia_total = 0
    vertices_totales = 0
    camino_total = lt.newList("ARRAY_LIST")
    lista_bono = []
    
    g_comparendos = catalog["grafo_comparendos"]
    vertx_origen = closest_vertx(vertices, lat1, long1)
    vertx_destino = closest_vertx(vertices, lat2, long2)
    search = djk.Dijkstra(g_comparendos, vertx_origen)
    haspath = djk.hasPathTo(search, vertx_destino)

    if haspath:
        camino = djk.pathTo(search, vertx_destino )
        prev = None
        for vertice in lt.iterator(camino):
            vertices_totales += 1
            if prev == None:
                lt.addLast(camino_total, vertice["vertexA"])
            lt.addLast(camino_total, vertice["vertexB"])
            total_multas += vertice["weight"]
            v1 = vertice["vertexA"]
            v2 = vertice["vertexB"]
            v1_info = me.getValue(mp.get(catalog["hash_ids"], v1))["info"]
            v2_info = me.getValue(mp.get(catalog["hash_ids"], v2))["info"]
            lat1_bono = float(v1_info[1])
            long1_bono = float(v1_info[0])
            lat2_bono = float(v2_info[1])
            long2_bono = float(v2_info[0])
            distancia = distance(lat1_bono, long1_bono ,lat2_bono, long2_bono)
            distancia_total += distancia
            prev = vertice
            if bono:
                lista_bono.append([[lat1_bono,long1_bono], [lat2_bono,long2_bono]])
        if bono:
            req_8(lista_bono, 7)
    else:
        print("No hay camino")
    
    return distancia_total, vertices_totales, camino_total, total_multas
            
            
def req_8(lista_cords, req):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    mymap = folium.Map(location=[4.656184209192183, -74.10225554997007], zoom_start=12)
    name = "Req " + str(req) + " map.html"
    folium.PolyLine(locations=lista_cords, color='blue', opacity = 0.8).add_to(mymap)    
    mymap.save(name)

#FUNCIONES DE ORDENAMIENTO
def sort_List(lista, comparefunction):

   return merg.sort(lista, comparefunction)


# ==============================
# Funciones Helper
# ==============================
def closest_vertx(vertices, lat1, long1):
    long1 = float(long1) * math.pi / 180
    lat1= float(lat1) * math.pi / 180
    closest_vertx = None
    min_distance = None
    for vertice in lt.iterator(vertices):
        lat = vertice["Latitud"]
        long = vertice["Longitud"]
        lat = float(lat) * math.pi / 180
        long = float(long) * math.pi / 180
        new_distance = distance( lat1, lat, long1, long )
        if min_distance == None:
            min_distance = new_distance
        if new_distance < min_distance:
            min_distance = new_distance
            closest_vertx = vertice["ID"]
    return closest_vertx


def max_min(maxlong,minlong,maxlat,minlat,long,lat):
    
    if long > maxlong:
        maxlong = long
    if long < minlong:
        minlong = long
    if lat > maxlat:
        maxlat = lat
    if lat < minlat:
        minlat = lat
    return maxlong,minlong,maxlat,minlat


def formatVertex(columna):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    id_mall = columna[0]
    return id_mall

def lat_long_vertx(catalog,id_vertx):
    entry = mp.get(catalog["hash_ids"], id_vertx)
    vertx_info = me.getValue(entry)
    longitud = vertx_info["info"][0]
    latitud = vertx_info["info"][1] 
    clst = vertx_info["closest_estacion"]
    return longitud, latitud, clst

def comparendos_entre_vertices(catalog, initial_vertx, vertx2):
    entry = mp.get(catalog["hash_ids"], initial_vertx)
    vertx_info = me.getValue(entry)
    entry2 = mp.get(catalog["hash_ids"], vertx2)
    vertx_info2 = me.getValue(entry2)
    size1 = len(vertx_info['comparendos'])
    size2 = len(vertx_info2['comparendos'])
    total = size1 + size2
    return total

def bono_check(bono):
    if bono == 'si':
        bono = True
    else:
        bono = False
    return bono     
            
            
def distance( lat1, lat2, long1, long2 ):
    Distancia = 2 * math.asin(math.sqrt(math.sin((lat2 - lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((long2-long1)/2)**2)) * 6371
    return Distancia

def lat_long_bono(mapa,vertx_id):
    entry = mp.get(mapa, vertx_id)
    vertx_info = me.getValue(entry)
    lat = float(vertx_info['info'][1])
    long = float(vertx_info['info'][0])
    return lat,long

def sort_comparendos(lista):

    return merg.sort(lista, comparendos_criteria)


def comparendos_criteria(c1,c2):
    try: 
        prioridad = {
            "Diplomatico":4,
            "Oficial" : 3,
            "Publico": 2
        }
        if c1["INFRACCION"] in (None, '', ' ', 'Unknown') or c2["INFRACCION"] in (None, '', ' ', 'Unknown'):
            return False
        letra1 = c1["INFRACCION"][0]
        letra2 = c2["INFRACCION"][0]
        cod1 = int(c1["INFRACCION"].replace(letra1, ''))
        cod2 = int(c2["INFRACCION"].replace(letra2, ''))
        tipo1 = prioridad.get(c1["TIPO_SERVICIO"], 0)
        tipo2 = prioridad.get(c2["TIPO_SERVICIO"], 0)
        
        if tipo1 > tipo2:
            return True
        elif tipo1 < tipo2:
            return False
        else:
            if letra1 > letra2:
                return True
            elif letra1 < letra2:
                return False
            else:
                if cod1 > cod2:
                    return True
                else:
                    return False
    except:
        return False

def closest_estacion(catalog,lat,long):
    estaciones = catalog["estaciones_policias"]
    long1 = float(long) * math.pi / 180
    lat1= float(lat) * math.pi / 180
    closest_vertx = None
    min_distance = None
    for vertice in lt.iterator(estaciones):
        lat = vertice["EPOLATITUD"]
        long = vertice["EPOLONGITU"]
        lat = float(lat) * math.pi / 180
        long = float(long) * math.pi / 180
        new_distance = distance( lat1, lat, long1, long )
        if min_distance == None:
            min_distance = new_distance
        if new_distance < min_distance:
            min_distance = new_distance
            closest_vertx = vertice
    return closest_vertx

def add_edge(grafo,v1,v2,weigth):
    edge_entry = gr.getEdge(grafo,v1,v2) 
    if edge_entry == None:
        gr.addEdge(grafo,v1,v2,weigth)
    return grafo

def compare_id(data_1, data_2):
    
    if data_1 > me.getKey(data_2):
        return 1
    elif data_1 < me.getKey(data_2):
        return -1
    else:
        return 0
    
def add_edge_estaciones(catalog, v1,v2, e1,e2, distancia):
    if e1 != None and e2 != None:
        if e1["OBJECTID"] == e2["OBJECTID"]:
            mapg = catalog["grafo_estaciones"]
            minigraph = me.getValue(mp.get(mapg, e1["OBJECTID"]))
            gr.insertVertex(minigraph, v1)
            gr.insertVertex(minigraph, v2)
            add_edge(minigraph, v1, v2, distancia)
            
            
def add_vertx(grafo, id_v):
    contains = gr.containsVertex(grafo, id_v)
    if not contains:
        gr.insertVertex(grafo, id_v)
    return grafo
    