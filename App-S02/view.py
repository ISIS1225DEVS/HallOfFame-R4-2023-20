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
    control = controller.new_controller()
    return control

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Identificar una posible ruta entre dos puntos definidos")
    print("3- Identificar la ruta con menos intersecciones entre dos puntos definidos")
    print("4- Buscar red de comunicaciones para instalacion de camaras en los M puntos con mas comparendos en una localidad")
    print("5-  Determinar la red de comunicaciones que soporte instalar cámaras en los M puntos con los comparendos de mayor gravedad")
    print("6- : Determinar la red de comunicaciones que soporte instalar cámaras de video en los M puntos con el mayor número de comparendos segun tipo de vehículo")
    print("7-  Obtener los caminos más cortos para que los policías atiendan los M comparendos más graves")
    print("8-  Obtener el camino más corto para que un conductores transiten por la ruta con la menor cantidad de comparendos")
    print("9- Graficar todos los requerimientos")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    controller.load_data(control,0)


def print_data(control, n_vertices, n_arcos, n_comparendos, n_estaciones, tiempo):
    """
        Función que imprime un dato dado su ID
    """
    print("El tiempo de ejecucion es de: " + str(tiempo))
    print("Total de comparendos cargados: " + str(n_comparendos))
    print(tabulate(lt.iterator(control["model"]["primeros_c"])))
    
    print("Total de estaciones cargados: " + str(n_estaciones))
    print(tabulate(lt.iterator(control["model"]["primeros_e"])))
    
    print("Total de vertices cargados: " + str(n_vertices))
    print(tabulate(lt.iterator(control["model"]["primeros_v"])))

def print_req_1(control, latO, longO, latD, longD):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    
    camino, totalD, totalV = controller.req_1(control, latO, longO, latD, longD)
    
    print("la distancia total del camino es: " + str(totalD))
    print("El total de vertices en el camino es: " + str(totalV))
    print("la secuencia de vertices del camino se mueseta a continuacion: ")
    print("")
    print(camino)    
    print("")
    print("")
    
    pass


def print_req_2(control, latO, longO, latD, longD):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    
    camino, totalD, totalV = controller.req_2(control, latO, longO, latD, longD)
    
    print("la distancia total del camino es: " + str(totalD))
    print("El total de vertices en el camino es: " + str(totalV))
    print("la secuencia de vertices del camino se mueseta a continuacion: ")
    print("")
    print(camino)    
    print("")
    print("")
    
    pass



def print_req_3(control, vertices_red, arcos_red, distance, costo, total_v):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    print("============ Req No. 3 Results ============")

    print("Total de vertices en la red: "+ str(total_v))
    print("Vertices incluidos en la red: ")
    for i in lt.iterator(vertices_red):
        print(tabulate(lt.iterator(i)))
    print("La cantidad de kilómetros de fibra óptica extendida: " + str(distance))
    print("El costo total: " + str(costo))
    print(tabulate(arcos_red))


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control, total_v, vertices_red, arcos_red, distance, tiempo):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    print("El tiempo fue de: " + str(tiempo))
    print("============ Req No. 3 Results ============")

    print("Total de vertices en la red: "+ str(total_v))
    print("Vertices incluidos en la red: ")
    for i in lt.iterator(vertices_red):
        print(tabulate(lt.iterator(i)))
    print("La cantidad de kilómetros de fibra óptica extendida: " + str(distance))
    print("El costo total: " + str(costo))
    print(tabulate(arcos_red))


def print_req_7(control, lato, longo, latd, longd):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    camino = controller.req_7(control, lato, longo, latd, longd)
    stringfinal = ""
    for vertice in camino:
        stringfinal += vertice + " --> "
    print(stringfinal)
    pass


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
            n_vertices, n_arcos, n_comparendos, n_estaciones, tiempo = load_data(control)
            print_data(control, n_vertices, n_arcos, n_comparendos, n_estaciones, tiempo)
        elif int(inputs) == 2:
            latO = float(input('Latitud origen: '))
            longO = float(input('Longitud origen: '))
            latD = float(input('Latitud destino: '))
            longD = float(input('Longitud destino: '))
            
            
            
            print_req_2(control, latO, longO, latD, longD)

        elif int(inputs) == 3:
            

            latO = float(input('Latitud origen: '))
            longO = float(input('Longitud origen: '))
            latD = float(input('Latitud destino: '))
            longD = float(input('Longitud destino: '))
            
            
            
            print_req_1(control, latO, longO, latD, longD)
            
        elif int(inputs) == 4:
            n = input("Ingrese la cantidad de camaras que se desea instalar: ")
            localidad = input("Ingrese la localidad: ")
            vertices_red, arcos_red, distance, costo, total_v, tiempo = controller.req_3(control, float(n), localidad)
            print("El tiempo de ejecución es: "+ str(tiempo))
            print("============ Req No. 3 Inputs ============")
            print("Localidad: " + localidad)
            print("Numero de camaras a instalar: " + n)
            print_req_3(control, vertices_red, arcos_red, distance, costo, total_v)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            n = input("Ingrese la cantidad de camaras que se desea instalar: ")
            total_v, grupos_v, arcos_red, distance, tiempo = controller.req_6(control, n)
            print_req_6(control, total_v, grupos_v, arcos_red, distance, tiempo)

        elif int(inputs) == 8:
            lato = float(input('Latitud origen: '))
            longo = float(input('Longitud origen: '))
            latd = float(input('Latitud destino: '))
            longd = float(input('Longitud destino: '))
            print_req_7(control, lato, longo, latd, longd)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
