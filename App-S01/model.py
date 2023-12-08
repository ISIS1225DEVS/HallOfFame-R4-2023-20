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
assert cf 

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_vial():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TOD: Inicializar las estructuras de datos
    vial = {"vertices":None,
                              "grafo_comparendos": None,
                              "grafo_distancia": None,
                              "grafo_num_v": None,
                              "comparendos": None,
                              "estaciones": None,
                              "vert_carga": None,
                              "arcos": None,
                              "comparendos_gravedad": None,
                              "tipo_carro": None, 
                              "comparendos_localidad": None}
    
    vial["vertices"] = mp.newMap(maptype="PROBING")
    
    vial["grafo_comparendos"] = gr.newGraph(directed=False)
    
    vial["grafo_distancia"] = gr.newGraph(directed=False)
    
    vial["grafo_num_v"] = gr.newGraph(directed=False)
    
    vial["comparendos"] = lt.newList()
    
    vial["estaciones"] = lt.newList()
    
    vial["vert_carga"] = lt.newList()
    
    vial["arcos"] = lt.newList()
    
    vial["comparendos_gravedad"] = mp.newMap()
    
    vial["tipo_carro"]= mp.newMap()

    vial["comparendos_localidad"]= mp.newMap()
                     
    return vial

# Funciones para agregar informacion al modelo

def add_vertice(vial, vertice, m):
    id = vertice[0]
    vertice_tabla = new_vertice(vertice)
    mp.put(vial["vertices"], id, vertice_tabla)
    gr.insertVertex(vial["grafo_comparendos"], id)
    gr.insertVertex(vial["grafo_distancia"], id)
    gr.insertVertex(vial["grafo_num_v"], id)
    vetice_carga = new_vertice_carga(vertice)
    lt.addLast(vial["vert_carga"], vetice_carga)
    #folium.Marker(location=vertice_tabla["lat_long"], popup=id).add_to(m)
    
    return vial["vert_carga"]

def new_vertice_carga(vertice):
    vertice = {"id": vertice[0],
               "latitud": vertice[2],
               "longitud": vertice[1]}
    return vertice

def add_estacion(vial,estacion, m):
    lat_long = (float(estacion["EPOLATITUD"]), float(estacion["EPOLONGITU"]))
    
    vertice = estacion["VERTICES"]
    vertice_info = mp.get(vial["vertices"], vertice)
    vertice_info = me.getValue(vertice_info)
    lt.addLast(vertice_info["estaciones"], estacion)
    estacion_carga = new_estacion(estacion, vertice)
    lt.addLast(vial["estaciones"], estacion_carga)
    #etiqueta = ("estacion con", lat_long, "cargado en ", vertice)
    folium.Marker(location=vertice_info["lat_long"], popup= str(estacion_carga).strip("{").strip("}"), icon=folium.Icon(color='green', icon='person-military-rifle', prefix='fa')).add_to(m)
    #etiqueta_2 = "estacion con ", lat_long, "ubicación real"
    #folium.Marker(location=lat_long, popup=etiqueta_2, icon=folium.Icon(color="green")).add_to(m)
    
    return vial["estaciones"]
    
def new_estacion(estacion, id_vertice ):
    estacion = {"id": estacion["OBJECTID"],
                "nombre": estacion["EPONOMBRE"],
                "latitud": estacion["EPOLATITUD"],
                "longitud": estacion["EPOLONGITU"],
                "descripcion": estacion["EPODESCRIP"],
                "dirección": estacion["EPODIR_SITIO"],
                "servicio": estacion["EPOSERVICIO"],
                "horario": estacion["EPOHORARIO"],
                "telefono": estacion["EPOTELEFON"],
                "correo": estacion["EPOCELECTR"],
                "id_vertice": id_vertice
                }
    return estacion
    

def add_comparendo(vial, comparendo, m):
    
    lat_long = (float(comparendo["LATITUD"]), float(comparendo["LONGITUD"]))
    vertice = comparendo["VERTICES"]
    vertice_info = mp.get(vial["vertices"], vertice)
    vertice_info = me.getValue(vertice_info)
    lt.addLast(vertice_info["comparendos"], comparendo)
    comparendo_carga = new_comparendo(comparendo, vertice)
    lt.addLast(vial["comparendos"], comparendo_carga)
    #folium.Marker(location=vertice_info["lat_long"], popup= str(comparendo_carga).strip("{").strip("}"), icon=folium.Icon(color='red', icon='car', prefix='fa')).add_to(m)
    comparendo_gravedad = new_comparendo_gravedad(comparendo, vertice, vertice_info["lat_long"])
    comparendo_servicio = mp.get(vial["comparendos_gravedad"], comparendo["TIPO_SERVICIO"])
    if comparendo_servicio:
        comparendo_servicio = me.getValue(comparendo_servicio)
    else:
        comparendo_servicio = mpq.newMinPQ(cmp_gravedad_comparendos)
        mp.put(vial["comparendos_gravedad"], comparendo["TIPO_SERVICIO"], comparendo_servicio)
    mpq.insert(comparendo_servicio, comparendo_gravedad)
    #add_tipo_carro(vial, comparendo)
    #add_comparendo_localidad(vial, comparendo)
    
    return vial["comparendos"]




#def  add_comparendo_localidad(vial, comparendo): 
 #   mapa= vial["comparendos_localidad"]
  #  info_comparendos= mp.get(mapa, comparendo["LOCALIDAD"])
   # if info_comparendos: 
    #    info_comparendos= me.getValue(info_comparendos)
     #   for i in lt.iterator(info_comparendos):
      #      if i["vertice_comparendo"] != comparendo["VERTICES"]:
       #         lt.addLast(info_comparendos, new_comparendo_localidad(comparendo))
    #else: 
     #   info_comparendos= lt.newList("ARRAY_LIST")
      #  lt.addLast(info_comparendos, new_comparendo_localidad(comparendo))
       # mp.put(mapa,comparendo["LOCALIDAD"],info_comparendos)
    #for dic in lt.iterator(info_comparendos):
     #   if dic["vertice_comparendo"]== comparendo["VERTICES"]:
      #      dic["num_comparendos"]= dic["num_comparendos"] + 1
        
    #return vial



def add_comparendo_localidad(vial, comparendo):
    mapa_vial = vial["comparendos_localidad"]
    info_comparendos = mp.get(mapa_vial, comparendo["LOCALIDAD"])
    if info_comparendos:
        lista_comparendos = me.getValue(info_comparendos)
    else:
        lista_comparendos = mp.newMap()
        mp.put(mapa_vial, comparendo["LOCALIDAD"], lista_comparendos)
        
    vertx_comp = mp.get(lista_comparendos, comparendo["VERTICES"])

    if vertx_comp:
        vertx_comp = me.getValue(vertx_comp)
        vertx_comp["numero_comparendos"] += vertx_comp["numero_comparendos"]+1
    else:
        comp_loc_info = mp.newMap()
        comp = new_comparendo_carro(comparendo)
        mp.put(comp_loc_info, comparendo["VERTICES"], comp )
        
    return vial 

#def add_comparendo_localidad(vial, comparendo):
    #mapa= vial["tipo_carro"]
    #info_localidad= mp.get(mapa, comparendo["LOCALIDAD"])
   # if info_localidad: 
       # info_localidad= me.getValue(info_localidad)
    #else: 
      #  info_localidad= mp.newMap()
     #   mp.put(mapa,comparendo["LOCALIDAD"], info_localidad)
    #comp_localidad = mp.get(info_localidad, comparendo["VERTICES"])
    #if comp_localidad:
      #  comp_localidad = me.getValue(comp_localidad)
     #   comp_localidad["numero_comparendos"] += 1
    #else:
      #  comp_localidad = new_comparendo_carro(comparendo)
     #   mp.put(info_localidad, comparendo["VERTICES"], comp_localidad)
    #return vial 

def add_tipo_carro(vial, comparendo): 
    mapa= vial["tipo_carro"]
    info_tipo_carro= mp.get(mapa, comparendo["CLASE_VEHICULO"])
    if info_tipo_carro: 
        info_tipo_carro= me.getValue(info_tipo_carro)
    else: 
        info_tipo_carro= mp.newMap()
        mp.put(mapa,comparendo["CLASE_VEHICULO"], info_tipo_carro)
    comp_carro = mp.get(info_tipo_carro, comparendo["VERTICES"])
    if comp_carro:
        comp_carro = me.getValue(comp_carro)
        comp_carro["numero_comparendos"] += 1
    else:
        comp_carro = new_comparendo_carro(comparendo)
        mp.put(info_tipo_carro, comparendo["VERTICES"], comp_carro)
        
    return vial

def new_comparendo_carro(comparendo): 
    
    dic= {"comparendos": comparendo["VERTICES"],
          "numero_comparendos": 1}
    
    return dic
    
def agregar_comparendos_m(vial, m):
    primeros = lt.subList(vial["comparendos"], 1, 5)
    ultimos = lt.subList(vial["comparendos"], lt.size(vial["comparendos"])-4, 5 )
    for comp in lt.iterator(primeros):
        folium.Marker(location=(comp["latitud"], comp["longitud"]), popup= str(comp).strip("{").strip("}"), icon=folium.Icon(color='red', icon='car', prefix='fa')).add_to(m)
    for comp in lt.iterator(ultimos):
        folium.Marker(location=(comp["latitud"], comp["longitud"]), popup= str(comp).strip("{").strip("}"), icon=folium.Icon(color='red', icon='car', prefix='fa')).add_to(m)

def new_comparendo_gravedad(comparendo, id_vertice, vertice_lat_long):
    
    #Para poder ordenarlos según gravedad en el requerimiento 4.
    """"
    if comparendo["TIPO_SERVICIO"] == "Diplomatico":
        print(comparendo["TIPO_SERVICIO"])
        servicio = 3
    elif comparendo["TIPO_SERVICIO"] == "Oficial":
        servicio = 2
    elif comparendo["TIPO_SERVICIO"] == "Público":
        servicio = 1
    else:
        servicio = 0
    """   
    comparendo = {"id": id_vertice,
                  "lat_long": vertice_lat_long,
                  "infraccion": comparendo["INFRACCION"]}
    return comparendo


def new_comparendo(comparendo, id_vertice):
    comparendo = {"id": comparendo["NUM_COMPARENDO"],
                  "latitud": comparendo["LATITUD"],
                  "longitud": comparendo["LONGITUD"],
                  "fehcha": comparendo["FECHA_HORA"],
                  "medio detencion": comparendo["MEDIO_DETECCION"],
                  "vehiculo": comparendo["CLASE_VEHICULO"],
                  "servicio": comparendo["TIPO_SERVICIO"],
                  "infraccion": comparendo["INFRACCION"],
                  "descripcion": comparendo["DES_INFRACCION"],}
    
    return comparendo

def add_arco(vial, info_arco):
    id_vert = info_arco[0]
    vertice = mp.get(vial["vertices"], id_vert)

    vertice = me.getValue(vertice)
    lat_long = vertice["lat_long"]
    for i in range(1, len(info_arco)):
        id_adj = info_arco[i]
        adj = mp.get(vial["vertices"], id_adj)
        adj = me.getValue(adj)
        lat_long_adj = adj["lat_long"]
        hav = haversine(lat_long, lat_long_adj)
        gr.addEdge(vial["grafo_distancia"], id_vert, id_adj, hav)
        num_comparendos = lt.size(vertice["comparendos"]) + lt.size(adj["comparendos"])
        gr.addEdge(vial["grafo_comparendos"], id_vert, id_adj, num_comparendos)
        arco = gr.getEdge(vial["grafo_distancia"], id_vert, id_adj)
        lt.addLast(vial["arcos"], arco)
        gr.addEdge(vial["grafo_num_v"], id_vert, id_adj, 1)
    
    return vial

def list_arcos_adj(vial):
    primeros = lt.subList(vial["arcos"], 1, 5)
    ultimos = lt.subList(vial["arcos"], lt.size(vial["arcos"])-4, 5)
    t_arcos = gr.numEdges(vial["grafo_distancia"])
    arcos_adj = lt.newList()
    for arco in lt.iterator(primeros):
        arco = new_arco_carga(vial, arco)
        lt.addLast(arcos_adj, arco)
    for arco in lt.iterator(ultimos):
        arco = new_arco_carga(vial, arco)
        lt.addLast(arcos_adj, arco)
    
    return arcos_adj, t_arcos

def new_arco_carga(vial, arco):
    
    arco = {"vertexA": arco["vertexA"],
            "vertexB": arco["vertexB"],
            "adj_vertexA": " "}
    adjs = gr.adjacents(vial["grafo_distancia"], arco["vertexA"])
    
    for adj in lt.iterator(adjs):
        arco["adj_vertexA"] += str(adj) + ", "
        
    arco["adj_vertexA"] = arco["adj_vertexA"][:-2]
    
    return arco

def vertice_cercano(vial, lat_long):
    cercano = ""
    distancia = ""
    for vertice in lt.iterator(mp.valueSet(vial["vertices"])):
        hav = haversine(vertice["lat_long"], lat_long )
        if distancia == "":
            distancia = hav
            cercano = vertice["id"]
        elif hav < distancia:
            distancia = hav
            cercano = vertice["id"]
    return cercano
        


def add_data(vial, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def new_vertice(vert):
    """
    Se usará para la tabla de vertices
    """
    lat_long = (float(vert[2]), float(vert[1]))
    vertice = {"id": vert[0],
               "lat_long": lat_long,
               "estaciones": None,
               "comparendos": None}
    
    vertice["estaciones"] = lt.newList()
    
    vertice["comparendos"] = lt.newList()
    
    return vertice


# Funciones de consulta

def get_data(vial, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(vial):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(vial, lat_i, long_i, lat_f, long_f):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    lat_long_i = (float(lat_i), float(long_i))
    lat_long_f = (float(lat_f), float(long_f))
    
    esta_i = esta_en_bogota(lat_long_i)
    esta_f = esta_en_bogota(lat_long_f)
    
    
    if esta_i and esta_f:
        
        vertice_i = vertice_cercano(vial, lat_long_i)
        vertice_f = vertice_cercano(vial, lat_long_f)
        
        search = dfs.DepthFirstSearch(vial["grafo_distancia"], vertice_i)
        camino = dfs.pathTo(search, vertice_f)
        
        id_vertices = lt.newList()
        
        total_km = 0
        
        vertexa = st.pop(camino)
        lt.addLast(id_vertices, vertexa)
        vertexb = None
        while (not st.isEmpty(camino)):
            vertexb = st.pop(camino)
            arco = gr.getEdge(vial["grafo_distancia"],vertexa, vertexb)
            total_km += arco["weight"]
            lt.addLast(id_vertices, vertexb)
            vertexa = vertexb
            
    else:
        id_vertices = None
        total_km = 0
            
    return id_vertices, total_km


def req_2(vial, lat_i, long_i, lat_f, long_f):
    """
    Función que soluciona el requerimiento 2
    """
    lat_long_i = (float(lat_i), float(long_i))
    lat_long_f = (float(lat_f), float(long_f))
    
    esta_i = esta_en_bogota(lat_long_i)
    esta_f = esta_en_bogota(lat_long_f)
    
    
    if esta_i and esta_f:
        
        vertice_i = vertice_cercano(vial, lat_long_i)
        vertice_f = vertice_cercano(vial, lat_long_f)
        
       # search = djk.Dijkstra(vial["grafo_num_v"], vertice_i)
       # camino = djk.pathTo(search, vertice_f)
        
        search = bf.BellmanFord(vial["grafo_num_v"], vertice_i)
        camino = bf.pathTo(search, vertice_f)
        
        id_vertices = lt.newList()
        
        total_km = 0
        
        arc_1 = st.pop(camino)
        vertexA = arc_1["vertexA"]
        lt.addLast(id_vertices, vertexA)
        vertexB = arc_1["vertexB"]
        lt.addLast(id_vertices, vertexB)
        arc_1_dist = gr.getEdge(vial["grafo_distancia"], vertexA, vertexB)
        total_km += arc_1_dist["weight"]
        vertexA = vertexB
        while (not st.isEmpty(camino)):
            vertexB = st.pop(camino)["vertexB"]
            arco = gr.getEdge(vial["grafo_distancia"],vertexA, vertexB)
            total_km += arco["weight"]
            lt.addLast(id_vertices, vertexB)
            vertexA = vertexB
            
    else:
        
        id_vertices = None
        total_km = 0

    return id_vertices, total_km

def req_3(vial, localidad , m):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3


    comp_localidad= vial["comparendos_localidad"]
    vertices= vial["vertices"]
    grafo_prin= gr.newGraph("ADJ_LIST")
    grafo_distancia = vial["grafo_distancias"]
    
    entry= mp.get(comp_localidad, localidad)
    #print(entry)
    value_dic= me.getValue(entry)

    quk.sort(value_dic, compare_req5)

    pre_lista= lt.subList(value_dic, 0, lt.size(value_dic))
    while lt.size(pre_lista) > m:
        lt.removeLast(pre_lista)

    arcos_inclus= lt.newList('ARRAY_LIST')
    print(pre_lista)
    copia=lt.newList('ARRAY_LIST')
    copia= pre_lista
    km_fibra=0
    id_vertex = lt.newList('ARRAY_LIST')
    for vertx in lt.iterator(pre_lista):
        
        vertexa= vertx["comparendo"]
        lt.addLast(id_vertex, vertexa)
        for f in lt.iterator(copia):
            vertexb= f["comparendo"]

            if vertexa != vertexb :
                print("entró")
                arco= gr.getEdge(grafo_distancia,vertexa, vertexb)
                km_fibra += arco["weight"]
                print(arco)
                if arco == False :
                    arcos_inclus= lt.addLast(arcos_inclus, arco)
        
    n_vertex= m
    
    costo= km_fibra *  1000000
    result= lt.newList('ARRAY_LIST')
    result = lt.addLast(result, crear_resultado(n_vertex , id_vertex, arcos_inclus , km_fibra , costo))
    
    return result

def crear_resultado(n_vertex , id_vertex , arcos_inclus , km_fibra , costo): 

    resultado={"número de vértices": n_vertex,
               "id vértices": id_vertex, 
               "arcos incluidos": arcos_inclus,
               "Kilometros de fibra óptica a usar": km_fibra,
               "Costo Total": costo}
    
    return resultado

def req_4(vial, n):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    
    n_vertices = mp.newMap()
    
    diplomaticos = me.getValue(mp.get(vial["comparendos_gravedad"], "Diplomatico"))


    while lt.size(n_vertices) < n and not mpq.isEmpty(diplomaticos):
        if not mp.get(n_vertices, mpq.min(diplomaticos)["id"]):
            mp.put(n_vertices, mpq.delMin(diplomaticos)["id"], 1)

    
    if lt.size(n_vertices) < n:
        oficial = me.getValue(mp.get(vial["comparendos_gravedad"], "Oficial"))

        while lt.size(n_vertices) < n and not  mpq.isEmpty(oficial):
            if not mp.get(n_vertices, mpq.min(oficial)["id"]):
                mp.put(n_vertices, mpq.delMin(oficial)["id"], 1)
                  
    if lt.size(n_vertices) < n:
        publico = me.getValue(mp.get(vial["comparendos_gravedad"], "Público"))

        while lt.size(n_vertices) < n and not mpq.isEmpty(publico):
            if not mp.get(n_vertices, mpq.min(publico)["id"]):
                mp.put(n_vertices, mpq.delMin(publico)["id"])
    
    if lt.size(n_vertices) < n:
        particular = me.getValue(mp.get(vial["comparendos_gravedad"], "Particular"))

        while lt.size(n_vertices) < n and not mpq.isEmpty(publico):
            if not mp.get(n_vertices, mpq.min(particular)["id"]):
                mp.put(n_vertices, mpq.delMin(particular)["id"])
                
    n_vertices = mp.keySet(n_vertices)
        
    total_vertices, lista_vertices, arcos, total_km, costo = mst_mini_grafo(vial, n_vertices)
    
    return total_vertices, lista_vertices, arcos, total_km, costo


def req_5(vial, clase_carro, m):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento1 5
    #Sacar los comparendos por tipo de carro
    #Sacar los M primeros vertices que tengan mas comparendos
    #Recorrer comparendos para encontrar el menos costoso 
    comp_tipo_carro= vial["tipo_carro"]
    vertices= vial["vertices"]
    #grafo_prin= gr.newGraph("ADJ_#LIST")
    lista_vertices= lt.newList("ARRAY_LIST")
    carros= mp.get(comp_tipo_carro, clase_carro)
    value_map= me.getValue(carros)
    dics= mp.keySet(value_map)
    if lt.size(dics) < int(m):
        pre_lista= dics
    else: 
        pre_lista= lt.subList(dics, 1, int(m))     
    for ids in lt.iterator(pre_lista):
        """tupla= mp.get(vertices, ids["comparendos"])
        vertice= me.getKey(tupla)"""
        lt.addLast(lista_vertices, ids)

    final= mst_mini_grafo(vial, lista_vertices)
    total_vertices= final[0]
    lis_vertices= final[1]
    arcos= final[2]
    total_km= final[3]
    costo= final[4]
    
    return total_vertices, lis_vertices, arcos, total_km, costo


def mst_mini_grafo(vial, lista_vertices):
    """ Carga un subgrafo con la distancia haversine entre los vertices proporcionados en un alista de DISClib.
    los pesos son las distancia haversine. 
    Retorna lo pedido por cada uno de los reuerimientos indivduales
    """
    mini_graf = gr.newGraph(directed=False)
    
    existe_arc = mp.newMap()
    
    for vertice in lt.iterator(lista_vertices):
        gr.insertVertex(mini_graf, vertice)
    
    for vertice in lt.iterator(lista_vertices):
        lat_long = me.getValue(mp.get(vial["vertices"],vertice))["lat_long"]
        for vertice_adj in lt.iterator(lista_vertices):
            if vertice_adj != vertice:
                lat_long_adj = me.getValue(mp.get(vial["vertices"], vertice_adj))["lat_long"]
                dist = haversine(lat_long, lat_long_adj)
                tup_1 = (vertice, vertice_adj)
                tup_2 = (vertice_adj, vertice)
                if not mp.get(existe_arc, tup_2) and not mp.get(existe_arc, tup_2):
                    gr.addEdge(mini_graf, vertice, vertice_adj, dist)
                    mp.put(existe_arc, tup_1, ":)")
                    mp.put(existe_arc, tup_2, ":)")
    
    search = prim.PrimMST(mini_graf, )
    prim.weightMST(mini_graf, search)
    
    #search["mst"] es una pila con los arcos del mst
    new_lista_vertices = lt.newList()
    
    total_vertices = lt.size(lista_vertices)
    arcos = lt.newList()
    total_km = 0
    
    while not st.isEmpty(search["mst"]):
        arc = st.pop(search["mst"])
        if lt.isEmpty(new_lista_vertices):
            lt.addLast(new_lista_vertices, arc["vertexA"])
        lt.addLast(new_lista_vertices, arc["vertexB"])
        arc_sin_peso = new_arc_sin_peso(arc)
        lt.addLast(arcos, arc_sin_peso)
        total_km += arc["weight"]
    
    costo = total_km * 1000000
    
    return total_vertices, new_lista_vertices, arcos, total_km, costo

        
    
def new_arc_sin_peso(arc):
    arc = {"vertexA": arc["vertexA"],
           "vertexB": arc["vertexB"]}
    return arc
                
def req_6(vial, cantidad_comparendos, stacion_police):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    
    vertexs= vial["vertices"]
    
    
    return tot_vertices, vertices_includ, arcos, includ, km_camino

def req_7(vial, lat_i, long_i, lat_f, long_f):
    """
    Como conductor deseo encontrar el
    camino “más corto” en términos número de menor cantidad de
    comparendos entre dos puntos de geográficos localizados en los límites de la ciudad de Bogotá.
    El punto de origen y destino son ingresados por el usuario como latitudes y longitudes (debe validarse que
    dichos puntos se encuentren dentro de los límites encontrados de la ciudad). Estas ubicaciones deben
    aproximarse a los vértices más cercanos en la malla vial.
    """
    # TODO: Realizar el requerimiento 7
    
    lat_long_i = (float(lat_i), float(long_i))
    lat_long_f = (float(lat_f), float(long_f))
    
    esta_i = esta_en_bogota(lat_long_i)
    esta_f = esta_en_bogota(lat_long_f)
    
    
    if esta_i and esta_f:
        
        vertice_i = vertice_cercano(vial, lat_long_i)
        vertice_f = vertice_cercano(vial, lat_long_f)
        
        search = djk.Dijkstra(vial["grafo_comparendos"], vertice_i)
        camino = djk.pathTo(search, vertice_f)
        
        #search = bf.BellmanFord(vial["grafo_comparendos"], vertice_i)
        #camino = bf.pathTo(search, vertice_f)
        

        
        id_vertices = lt.newList()
        arcos = lt.newList()
        total_km = 0
        total_comparendos = 0
         
        arc_1 = st.pop(camino)
        vertexA = arc_1["vertexA"]
        lt.addLast(id_vertices, vertexA)
        vertexB = arc_1["vertexB"]
        lt.addLast(id_vertices, vertexB)
        arc_1_dis = gr.getEdge(vial["grafo_distancia"], vertexA, vertexB)
        arc_1_comp = gr.getEdge(vial["grafo_comparendos"], vertexA, vertexB)
        total_km += arc_1_dis["weight"]
        total_comparendos += arc_1_comp["weight"]
        arc_1 = new_arc_sin_peso(arc_1)
        vertexA = vertexB
        while (not st.isEmpty(camino)):
            vertexB = st.pop(camino)["vertexB"]
            arco_km = gr.getEdge(vial["grafo_distancia"],vertexA, vertexB)
            arco_com = gr.getEdge(vial["grafo_comparendos"],vertexA, vertexB)
            arco = new_arc_sin_peso(arco_com)
            lt.addLast(arcos, arco)
            total_km += arco_km["weight"]
            total_comparendos += arco_com["weight"]
            lt.addLast(id_vertices, vertexB)
            vertexA = vertexB
    else:
        id_vertices = None
        arcos = None
        total_comparendos = 0
        total_km = 0
            
    return id_vertices, arcos, total_comparendos, total_km
        
        
        
    
    pass

def esta_en_bogota(lat_long):
    """
    Determina si un punto con ltitud y lingitud está o no dentro de los limites de Bogotá.
    Responde con un booleano.
    """
    lat, long = lat_long
    if lat > 4.836643219999985 or lat < 3.819966340000008:
        return False
    elif long > -73.99132694999997 or long < -74.39470032000003:
        return False
    else:
        return True
    
    


def ordenar_comparendos_gravedad(comparendos_gravedad):
    
    merg.sort(comparendos_gravedad, cmp_gravedad_comparendos)
    
    return comparendos_gravedad


def req_8(vial):
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

def cmp_gravedad_comparendos(com1, com2):
    """
    if com1["servicio"] == com2["servicio"]:
        if com1["infraccion"] > com2["infraccion"]:
            return True
        else:
            return False
    elif com1["servicio"] > com1["servicio"]:
        return True
    else: 
        return False
    """
    if com1["infraccion"] < com2["infraccion"]:
        return True
    else:
        return False

def cmp_hav(com1, com2):
    if com1["hav"] < com2["hav"]:
        return True
    else:
        return False
    
def compare_req5(dic_1,dic_2):
    if dic_1["numero_comparendos"] < dic_2["numero_comparendos"]:
        return True
    else:
        return False
    

def sort(vial):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
