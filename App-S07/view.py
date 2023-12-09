"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate as tb
import traceback
import threading

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    data = controller.load_data(control)
    return data

def print_data(totalInfractions, InfractionsList, totalPoliceStations, policeStationsList, totalVertices, verticesList, limits, totalEdges, edgesList):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    print("Total infractions: " + str(totalInfractions))
    print(tb(InfractionsList["elements"], headers="keys",tablefmt="grid"))
    print("\nTotal police satations: " + str(totalPoliceStations))
    print(tb(policeStationsList["elements"], headers="keys",tablefmt="grid"))
    print("\nTotal vertices: " + str(totalVertices))
    print(tb(verticesList["elements"], headers="keys",tablefmt="grid"))
    print("\nCity limits: ")
    print(tb([limits], headers="keys",tablefmt="grid"))
    print("\nTotal edges: " + str(totalEdges))
    print(tb(edgesList["elements"], headers="keys",tablefmt="grid"))

def print_req_1(camino):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    lista = []
    for c in lt.iterator(camino):
        lista.append(c)
    print(lista)

def print_req_2(path):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pathRoute = []
    for vertex in lt.iterator(path):
        pathRoute.append(vertex)
    print(pathRoute)

def print_req_3(routesRed):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    verticesList = mp.keySet(routesRed)
    for vertice in lt.iterator(verticesList):
        verticeEntry = mp.get(routesRed, vertice)
        routeVertice = me.getValue(verticeEntry)
        print("\nCameraID: " + str(vertice))
        print("\nTotal vertices route: " + str(lt.size(routeVertice)))
        print(routeVertice["elements"])

def print_req_4(ruta):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    rutas = []
    vertices = mp.keySet(ruta)
    for v in lt.iterator(vertices):
        entry = mp.get(ruta, v)
        rutav = me.getValue(entry)
        diccionario = {"Camara": v, "ruta": rutav["elements"]}
        rutas.append(diccionario)
    print(tb(rutas, headers="keys",tablefmt="grid"))


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass

def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

def print_req_7(path):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pathRoute = []
    for vertex in lt.iterator(path):
        pathRoute.append(vertex["vertexB"])
    print(pathRoute)

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
def thread_cycle():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')

        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
            totalInfractions, InfractionsList, totalPoliceStations, policeStationsList, totalVertices, verticesList, limits, totalEdges, edgesList = controller.get_load_info(data)
            print_data(totalInfractions, InfractionsList, totalPoliceStations, policeStationsList, totalVertices, verticesList, limits, totalEdges, edgesList)

        elif int(inputs) == 2:
            print("Ingrese la informacion del punto de origen")
            latitud1 =  float(input("Ingrese la latitud: ") )
            longitud1= float(input("Ingrese la longitud: ")) 
            print("Ingrese la informacion del punto de destino")
            latitud2 = float(input("Ingrese la latitud: ")) 
            longitud2 = float(input("Ingrese la longitud: ")) 
            distancia, vertices, camino = controller.req_1(data, longitud1, latitud1, longitud2, latitud2)
            print("La distancia total es de: " + str(distancia))
            print("El total de vertices es de: " + str(vertices))
            print("El camino sugerido que se debe tomar es: ")
            print_req_1(camino)

        elif int(inputs) == 3:
            print("\nIngrese la informacion del punto de origen")
            originLatiude = float(input("Ingrese la latitud: ")) 
            originLongitude = float(input("Ingrese la longitud: "))
            print("\nIngrese la informacion del punto de destino")
            destinationLatitude = float(input("Ingrese la latitud: ")) 
            destinationLongitude = float(input("Ingrese la longitud: "))
            path, verticesPath, totalDistance, routeVertices = controller.req_2(data, originLatiude, originLongitude, destinationLatitude, destinationLongitude)
            print("\nID punto de origen: " + str(routeVertices[0]))
            print("\nID punto de destino: " + str(routeVertices[1]))
            print("\nDistancia total que toma el camino: " + str(totalDistance) + " km")
            print("\nTotal de vertices que contiene el camino: " + str(verticesPath))
            print("\nSecuencia de vertices que componen el camino: ")
            print_req_2(path)

        elif int(inputs) == 4:
            cameras = int(input("Ingrese el numero de camaras que desea instalar: ")) 
            locality = input("Ingrese la localidad: ")
            camerasVertices, originVertex, routesRed, DistanceRed, totalCost = controller.req_3(data, cameras, locality)
            print("\Vertices con camaras que componen la red: ")
            print(camerasVertices["elements"])
            print("\nID origen red: " + str(originVertex))
            print("\nSecuencia de vertices que componen la red: ")
            print_req_3(routesRed)
            print("\nDistancia total de la fibra optica: " + str(DistanceRed))
            print("\nCosto monetario de la fibra optica: " + str(totalCost) + " COP")

        elif int(inputs) == 5:
            m1 = int(input("Numero de puntos: "))
            time, total, vertices, ruta, km, costo = controller.req_4(data, m1)
            print("El tiempo total para encontar la solución: " +str(time))
            print("El total de vertices es de : " +str(total))
            print("La cantidad de KM es: " +str(km))
            print("El costo total es de: " + str(costo))
            print("Los vertices son: ")
            print(vertices["elements"])
            print("La secuencia de vertice es: ")
            print_req_4(ruta)

        elif int(inputs) == 6:
            m = int(input("Numero de puntos: "))
            t = input("Tipo vehiculo: ")
            m, vertices_red, kms, costo_total, tiempo = controller.req_5(control, m, t)
            print("Total de vertices en la red: " + str(m) )
            print("Vertices")
            rta  = ""
            for v in lt.iterator(vertices_red):
                rta += v + ", "
            rta.strip(", ")
            tiempo = str(tiempo)
            print("Tiempo [ms]: " + tiempo[1::])
            print(rta)
            print("\nKilometros totales: " + str(kms))
            print("Costo total de la red: " + str(costo_total))

        elif int(inputs) == 7:
            estacion = input("ID de la estación de policia: ")
            n = int(input("Cantidad de comparendos: "))
            rta, tiempo = controller.req_6(control, estacion, n)
            i = 1
            tiempo = str(tiempo)
            print("Tiempo [ms]: " + tiempo[1::])
            for r in lt.iterator(rta):
                print("\ncamino "+ str(i))
                print("total vertices: " + str(r["vertices totales"]))
                print("vertices: "+ r["vertices"])
                print("kilometros: "+ str(r["kilometros"]))
                i += 1

        elif int(inputs) == 8:
            print("\nIngrese la informacion del punto de origen")
            originLatiude = float(input("Ingrese la latitud: ")) 
            originLongitude = float(input("Ingrese la longitud: "))
            print("\nIngrese la informacion del punto de destino")
            destinationLatitude = float(input("Ingrese la latitud: ")) 
            destinationLongitude = float(input("Ingrese la longitud: "))
            path, verticesPath, totalInfractions, totalDistance = controller.req_7(data, originLatiude, originLongitude, destinationLatitude, destinationLongitude)
            print(("\nDistancia total que toma el camino: " + str(totalDistance) + " km"))
            print(("\nInfraciones totales que tiene el camino: " + str(totalInfractions) + " infractions"))
            print("\nTotal de vertices que contiene el camino: " + str(verticesPath))
            print("\nSecuencia de vertices que componen el camino: ")
            print_req_7(path)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()