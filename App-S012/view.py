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
sys.setrecursionlimit(2 ** 29)

def new_controller():
    """
        Se crea una instancia del controlador
    """
    control = controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Identificar una posible ruta entre dos puntos")
    print("3- Identificar la ruta con menos intersecciones entre dos puntos")
    print("4- Determinar la red de comunicaciones con cámaras en los M puntos con el mayor numero de comparendos")
    print("5- Determinar la red de comunicaciones con cámaras en los M puntos con mayor gravedad")
    print("6- Determinar la red de comuncaciones con cámaras en los M puntos con mayor comparendos segun tipo de vehiculo")
    print("7- Obtener los caminos más cortos para que los policías atiendan los M comparendos más graves ")
    print("8- Obtener el camino más corto para que los conductores transiten por la ruta con la menor cantidad de comparendos ")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    comparendos, estaciones, vertices, arcos, maxlong,minlong,maxlat,minlat, comparendos_ordenados =  controller.load_data(control)
    return comparendos, estaciones, vertices, arcos, maxlong,minlong,maxlat,minlat, comparendos_ordenados




#Funcion encarga de tabular listas con mas de 6 elementos
def print_tabulate_6(lista, columnas):
    lista = lista["elements"][:3] + lista["elements"][-3:]
    reduced = []
    for result in lista:
        linea = []
        for c in columnas:
            linea.append(result[c])
        reduced.append(linea)  
    tabla = print(tabulate(reduced, headers=columnas, tablefmt="grid"))
    return tabla

#Funcion encarga de tabular listas con menos de 6 elementos
def print_tabulate(lista, columnas):
    reduced = []
    for result in lista["elements"]:
        linea = []
        for c in columnas:
            linea.append(result[c])
        reduced.append(linea)  
    tabla = print(tabulate(reduced, headers=columnas, tablefmt="grid"))
    return tabla

#Funcion encargada de unicamente generar el tabulate sin imprimirlo
def print_tabulate2(lista, columnas):
    reduced = []
    for result in lista:
        linea = []
        for c in columnas:
            linea.append(result[c])
        reduced.append(linea)  
    tabla = tabulate(reduced, headers=columnas, tablefmt="grid")
    return tabla

def print_tabulate_5(lista, columnas):
    lista = lista["elements"][:5] + lista["elements"][-5:]
    reduced = []
    for result in lista:
        linea = []
        for c in columnas:
            linea.append(result[c])
        reduced.append(linea)  
    tabla = print(tabulate(reduced, headers=columnas, tablefmt="grid"))
    return tabla

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
        #try:
            print_menu()
            inputs = input('Seleccione una opción para continuar\n')
            if int(inputs) == 1:
                print("Cargando información de los archivos ....\n")
                comparendos, estaciones, vertices, arcos, maxlong,minlong,maxlat,minlat, comparendos_ordenados = load_data(control)
                size_c = lt.size(comparendos)
                size_e = lt.size(estaciones)
                size_v = lt.size(vertices)
                size_a = lt.size(arcos)
                print("\n El total de comparendos cargados en la aplicación es: " + str(size_c))
                print_tabulate_5(comparendos, ["OBJECTID", "LATITUD", "LONGITUD", "FECHA_HORA", "MEDIO_DETECCION", "CLASE_VEHICULO", "TIPO_SERVICIO", "INFRACCION", "DES_INFRACCION"])
                print("\n El total de estaciones de policía cargadas en la aplicación es: " + str(size_e))
                print_tabulate_5(estaciones, ["OBJECTID", "EPONOMBRE", "EPOLATITUD", "EPOLONGITU", "EPODESCRIP", "EPODIR_SITIO",  "EPOHORARIO", "EPOTELEFON", "EPOCELECTR"])
                print("\n El total de vértices de la malla vial cargadas en la aplicación es: " + str(size_v))
                print_tabulate_5(vertices, ["ID", "Longitud", "Latitud"])
                print("-----LIMITES----\n")
                print("Longitud minima: " + str(maxlong))
                print("Longitud maxima: " + str(minlong))
                print("Latitud minima: " + str(minlat))
                print("Latitud maxima: "  +str(maxlat) + "\n")
                print("\n El total de arcos de la malla vial cargadas en la aplicación es: " + str(size_a))
                print_tabulate_5(arcos, ["ID", "Vertices Adyacentes"])
                
                
            elif int(inputs) == 2:
                latitud1 = float(input("Ingrese la latitud del punto de origen: "))
                longitud1 = float(input("Ingrese la longitud del punto de origen: "))
                latitud2 = float(input("Ingrese la latitud del punto de destino: "))
                longitud2 = float(input("Ingrese la longitud del punto de destino: "))
                camino_total,distancia_total,total_vertx = controller.req_1(control,vertices, latitud1, longitud1, latitud2, longitud2)
                elements = camino_total['elements']
                print('-->'.join(str(e) for e in elements))
    
                print( "La distancia total es de: " + str(distancia_total))
                print("El total de vertices es de: " + str(total_vertx))
                
                
            elif int(inputs) == 3:
                latitud1 = float(input("Ingrese la latitud del punto de origen: "))
                longitud1 = float(input("Ingrese la longitud del punto de origen: "))
                latitud2 = float(input("Ingrese la latitud del punto de destino: "))
                longitud2 = float(input("Ingrese la longitud del punto de destino: "))
                camino_total,distancia_total,total_vertx = controller.req_2(control,vertices, latitud1, longitud1, latitud2, longitud2)
                elementos = camino_total['elements']
                print( "\nLa distancia total es de: " + str(distancia_total))
                print("El total de vertices es de: " + str(total_vertx))
                print('-->'.join(str(e) for e in elementos))

            elif int(inputs) == 4:
                X= controller.req_3(control,vertices,20,"CHAPINERO")
                elementos= X["elements"]
                print('-->'.join(str(e) for e in elementos))
                
            elif int(inputs) == 5:
                camaras = int(input("Ingrese el numero de camaras: "))
                bono = input("Desea caragar el bono(si/no): ")
                vertices, arcos, weight = controller.req_4(control, comparendos_ordenados, camaras, bono)
                weight = weight *  0.001
                print("El total de vertices es de: " + str(vertices))
                print("El total de arcos es de: " + str(arcos))
                print("La cantidad de kilometros en fibra optica es de: " + str(weight))
                print("El costo toal es de : " + str(1000000/weight) + " pesos")
                
            elif int(inputs) == 6:
                pass
                
                
            elif int(inputs) == 7:
                numero_comparendos = int(input("Ingrese el numero de comparendos: "))
                bono = input("Desea caragar el bono(si/no): ")
                camino_total = controller.req_6(control, numero_comparendos, comparendos_ordenados, bono)
                print(camino_total)
                
            elif int(inputs) == 8:
                lat1 = float(input("Ingrese la latitud del punto de origen: "))
                long1 = float(input("Ingrese la longitud del punto de origen: "))
                lat2 = float(input("Ingrese la latitud del punto de destino: "))
                long2 = float(input("Ingrese la longitud del punto de destino: "))
                bono = input("Desea caragar el bono(si/no): ")
                distancia_total, vertices_totales, camino_total, total_multas = controller.req_7(control, vertices,  lat1, long1, lat2, long2,bono)
                print(camino_total)
                print("El total de vertices es de: " + str(vertices_totales))
                print("El total de comparendos es de: " + str(total_multas))
                print("La distancia en kilometros es de: " + str(distancia_total))
                
            elif int(inputs) == 9:
                pass

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        #except:
            #print("Error")
    sys.exit(0)
