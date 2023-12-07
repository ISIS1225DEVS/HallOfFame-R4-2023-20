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
from tabulate import tabulate
import traceback

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


def load_data(control, vertexname, arcosname, policeStation, comparendos):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    catalog = controller.load_data(control, vertexname, arcosname, policeStation, comparendos)
    return catalog


def print_data(control):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    stations, numV, Vertex, min_lon, max_lon, min_lat, max_lat, Nume, comparendos, num_St, com_St, edges, d = controller.get_data(control)
    print("load in: " + str(d) + " ms")
    print("Total comparendos: " + str(com_St), "\n")
    print("The first and last five comparendos:")
    print(tabulate(lt.iterator(comparendos), headers='keys', tablefmt="grid"), "\n")
    print("Total stations: " + str(num_St), "\n")
    print("The first and last five stations:")
    print(tabulate(lt.iterator(stations), headers='keys', tablefmt="grid"), "\n")
    print("Total vertex: " + str(numV))
    print("Min lon: " + str(min_lon))
    print("Max lon: " + str(max_lon))
    print("Min lat: " + str(min_lat))
    print("Max lat: " + str(max_lat), "\n")
    print(tabulate(lt.iterator(Vertex), headers='keys', tablefmt="grid"), "\n")
    print("Total edges: " + str(Nume))
    print(tabulate(lt.iterator(edges), headers='keys', tablefmt="grid"), "\n")

    pass

def print_req_1(control, initial_point, final_point):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    distancia_total, numero_vertices_recorridos, camino, delt, deltM = controller.req_1(control, initial_point, final_point)
    return distancia_total, numero_vertices_recorridos, camino, delt, deltM


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    initial_point = input('Ingrese latitud y longitud del punto inicial (xxx, yyy): ')
    final_point = input('Ingrese latitud y longitud del punto final (xxx, yyy): ')
    retorno, distancia = controller.req_2(control, initial_point, final_point)
    print("\n===== Req 2 Results =====")
    print("\n-La distancia total a recorrer entre las ubicaciones es de: {0}".format(distancia))
    print("\n-Se recorrieron {0} vertices/intersecciones".format(lt.size(retorno)))
    print("\n-Esta es la secuencia de vertices recorridos por sus respectivos codigos:")
    print(tabulate(lt.iterator(retorno)))


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control, M):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    total_vertices, lista_camino, vertice_initial, vertice_final, distancia_total, costo_total, delt, deltM = controller.req_4(control, M) 
    return total_vertices, lista_camino, vertice_initial, vertice_final, distancia_total, costo_total, delt, deltM


def print_req_5(control, M, V):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    distance, costo, total_vertices,vertices_identicadores, arcos, v,d = controller.req_5(control, M, V)
    print("load in: " + str(d) + " ms")
    print("Total distance: " + str(distance))
    print("Total cost: " + str(costo))
    print("Total vertex: " + str(total_vertices))
    print("Vertices identifcadores: " + str(vertices_identicadores), "\n")
    print(v)
    print("Total edges: " + str(lt.size(arcos)), "\n")
    print(tabulate(lt.iterator(arcos), headers='keys', tablefmt="grid"), "\n")

def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    M = input('Ingrese la cantidad de comparendos mas importantes a analizar: ')
    retorno = controller.req_6(control, M) 
    num = 0
    for camino in lt.iterator(retorno):
        num += 1
        print('\nEl camino al {0} comparendo mas importante es el siguiente:'.format(num))
        print(tabulate(lt.iterator(camino)))
        print('La estacion mas cercana es "{0}"'.format(camino['nombre']))
        print('El camino pasa por {0} vertices'.format(lt.size(camino)))

def print_req_7(control, initial_point, final_point):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    total_vertices, lista_vertices, vertice_initial, vertice_destiny, comparendos_totales, distancia_total, delt, deltM=controller.req_7(control, initial_point, final_point)
    return total_vertices, lista_vertices, vertice_initial, vertice_destiny, comparendos_totales, distancia_total, delt, deltM


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
            vertexname = 'data.txt'
            arcosname = 'bogota_arcos.txt'
            policeStation = "estacionpolicia.json"
            comparendos = "Comparendos_2019_Bogota_D_C.geojson"
            data = load_data(control, vertexname, arcosname, policeStation, comparendos)
            print_data(control)

        elif int(inputs) == 2:
            initial_point = input("Ingrese la latitud y longitud del punto de inicio respectivamente: ")
            final_point = input("Ingrese la latitud y longitud del punto final respectivamente: ")
            distancia_total, numero_vertices_recorridos, camino, delt, deltM=print_req_1(control, initial_point, final_point)
            print("\n")
            print("La distancia total para el camino encontrado entre los vértices es: "+str(distancia_total))
            print("El número de vertices encontrados para el camino es: "+str(numero_vertices_recorridos))
            print("\n")
            print("El camino encontrado (vértices) es el siguiente: ")
            print(camino)
            print("\n")     
            print("El timepo que ha tomado este requerimiento es de: "+str(delt))
            print("El espacio en memoria que ha tomado este requerimiento es de: "+str(deltM))
            print("\n")


        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            M = input("Ingrese el número (M) de cámaras para ser instaladas: ")
            total_vertices, lista_camino, vertice_initial, vertice_final, distancia_total, costo_total, delt, deltM=print_req_4(control, M)
            print("\n")     
            print("El timepo que ha tomado este requerimiento es de: "+str(delt))
            print("El espacio en memoria que ha tomado este requerimiento es de: "+str(deltM))
            print("\n") 
            print("El número de vertices encontrados para el camino es: "+str(total_vertices))
            print("\n")
            print("El camino encontrado (vértices) es el siguiente: ")
            print(lista_camino)
            print("\n") 
            print("El vértices inicial es: "+str(vertice_initial))
            print("El vértices final es: "+str(vertice_final))
            print("La distancia total es: "+str(distancia_total))
            print("La distancia total es: "+str(costo_total))

        elif int(inputs) == 6:
            M = input("No: ")
            V = input("tipo de vehiculo: ")
            print_req_5(control, M, V)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            initial_point = input("Ingrese la latitud y longitud del punto de inicio respectivamente: ")
            final_point = input("Ingrese la latitud y longitud del punto final respectivamente: ")

            total_vertices, lista_vertices, vertice_initial, vertice_destiny, comparendos_totales, distancia_total, delt, deltM=print_req_7(control, initial_point, final_point)
            print("\n")
            print("El número de vertices encontrados para el camino es: "+str(total_vertices))
            print("\n")
            print("El camino encontrado (vértices) es el siguiente: ")
            print(lista_vertices)
            print("\n") 
            print("El vértices inicial es: "+str(vertice_initial))
            print("El vértices final es: "+str(vertice_destiny))
            print("El número de comparendos totales es: "+str(comparendos_totales))
            print("La distancia total es: "+str(distancia_total))
            print("\n")   
            print("El timepo que ha tomado este requerimiento es de: "+str(delt))
            print("El espacio en memoria que ha tomado este requerimiento es de: "+str(deltM))
            print("\n") 

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)

