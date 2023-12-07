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
from DISClib.Utils import error as error
assert cf
import sys
import math
from math import radians, cos, sin, asin, sqrt

default_limit = 1000
sys.setrecursionlimit(default_limit*10000)

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
        "vertexInfo" : None,
        "arcos" : None, 
        "search":None
    }
    data_structs["comparendos"] = mp.newMap(numelements=200000, 
                                         maptype='CHAINING', loadfactor=4,
                                         cmpfunction=None)

    data_structs["stations"] = mp.newMap(numelements=20, 
                                         maptype='CHAINING', loadfactor=4,
                                         cmpfunction=None)

    data_structs['vertexInfo'] = mp.newMap(numelements=14000, 
                                         maptype='PROBING',cmpfunction=None)

    data_structs['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=230000,
                                        cmpfunction=None)
    data_structs['connections_comparendos'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=230000,
                                        cmpfunction=None)
    
    data_structs["Req_4_comparendos"]=om.newMap(omaptype="RBT", cmpfunction=Compare_req4)
    data_structs['vertex_reqs'] =  lt.newList()
    data_structs['edges_reqs'] =  lt.newList()

    return data_structs


# Funciones para agregar informacion al modelo

def add_Req_vertex(data_structs, vertex):
    vertex = {"id": vertex['id'], "lon": vertex['lon'],
                  "lat": vertex["lat"], "comparendos": vertex["comparendos"], "estacion": vertex['estacion']}
    lt.addLast(data_structs['vertex_reqs'], vertex)

def edge_req(data_structs, edge):
    edge = {"id": edge['id']}
    lt.addLast(data_structs['edges_reqs'], edge)


def addBogotaVertex(data_structs, vertex):
    vertexId = formatVertex(vertex)
    addVertex(data_structs, vertexId)
    addVertexInfo(data_structs, vertex)

def addVertexInfo(data_structs, vertex): 
    vertexInfo = data_structs['vertexInfo']
    key = vertex["id"]
    info = newVertex(vertex["id"])
    info["lon"] = vertex["lon"]
    info["lat"] = vertex["lat"]
    if vertex["comparendos"]!= "None":
        comparendos = vertex["comparendos"].split(';')
        if len(comparendos) > 1:
            for comparendo in comparendos:
                entry = mp.get(data_structs["comparendos"], comparendo)
                values = me.getValue(entry)
                lt.addLast(info["Comparendos"], values)
        else:
            entry = mp.get(data_structs["comparendos"], comparendos[0])
            values = me.getValue(entry)
            lt.addLast(info["Comparendos"], values)
    if vertex["estacion"] != "None":
        estaciones = vertex["estacion"].split(';')
        if len(estaciones) > 1:
            for estacion in estaciones:
                entry = mp.get(data_structs["stations"], estacion)
                values = me.getValue(entry)
                lt.addLast(info["Estacion de policia"], values)
        else:
            entry = mp.get(data_structs["stations"], estaciones[0])
            values = me.getValue(entry)
            lt.addLast(info["Estacion de policia"], values)
    mp.put(vertexInfo, key, info)

def newVertex(id):
    
    vertex = {'id': "",
              "Estacion de policia": None,
              "Comparendos": None,
              "lon": None,
              "lat": None}
    vertex['id'] = id
    vertex['Estacion de policia'] = lt.newList('ARRAY_LIST')
    vertex['Comparendos'] = lt.newList('ARRAY_LIST')
    return vertex 

def addVertexStations(data_structs, station):
    cords = station['geometry']['coordinates']
    key = station['properties']['OBJECTID']
    station_i = {"ID": station['properties']['OBJECTID'], "Name": station['properties']['EPONOMBRE'],
                  "Lat": cords[0], "Lon": cords[1], "Address": station['properties']['EPODIR_SITIO'],
                    "Service": station['properties']['EPOSERVICIO'], "schedule": station['properties']['EPOHORARIO'], 
                    "Number": station['properties']['EPOTELEFON'], "Email": station['properties']['EPOCELECTR']}
    station = data_structs['stations']
    mp.put(station, str(key), station_i)

def searchVertex(data_structs, lon, lat): 
    vertex = data_structs['vertex'] #lista con todos los vertices
    key = min(vertex, key=lambda v: haversine(lon, lat, v[0], v[1]))#devuelve la la llave en este caso la lon y lat del vertice mas cercano
    return key

def addComparendos(data_structs, comparendo):
    cords = comparendo['properties']
    comparendos = data_structs['comparendos']
    key = str(cords['GlobalID'])
    comparendo = {"ID": cords['GlobalID'], "Lat": cords['LATITUD'],
                  "Lon": cords["LONGITUD"], "Fecha": cords["FECHA_HORA"], "Medio deteccion": cords['MEDIO_DETECCION'],
                    "Clase vehiculo": cords['CLASE_VEHICULO'], "Tipo de servicio": cords['TIPO_SERVICIO'], 
                    "Infraccion": cords['INFRACCION'], "Desc infra..": cords['DES_INFRACCION']}
    mp.put(comparendos, key, comparendo)

def addBogotaArc(data_structs, arc):
    relations = arc["id"].split()
    origin = relations[0]
    relations.pop(0)
    vertexInfo = data_structs['vertexInfo']
    entry_origin = mp.get(vertexInfo, origin)
    values_origin = me.getValue(entry_origin)
    origin_lon = values_origin["lon"]
    origin_lat = values_origin["lat"]
    if len(relations) > 0:
        for destination in relations:
            comparendos = lt.size(values_origin['Comparendos'])
            edge = gr.getEdge(data_structs['connections'], origin, destination)
            if edge is None:
                entry = mp.get(vertexInfo, destination)
                values = me.getValue(entry)
                dest_lon = values["lon"]
                dest_lat = values["lat"]
                comparendos += lt.size(values['Comparendos'])
                distance = haversine(float(origin_lon), float(origin_lat), float(dest_lon), float(dest_lat))
                weight_distance = distance
                weight_comparendos = comparendos
                gr.addEdge(data_structs['connections'], origin, destination, weight_distance)
                gr.addEdge(data_structs['connections_comparendos'], origin, destination, weight_comparendos)

def addVertex(catalog, vertex):
        try:
            if not gr.containsVertex(catalog['connections'], vertex):
                gr.insertVertex(catalog['connections'], vertex)
                gr.insertVertex(catalog['connections_comparendos'], vertex)              
            return catalog
        except Exception as exp:
            error.reraise(exp, 'model:addstop')

def formatVertex(vertex):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = vertex["id"]
    return name

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass

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
# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    
    numV = gr.numVertices(data_structs['connections'])
    vertex = mp.valueSet(data_structs["vertexInfo"])
    min_lon = 999999999
    min_lat = 999999999
    max_lon = -999999999
    max_lat = -999999999
    for element in lt.iterator(vertex):
        if float(element["lon"]) < min_lon:
            min_lon = float(element["lon"])
        if float(element["lat"]) < min_lat:
            min_lat = float(element["lat"])
        if float(element["lon"]) > max_lon:
            max_lon = float(element["lon"])
        if float(element["lat"]) > max_lat:
            max_lat = float(element["lat"])
    Nume = gr.numEdges(data_structs['connections'])
    edges = data_structs['edges_reqs']
    Vertex = get_load_data(vertex, "vertex", data_structs)
    edges = get_load_data(edges, "ADT_List", data_structs)
    stations = mp.valueSet(data_structs['stations'])
    comparendos = mp.valueSet(data_structs['comparendos'])
    comparendos = get_load_data(comparendos, "comparendo", None)
    stations = get_load_data(stations, "station", None)  
    num_St = mp.size(data_structs["stations"])
    com_St = mp.size(data_structs["comparendos"])
    return stations, numV, Vertex, min_lon, max_lon, min_lat, max_lat, Nume, comparendos, num_St, com_St, edges

def get_load_data(item, type, data_structs):
    data = lt.newList()
    if type == "vertex":
        for i in range(1, 5+1):
            element = lt.getElement(item, i)
            p = {'id': element["id"],"longitude": element["lon"], "latitude": element["lat"]}
            lt.addLast(data, p)
        for i in range((lt.size(item)-5) + 1, lt.size(item) + 1):
            element = lt.getElement(item, i)
            p = {'id': element["id"],"longitude": element["lon"], "latitude": element["lat"]}
            lt.addLast(data, p)
    if type == "ADT_List":
        for i in range(1, 5+1):
            element = lt.getElement(item, i)
            relations = element["id"].split()
            if len(relations) > 1:
                edge = {'origin': relations[0], "destinations": relations[1:]}
            else:
                edge = {'origin': relations[0], "destinations": "None"}
            lt.addLast(data, edge)
        for i in range((lt.size(item)-5) + 1, lt.size(item) + 1):
            element = lt.getElement(item, i)
            relations = element["id"].split()
            if len(relations) > 1:
                edge = {'origin': relations[0], "destinations": relations[1:]}
            else:
                edge = {'origin': relations[0], "destinations": "None"}
            lt.addLast(data, edge)
    if type == "station":
        for i in range(1, 6):
            res = lt.getElement(item, i)
            lt.addLast(data, res)
        for j in range((lt.size(item)-5) + 1, lt.size(item) + 1):
            res = lt.getElement(item, j)
            lt.addLast(data, res)
    if type == "comparendo":
        for i in range(1, 6):
            res = lt.getElement(item, i)
            lt.addLast(data, res)
        for j in range((lt.size(item)-5) + 1, lt.size(item) + 1):
            res = lt.getElement(item, j)
            lt.addLast(data, res)
    return data
def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs, initial_point, final_point):
    
    """
    Función que soluciona el requerimiento 1
    """

    min_lon= -74.39470032000003
    max_lon= -73.99132694999997
    min_lat= 3.819966340000008
    max_lat= 4.836643219999985

    initial_point=initial_point.split(",")

    lat_initial=initial_point[0]
    lon_initial=initial_point[1].strip()

    final_point=final_point.split(",")

    lat_destiny=final_point[0]
    lon_destiny=final_point[1].strip()

    #Verifico si los vértices se encuentran dentro de los límites encontrados de la ciudad

    if (float(min_lon)<=float(lon_initial)<=float(max_lon)) and (float(min_lat)<=float(lat_initial)<=float(max_lat)) and (float(min_lon)<=float(lon_destiny)<=float(max_lon)) and (float(min_lat)<=float(lat_destiny)<=float(max_lat)):

        try: 
            #Hallamos los vértices respectivos
            llaves=mp.keySet(data_structs["vertexInfo"])

            vertice_initial = None
            vertice_destiny = None
            distancia_minima = float('inf')
            distancia_minima_2 = float('inf')

            for llave in lt.iterator(llaves):
                
                pareja_llave_valor=mp.get(data_structs["vertexInfo"], llave)
                lat_= me.getValue(pareja_llave_valor)["lat"]
                lon_= me.getValue(pareja_llave_valor)["lon"]
                

                #distancia_initial=haversine(float(lon_), float(lat_), float(lon_initial), float(lat_initial))
                distancia_initial = math.sqrt((float(lat_) - float(lat_initial))**2 + (float(lon_) - float((lon_initial)))**2)

                # Actualizar el vértice más cercano si la distancia actual es menor que la mínima registrada

                if distancia_initial < distancia_minima:
                    distancia_minima = distancia_initial
                    vertice_initial = llave


            for llave in lt.iterator(llaves):
                
                pareja_llave_valor=mp.get(data_structs["vertexInfo"], llave)
                lat_= me.getValue(pareja_llave_valor)["lat"]
                lon_= me.getValue(pareja_llave_valor)["lon"]

                
                #distancia_destiny=haversine(float(lon_), float(lat_), float(lon_destiny), float(lat_destiny))
                distancia_destiny= ((float(lat_) - float(lat_destiny))**2 + (float(lon_) - float((lon_destiny)))**2)**0.5

                if distancia_destiny < distancia_minima_2:
                    distancia_minima_2 = distancia_destiny
                    vertice_destiny = llave
            
            data_structs['search'] = bfs.BreathFirstSearch(data_structs['connections'], vertice_initial) 
            existe_camino = bfs.hasPathTo(data_structs['search'], vertice_destiny)
            path = bfs.pathTo(data_structs['search'], vertice_destiny)
            distancia_total=0

            numero_vertices_recorridos=0
            camino=lt.newList("ARRAY_LIST")

            if existe_camino==True or existe_camino=="True":
            
                for i in lt.iterator(path):


                    distancia=gr.getEdge(data_structs['connections'], vertice_initial, i)
                    numero_vertices_recorridos+=1

                    if distancia!=None:

                        
                        distancia_arco=float(distancia["weight"])
                        distancia_total+=distancia_arco
                        lt.addLast(camino, i)

                    vertice_initial=i

    

            return distancia_total, numero_vertices_recorridos, camino
        
        except:
            return 0, 0, "Los vértices suministrados (o alguno de ellos) no se encuentran dentro de los límites de la ciudad."        

def req_2(data_structs, initial_point, final_point):
    #initial_point = "4.60293518548777, -74.06511801444837"
    #final_point =  "4.693518613347496, -74.13489678235523"

    """Preparacion para encontrar vertices en el grafo"""
    initial_point=initial_point.split(",")
    lat_initial=initial_point[0]
    lon_initial=initial_point[1].strip()
    final_point=final_point.split(",")
    lat_destiny=final_point[0]
    lon_destiny=final_point[1].strip()

    #Hallamos el vértice de origen más cercano
    llaves=mp.keySet(data_structs["vertexInfo"])

    vertice_i = None
    vertice_f = None
    distancia_minima = float('inf')
    distancia_minima_2 = float('inf')

    for llave in lt.iterator(llaves):
          
        pareja_llave_valor=mp.get(data_structs["vertexInfo"], llave)
        lat_= me.getValue(pareja_llave_valor)["lat"]
        lon_= me.getValue(pareja_llave_valor)["lon"]
        
        distancia_initial = math.sqrt((float(lat_) - float(lat_initial))**2 + (float(lon_) - float((lon_initial)))**2)
        distancia_destiny = math.sqrt((float(lat_) - float(lat_destiny))**2 + (float(lon_) - float((lon_destiny)))**2)

        # Actualizar el vértice más cercano si la distancia actual es menor que la mínima registrada
        if distancia_initial < distancia_minima:
            distancia_minima = distancia_initial
            vertice_i = llave
        
        if distancia_destiny < distancia_minima_2:
            distancia_minima_2 = distancia_destiny
            vertice_f = llave

    data_structs['search'] = bfs.BreathFirstSearch(data_structs['connections'], vertice_i)
    camino = bfs.pathTo(data_structs['search'], vertice_f)
    lista = lt.newList('SINGLE_LINKED')
    retorno = recur(camino['first'], lista)

    anterior = None
    distancia = 0
    for vertice in lt.iterator(retorno):
        if anterior == None:
            pass
        else:
            h = gr.getEdge(data_structs['connections'], anterior, vertice[0])
            distancia += float(h['weight'])
        anterior = vertice[0]
        

    return retorno, distancia

def recur(camino, lista):
    if camino['next'] == None:
        return lista
    else:
        lt.addLast(lista, [camino['info']])
        recur(camino['next'], lista)
    return lista


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs, M):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    M=int(M)
    llaves=mp.keySet(data_structs["comparendos"])
    lista_comparendos=lt.newList("ARRAY_LIST")

    for llave in lt.iterator(llaves):

        pareja_llave_valor=mp.get(data_structs["comparendos"], llave)
        vertice=me.getValue(pareja_llave_valor)

        if vertice["Tipo de servicio"] == "Diplomatico":
            vertice["Tipo de servicio"]=4
        elif vertice["Tipo de servicio"] =="Oficial":
            vertice["Tipo de servicio"]=3
        elif vertice["Tipo de servicio"]== "Público":
            vertice["Tipo de servicio"]=2
        elif vertice["Tipo de servicio"]== "Particular":
            vertice["Tipo de servicio"]=1
        else:
            vertice["Tipo de servicio"]=0

        llave = str(vertice["Tipo de servicio"]) + "," + vertice["Infraccion"] + "," + vertice["ID"] 
        
        mp.put(data_structs["Req_4_comparendos"], llave, vertice)
    
    llaves=mp.keySet(data_structs["Req_4_comparendos"])

    i=1
    for llave in lt.iterator(llaves):
        if i<=M:
            lt.addLast(lista_comparendos, llave)
        i+=1

    vertice_initial=None
    vertices_mayor_gravedad=lt.newList("ARRAY_LIST")

    llaves=mp.keySet(data_structs["vertexInfo"])
    for comparendos in lt.iterator(lista_comparendos):
            
            pareja_llave_valor_=mp.get(data_structs["Req_4_comparendos"], comparendos)
            lat_initial=me.getValue(pareja_llave_valor_)["Lat"]
            lon_initial=me.getValue(pareja_llave_valor_)["Lon"]
            distancia_minima = float('inf')

            
            try:
                for llave in lt.iterator(llaves):
                    
                    pareja_llave_valor=mp.get(data_structs["vertexInfo"], llave)

                    lat_= me.getValue(pareja_llave_valor)["lat"]
                    lon_= me.getValue(pareja_llave_valor)["lon"]
                    
                    #distancia_initial= haversine(lon_, lat_, lon_initial, lat_initial)
                    distancia_initial = math.sqrt((float(lat_) - float(lat_initial))**2 + (float(lon_) - float((lon_initial)))**2)
                
                    if distancia_initial < distancia_minima:
                        distancia_minima = distancia_initial
                        vertice_initial = llave
            
            
                lt.addLast(vertices_mayor_gravedad, vertice_initial)

            except:
                pass
    
    print("Los vértices de mayor gravedad son: ")  
    print(vertices_mayor_gravedad)


    inicial=lt.firstElement(vertices_mayor_gravedad) 
    lt.removeFirst(vertices_mayor_gravedad)
    pos=0
    lista_camino=lt.newList("ARRAY_LIST")
    segundo=lt.firstElement(vertices_mayor_gravedad) 
    lt.removeFirst(vertices_mayor_gravedad)

    data_structs['search'] = djk.Dijkstra(data_structs['connections'], inicial) 
    existe_camino = djk.hasPathTo(data_structs['search'], segundo)
    path = djk.pathTo(data_structs['search'], segundo)

    for i in lt.iterator(path):
        lt.addLast(lista_camino, i["vertexB"])

    inicial=lt.firstElement(vertices_mayor_gravedad) 
    lt.removeFirst(vertices_mayor_gravedad)
       
    if existe_camino==True or existe_camino=="True":
     try:

        for i in lt.iterator(vertices_mayor_gravedad):
            pos+=1 
            
            for j in lt.iterator(path):
                lt.addLast(lista_camino, j["vertexB"]) 

            if lt.isPresent(lista_camino, i)==0:
                    lt.deleteElement(vertices_mayor_gravedad, pos)

            data_structs['search'] = djk.Dijkstra(data_structs['connections'], inicial) 
            existe_camino = djk.hasPathTo(data_structs['search'], i)
            path = djk.pathTo(data_structs['search'], i)

        inicial=i

     except:
        pass

    total_vertices=0
    distancia_total=0

    for i in lt.iterator(lista_camino):

        total_vertices+=1
             
        distancia=gr.getEdge(data_structs['connections'], vertice_initial, i)
       
        total_vertices+=1 

        if distancia!=None:
        
                distancia_arco=float(distancia["weight"])
                distancia_total+=distancia_arco
               

        vertice_initial=i
    

    vertice_initial=lt.getElement(lista_camino, 1)
    vertice_final=lt.getElement(lista_camino, -1)

    costo_total= distancia_total*(1000000)

    return total_vertices, lista_camino, vertice_initial, vertice_final, distancia_total, costo_total



def req_5(data_structs, M, V):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    llaves_C = mp.keySet(data_structs['comparendos'])
    req_vertex = data_structs['vertex_reqs']
    m = int(M)
    map_req = mp.newMap(numelements=50000, 
                        maptype='CHAINING', loadfactor=4,
                        cmpfunction=None)
    map_vertex_req = mp.newMap(numelements=50000, 
                        maptype='CHAINING', loadfactor=4,
                        cmpfunction=None)
    gr_req_5 = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=m,
                                        cmpfunction=None)
    for llave in lt.iterator(llaves_C):
        entry = mp.get(data_structs['comparendos'],llave)
        value = me.getValue(entry)
        if value['Clase vehiculo'] == V:
            Values = {"ID": value['ID'], "lat": value['Lat'],
                  "lon": value["Lon"], "Clase vehiculo": value['Clase vehiculo']}
            mp.put(map_req, llave,Values)
    for vertex in lt.iterator(req_vertex):
        if vertex["comparendos"]!= "None":
            comparendos = vertex["comparendos"].split(';')
            if len(comparendos) > 1:
                for comparendo in comparendos:
                    if mp.contains(map_req, comparendo):
                        addBogotaVertexReq5(map_vertex_req, vertex, comparendo, gr_req_5)             
            else:
                if mp.contains(map_req, comparendos[0]):
                        addBogotaVertexReq5(map_vertex_req, vertex, comparendos[0], gr_req_5)
    vertex_req = mp.valueSet(map_vertex_req)
    merg.sort(vertex_req, compare_req_5)
    origin = lt.getElement(vertex_req, 1)
    id_origin = origin["id"]
    gr.insertVertex(gr_req_5, id_origin)
    distance = 0
    vertices_incluidos = 0
    while int(gr.numVertices(gr_req_5)) < m:
        listaV = gr.vertices(gr_req_5)
        for vertex in lt.iterator(vertex_req):
            if (lt.isPresent(listaV, vertex["id"]) == False) or (lt.isPresent(listaV, vertex["id"]) == "False"):
                id_vertex = vertex["id"]
                if (id_vertex != id_origin):
                    exist = bfs.BreathFirstSearch(data_structs['connections'], id_origin)
                    existe_camino = bfs.hasPathTo(exist, id_vertex)
                    if (existe_camino == True) or (existe_camino == "True"):
                        camino = bfs.pathTo(exist, id_vertex)
                        vertices_incluidos += lt.size(camino)
                        gr.insertVertex(gr_req_5, id_vertex)
                        weight = haversine(float(origin['lon']), float(origin['lat']), float(vertex['lon']), float(vertex['lat']))
                        distance += weight
                        gr.addEdge(gr_req_5, id_origin, id_vertex, weight)
                        id_origin = id_vertex
                        break   
    costo = distance * 1000000
    vertices_identicadores = gr.numVertices(gr_req_5)
    arcos = gr.edges(gr_req_5)
    total_vertices = vertices_incluidos
    v = gr.vertices(gr_req_5)

    return distance, costo, total_vertices,vertices_identicadores, arcos, v

                    


def compare_req_5(data_1, data_2):
    if lt.size(data_1["comparendos"]) > lt.size(data_2["comparendos"]):
        return True
    else:
        return False


def addBogotaArcReq5(data_structs, origin, map_vertex_req):
    values_vertex = mp.keySet(map_vertex_req)
    graf_vertex = data_structs["connections"] 
    for vertex in values_vertex:
        if vertex != origin:
            exist = bfs.BreathFirstSearch(graf_vertex, origin)
            existe_camino = bfs.hasPathTo(exist, vertex)
            print(existe_camino)
        """entry_origin = mp.get(vertexInfo, origin)
        values_origin = me.getValue(entry_origin)
        origin_lon = values_origin["lon"]
        origin_lat = values_origin["lat"]
        if len(relations) > 0:
            for destination in relations:
                comparendos = lt.size(values_origin['comparendos'])
                edge = gr.getEdge(gr_req_5, origin, destination)
                if edge is None:
                    entry = mp.get(VertexDes, destination)
                    values = me.getValue(entry)
                    dest_lon = values["lon"]
                    dest_lat = values["lat"]
                    if mp.contains(vertexInfo, destination):
                        entry = mp.get(vertexInfo, destination)
                        values = me.getValue(entry)
                        comparendos += lt.size(values['comparendos'])
                    distance = haversine(float(origin_lon), float(origin_lat), float(dest_lon), float(dest_lat))
                    weight_distance = distance
                    weight_comparendos = comparendos
                    gr.addEdge(gr_req_5, origin, destination, weight_distance)
                    gr.addEdge(data_structs['connections_comparendos'], origin, destination, weight_comparendos)"""

    
def addBogotaVertexReq5(map_vertex_req, vertex, comparendo, gr_req_5):
    vertexId = formatVertex(vertex)
    addVertexInfoReq5(map_vertex_req, vertex, comparendo)

def addVertexInfoReq5(map_vertex_req, vertex, comparendo): 
    vertexInfo = map_vertex_req
    key = vertex["id"]
    if mp.contains(vertexInfo, key):
        entry = mp.get(map_vertex_req, key)
        value = me.getValue(entry)
        lt.addLast(value["comparendos"], comparendo)
    else:
        value = {"id": vertex['id'], "lat": vertex['lat'], "lon": vertex['lon'], "comparendos": lt.newList()}
        lt.addLast(value["comparendos"], comparendo)
        mp.put(map_vertex_req,key,value)

def addVertex_req_5(gr_req, vertex):
        try:
            if not gr.containsVertex(gr_req, vertex):
                gr.insertVertex(gr_req, vertex)
                gr.insertVertex(gr_req, vertex)              
            return gr_req
        except Exception as exp:
            error.reraise(exp, 'model:addstop')


def req_6(data_structs, M):
    """
    Función que soluciona el requerimiento 6
    """
    # Organizacion de los comparendos de mas grave a menos grave
    lista = mp.valueSet(data_structs['comparendos'])
    #lista = quk.sort(lista, sort_crit_req_6)
    lista = lt.subList(lista, 1, M)

    # Validacion de estacion mas cercana por comparendo
    estaciones = mp.valueSet(data_structs['stations'])
    llaves = mp.keySet(data_structs["vertexInfo"])
    vertices_estaciones = lt.newList('SINGLE_LINKED')

    for estacion in lt.iterator(estaciones): 
        lat = float(estacion['Lat'])
        lon = float(estacion['Lon'])
        vertice_i = None
        distancia_minima = float('inf')

        for llave in lt.iterator(llaves):
            
            pareja_llave_valor=mp.get(data_structs["vertexInfo"], llave)
            lat_= float(me.getValue(pareja_llave_valor)["lat"])
            lon_= float(me.getValue(pareja_llave_valor)["lon"])
            
            distancia_initial = abs(abs(abs(lat_) - abs(lat)) - abs(abs(lon_) - abs(lon)))
            # Actualizar el vértice más cercano si la distancia actual es menor que la mínima registrada
            if distancia_initial < distancia_minima:
                distancia_minima = distancia_initial
                vertice_i = llave
        lt.addLast(vertices_estaciones, {estacion['Name']: vertice_i})
    #vertices_estaciones es mi lista de estaciones con su respectivo codigo de vertice

    #hallar la calle del comparendo para saber en que vertice se encuentra
    vertices_comparendos = lt.newList('SINGLE_LINKED')
    for comparendo in lt.iterator(lista):
        distancia = 100000000
        lat = float(comparendo['Lat'])
        lon = float(comparendo['Lon'])
        for llave in lt.iterator(llaves):
            pareja_llave_valor=mp.get(data_structs["vertexInfo"], llave)
            lat_= float(me.getValue(pareja_llave_valor)["lat"])
            lon_= float(me.getValue(pareja_llave_valor)["lon"])

            distancia_initial = abs(abs(abs(lat_) - abs(lat)) - abs(abs(lon_) - abs(lon)))

            if distancia_initial < distancia:
                distancia = distancia_initial
                vertice = llave
        lt.addLast(vertices_comparendos, vertice)
    #vertices_comparendos me dice en que vertice ocurre cada comparendo

    #algoritmo correcto tomando en cuenta 'distancias' de los arcos con dijkstra
    """
    retorno_prime = lt.newList('SINGLE_LINKED')
    for comparendo in lt.iterator(vertices_comparendos):
        closest = 10000000
        recorrido = djk.Dijkstra(data_structs['connections'], str(comparendo))
        for estacion in lt.iterator(vertices_estaciones):
            for nombre in estacion:
                codigo = estacion[nombre]
                validacion = djk.hasPathTo(recorrido, codigo)
                camino = djk.pathTo(recorrido, codigo)
                if validacion == True:
                    retorno = lt.newList('SINGLE_LINKED')
                    retorno = recur(camino['first'], retorno)
                if lt.size(retorno) < closest:
                    cercana = retorno
                    closest = lt.size(retorno)
                    retorno['nombre'] = nombre
        lt.addLast(retorno_prime, cercana)
    """

    #algoritmo provisional usando bfs para una menor demora
    retorno_prime = lt.newList('SINGLE_LINKED')
    for comparendo in lt.iterator(vertices_comparendos):
        closest = 10000000
        recorrido = bfs.BreathFirstSearch(data_structs['connections'], str(comparendo))
        for estacion in lt.iterator(vertices_estaciones):
            for nombre in estacion:
                codigo = estacion[nombre]
                validacion = bfs.hasPathTo(recorrido, codigo)
                camino = bfs.pathTo(recorrido, codigo)
                if validacion == True:
                    retorno = lt.newList('SINGLE_LINKED')
                    retorno = recur(camino['first'], retorno)
                if lt.size(retorno) < closest:
                    cercana = retorno
                    closest = lt.size(retorno)
                    retorno['nombre'] = nombre
        lt.addLast(retorno_prime, cercana)

    return retorno_prime

        

def sort_crit_req_6(data1, data2):
    if data1['Tipo de servicio'] == 'Publico' and data2['Tipo de servicio'] != 'Publico':
        return 1
    elif data2['Tipo de servicio'] == 'Publico' and data1['Tipo de servicio'] != 'Publico':
        return 0
    elif data1['Tipo de servicio'] != 'Publico' and data2['Tipo de servicio'] != 'Publico':
        if data1['Tipo de servicio'] == 'Oficial' and data2['Tipo de servicio'] != 'Oficial':
            return 1
        elif data2['Tipo de servicio'] == 'Oficial' and data1['Tipo de servicio'] != 'Oficial':
            return 0 
        elif data1['Tipo de servicio'] != 'Particular' and data2['Tipo de servicio'] != 'Particular':
            if data1['Infraccion'] > data2['Infraccion']:
                return 1
            elif data1['Infraccion'] < data2['Infraccion']:
                return 0
            else:
                return -1
            

def req_7(data_structs, initial_point, final_point):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7

    initial_point=initial_point.split(",")

    lat_initial=initial_point[0]
    lon_initial=initial_point[1].strip()

    final_point=final_point.split(",")

    lat_destiny=final_point[0]
    lon_destiny=final_point[1].strip()

    #Hallamos el vértice de origen más cercano
    llaves=mp.keySet(data_structs["vertexInfo"])

    vertice_initial = None
    vertice_destiny = None
    distancia_minima = float('inf')
    distancia_minima_2 = float('inf')

    min_lon= -74.39470032000003
    max_lon= -73.99132694999997
    min_lat= 3.819966340000008
    max_lat= 4.836643219999985

    if (float(min_lon)<=float(lon_initial)<=float(max_lon)) and (float(min_lat)<=float(lat_initial)<=float(max_lat)) and (float(min_lon)<=float(lon_destiny)<=float(max_lon)) and (float(min_lat)<=float(lat_destiny)<=float(max_lat)):

     try: 

        for llave in lt.iterator(llaves):
            
            pareja_llave_valor=mp.get(data_structs["vertexInfo"], llave)
            lat_= me.getValue(pareja_llave_valor)["lat"]
            lon_= me.getValue(pareja_llave_valor)["lon"]
            

            
            #distancia_initial=haversine(float(lon_), float(lat_), float(lon_initial), float(lat_initial))
            distancia_initial = math.sqrt((float(lat_) - float(lat_initial))**2 + (float(lon_) - float((lon_initial)))**2)


            # Actualizar el vértice más cercano si la distancia actual es menor que la mínima registrada
            if distancia_initial < distancia_minima:
                distancia_minima = distancia_initial
                vertice_initial = llave


        for llave in lt.iterator(llaves):
            
            pareja_llave_valor=mp.get(data_structs["vertexInfo"], llave)
            lat_= me.getValue(pareja_llave_valor)["lat"]
            lon_= me.getValue(pareja_llave_valor)["lon"]

            
            #distancia_destiny=haversine(float(lon_), float(lat_), float(lon_destiny), float(lat_destiny))
            distancia_destiny= ((float(lat_) - float(lat_destiny))**2 + (float(lon_) - float((lon_destiny)))**2)**0.5

            if distancia_destiny < distancia_minima_2:
                distancia_minima_2 = distancia_destiny
                vertice_destiny = llave

        data_structs['search'] = djk.Dijkstra(data_structs['connections_comparendos'], vertice_initial) 
        existe_camino = djk.hasPathTo(data_structs['search'], vertice_destiny) #Ya sé que existe camnino
        path = djk.pathTo(data_structs['search'], vertice_destiny)


        distancia_total=0
        comparendos_totales=0

        total_vertices=0
        lista_vertices=lt.newList("ARRAY_LIST")
        if existe_camino==True or existe_camino=="True":
        
            for i in lt.iterator(path):
                
                distancia=gr.getEdge(data_structs['connections'], vertice_initial, i["vertexB"])
                comparendo=gr.getEdge(data_structs['connections_comparendos'], vertice_initial, i["vertexB"])
                total_vertices+=1
                lt.addLast(lista_vertices, i["vertexB"]) 

                if distancia!=None:
                
                    distancia_arco=float(distancia["weight"])
                    comparendo_arco=float(comparendo["weight"])
                    distancia_total+=distancia_arco
                    comparendos_totales+=comparendo_arco

                vertice_initial=i["vertexB"]

    
        return total_vertices, lista_vertices, vertice_initial, vertice_destiny, comparendos_totales, distancia_total
     
     except:
         return 0, 0, 0, 0, 0, 0




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

def Compare_req4(data_1, data_2):
    if data_1==data_2:
        return 0
    elif data_1<data_2:
        return 1
    else:
        return -1