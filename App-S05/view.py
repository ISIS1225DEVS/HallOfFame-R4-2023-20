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
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
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
    return controller.new_controller()



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

extremos = {"lat_max":None,
            "lat_min":None,
            "long_max":None,
            "long_min":None
            }
def load_data(control):
    """
    Carga los datos
    """
    respuesta = controller.load_data(control)
    comparendos_5_primeros = lt.subList(control['model']['Comparendos'], 1, 5)
    comparendos_5_ultimos = lt.subList(control['model']['Comparendos'], lt.size(control['model']['Comparendos'])-5, 5)
    estaciones_5_primeros = lt.subList(control['model']['Estaciones de policia'], 1, 5)
    estaciones_5_ultimos = lt.subList(control['model']['Estaciones de policia'], lt.size(control['model']['Estaciones de policia'])-5, 5)
    print('El total de comparendos cargados son: ' + str(lt.size(control['model']['Comparendos'])))
    print('Los primeros cinco comparendos son:')
    for comparendo in lt.iterator(comparendos_5_primeros):
        print(comparendo)
    print('Los ultimas cinco comparendos son:')
    for comparendo in lt.iterator(comparendos_5_ultimos):
        print(comparendo)
    print('El total de estaciones cargados son: ' + str(lt.size(control['model']['Estaciones de policia'])))
    print('Los primeros cinco estacioens cargadas son:')
    for estacion in lt.iterator(estaciones_5_primeros):
        print(estacion)
    print('Los ultimas cinco estaciones cargadas son:')
    for estacion in lt.iterator(estaciones_5_ultimos):
        print(estacion)
    print('El total vertices de la malla vial son : ' + str(gr.numVertices(control['model']['Grafo_distancias'])))
    for vertices in range(1, 6):
        dict =  me.getValue(mp.get(control['model']['Malla_Vial'], str(vertices)))
        print(str(vertices) + ' ' + str(dict['lat']) + ' ' + str(dict['long']))
    for vertices in range(lt.size(control['model']['vertices'])-6, lt.size(control['model']['vertices'])):
        dict =  me.getValue(mp.get(control['model']['Malla_Vial'], str(vertices)))
        print(str(vertices) + ' ' + str(dict['lat']) + ' ' + str(dict['long']))
    print('El total arcos de la malla vial son : ' + str(gr.numEdges(control['model']['Grafo_distancias'])))
    print('los limites de la malla vial son')
    print('lat_max = '+ str(respuesta[0]))
    print('lat_min = '+ str(respuesta[1]))
    print('long_max = '+ str(respuesta[2]))
    print('long_min = '+ str(respuesta[3]))
    extremos["lat_max"]=float(respuesta[0])
    extremos["lat_min"]=float(respuesta[1])
    extremos["long_max"]=float(respuesta[2])
    extremos["long_min"]=float(respuesta[3])

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    lat_inicio = float(input('Ingrese la latitud de inicio: '))
    long_inicio = float(input('Ingrese la longitud de inicio: '))
    lat_destino = float(input('Ingrese la latitud de destino: '))
    long_destino = float(input('Ingrese la longitud de destino: '))
    if lat_inicio<=extremos["lat_max"] and lat_destino<=extremos["lat_max"] and lat_inicio>=extremos["lat_min"] and lat_destino>=extremos["lat_min"] and long_inicio<=extremos["long_max"] and long_destino<=extremos["long_max"] and long_inicio>=extremos["long_min"] and long_destino>=extremos["long_min"]:
   
        respuesta, totalVertices, peso, vertice1, vertice2 = controller.req_1(control, lat_inicio, long_inicio, lat_destino, long_destino)
        print('El total de vertices que contienen el camino es: ' + str(totalVertices))
        print('La distancia total del camino es: ' + str(peso) + ' [km]')
        print('El vertice inicial es: ' + str(vertice1))
        print('El vertice final es: ' + str(vertice2))
        print('Los vertices que contienen el camino son: \n')
        for i in lt.iterator(respuesta):
            print(i)


def print_req_2(control,extremos):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    lat_inicio = float(input('Ingrese la latitud de inicio: '))
    long_inicio = float(input('Ingrese la longitud de inicio: '))
    lat_destino = float(input('Ingrese la latitud de destino: '))
    long_destino = float(input('Ingrese la longitud de destino: '))
    if lat_inicio<=extremos["lat_max"] and lat_destino<=extremos["lat_max"] and lat_inicio>=extremos["lat_min"] and lat_destino>=extremos["lat_min"] and long_inicio<=extremos["long_max"] and long_destino<=extremos["long_max"] and long_inicio>=extremos["long_min"] and long_destino>=extremos["long_min"]:
        peso,numero_pasos,pasos = controller.req_2(control, lat_inicio, long_inicio, lat_destino, long_destino) 
        print("\nLa distancia total que tomará el camino entre el punto de encuentro de origen y el de destino: "+str(peso))
        print("\nEl total de vértices que contiene el camino encontrado es de: "+str(numero_pasos))
        print("\nLa secuencia de vértices es de: " + str(pasos))
    else:
        print("Los valores ingresados estan fuera de los limites de la ciudad.")


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    M = input('Ingrese la cantidad de camaras de video que se desean instalar: ')
    localidad = input('Ingrese la localidad donde se desean instalar: ')

    controller.req_3(control, M, localidad)  

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    M = input("Ingrese la cantidad de camaras de video que desea instalar: ")
    vertices,arcos,kilometros,costo = controller.req_4(control,M)
    print("\nEl total de vertices en el camino fue de: "+str(vertices))
    print("\nLos arcos en el camino fueron: ")
    print(arcos)
    print("\nEl total de kilometros en el red fue de: "+str(kilometros)+"km")
    print("\nEl total de costo por la red fue de: "+str(costo)+"COP")


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    m = input('Ingrese el numero de comparendos: ')
    clase = input('Ingrese la clase de vehiculo: ')
    listaVerticesRed, listaArcosRed, distancia_total, formato, SubListaVertices = controller.req_5(control, m, clase)
    print( 'los vertices que contaran con camaras som: \n')
    for i in lt.iterator(SubListaVertices):
        print(i['vertice'])
    print('\nla longitud total de fibra optica es:' + str(distancia_total) + ' [km]')
    print('la cantidad de dinero para la implementacion de la red es:' + formato + ' [COP]')
    print('Los verticen conectados por la red son: \n \n')
    print(listaVerticesRed) 
    print('\n \n \n los arcos conectados por la red son: \n \n')
    print(listaArcosRed)


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    m = input('Ingrese el numero de comparendos: ')
    lista = controller.req_6(control, m)
    
    for camino in lt.iterator(lista):
        comparendo = camino['comparendo']
        print('\n\nID comparendo: ' + str(comparendo['OBJECTID']))
        print('\nEl camino mas corto es:')
        print(camino['listaVerticesCamino'])
        print('\nLa distancia total del camino es: ' + str(camino['distancia']) + ' [km] \n')

def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    lat_inicio = float(input('Ingrese la latitud de inicio: '))
    long_inicio = float(input('Ingrese la longitud de inicio: '))
    lat_destino = float(input('Ingrese la latitud de destino: '))
    long_destino = float(input('Ingrese la longitud de destino: '))
    if lat_inicio<=extremos["lat_max"] and lat_destino<=extremos["lat_max"] and lat_inicio>=extremos["lat_min"] and lat_destino>=extremos["lat_min"] and long_inicio<=extremos["long_max"] and long_destino<=extremos["long_max"] and long_inicio>=extremos["long_min"] and long_destino>=extremos["long_min"]:
        total_vertices,vertices,arcos,cantidad_comparendos,cantidad_kilometros = controller.req_7(control, lat_inicio, long_inicio, lat_destino, long_destino)
        print("\nEl total de vertices fue de: "+str(total_vertices))
        print("\nLos vertices son: ")
        print(vertices)
        print("\nLos arcos incluidos son: ")
        print(arcos)
        print("\nLa cantidad de comparendos del camino fue de: "+str(cantidad_comparendos))
        print("\nLa cantidad de kilometros del camino fue de: "+str(cantidad_kilometros)+"km")
    else:
        print("Los valores ingresados estan fuera de los limites de la ciudad.")
        
        
        
def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
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
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control, extremos)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
