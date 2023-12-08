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
    control = controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Identificar una posible ruta entre dos puntos definidos")
    print("3- Identificar la ruta con menos intersecciones entre puntos diferentes")
    print("4- Determinar la red de comunicciones que soporte instalar cámars en los M puntos con el mayor numero de comparendos en una localidad")
    print("5- Determinar la red de comunicaciones que soporte instalar cámaras en los M puntos con los comparendos de mayor gravedad")
    print("6- Determinar la red de comunicaciones que soporte instalar cámaras en los M puntos con el mayor numero de comparendos segun tipo de vehículo")
    print("7- Obtener los caminos más cortos para que los policías atiendan los M comparendos más graves")
    print("8- Obtener el caminko más corto para que un conductor transite por la ruta con la menor cantidad de comparendos")
    print("9- Graficar los resultados para cada uno de los requerimientos")
    print("0- Salir")


def load_data(control):
    """
    Carga los dato
    """
    #TODO: Realizar la carga de datos
    vertices, min_long, min_lat, max_long, max_lat, estaciones, comparendos, arcos, t_arcos, d_time = controller.load_data(control)
    return vertices, min_long, min_lat, max_long, max_lat, estaciones, comparendos, arcos, t_arcos, d_time


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(vertices, dist, d_time):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    print("================= POSIBLE RUTA ENTRE DOS PUNTOS ================")
    print()
    print("Distancia total entre los puntos: ", dist)
    print("Total de vertices del camino: ", lt.size(vertices))
    print()
    print("***** secuencia de vertices del camino *****")
    print("Los 5 primeros y ultimos vertices son")
    
    for i in range(1, 6):
        print(lt.getElement(vertices, i))
        
    print( "* * *")
        
    for i in range(lt.size(vertices)-4, lt.size(vertices)+1):
        print(lt.getElement(vertices, i))
        
    print("Tiepo de eección [ms] ", d_time)
    


def print_req_2(vertices, dist, d_time):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    print("================= RUTA CON MENOR NUMERO DE INTERSECCIONES ==============")
    print()
    print("Distancia total entre los puntos: ", dist)
    print("Total de vertices del camino: ", lt.size(vertices))
    print()
    print("***** secuencia de vertices del camino *****")
    print("Los 5 primeros y ultimos vertices son")
    print()
    for i in range(1, 6):
        print(lt.getElement(vertices, i))
        
    print( "* * *")
        
    for i in range(lt.size(vertices)-4, lt.size(vertices)+1):
        print(lt.getElement(vertices, i))
    
    print()
    print("Tiepo de ejección [ms] ", d_time)


def print_req_3(result, d_time):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    print("================= RED DE COMUNICACIONES PARA INSTALAR CÁMARAS ==============")
    print("Tiepo de eección [ms] ", d_time)
    print(result)
    print()
    


def print_req_4(total_vertices, vertices, arcos, total_km, costo, d_time):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    print("======================== RED DE CAMARAS M COMPARENDOS MAS GRAVES ======================")
    print()
    print("Total de vertices de la red: ", total_vertices)
    print()
    print("***** secuencia de vertices de la red *****")
    print()
    print("Los 5 primeros y ultimos vertices son")
    print()
    for i in range(1, 6):
        print(lt.getElement(vertices, i))
        
    print( "* * *")
        
    for i in range(lt.size(vertices)-4, lt.size(vertices)+1):
        print(lt.getElement(vertices, i))
        
    print()
    print("Total de arcos de la red: ", lt.size(arcos))
    print()
    print_tabla(arcos)
    print()
    print("Total de kilometros de fibra optica extendida: ", total_km, " km")
    print("Costo monetario total: ", costo, " COP")
    print()
    print("Tiepo total de ejecución [ms]: ", d_time)
    


def print_req_5(control, d_time, total_vertices, lis_vertices, arcos, total_km, costo):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    print("========================RED DE COMUNICACIONES SEGUN TIPO DE VEHICULO===========================")
    print()
    print("Total vertices:" + str(total_vertices))
    print("Vertices identificadores: ")
    print(lis_vertices)
    print("Arcos: " )
    print(arcos)
    print("Total de kilometros: " + str(total_km))
    print("Costo total de la red: " + str(costo))
    print()
    print("tiempo de ejecución: " + str(d_time))
    print()


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(vertices, arcos, comparendos, km, d_time):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    print("================= RUTA CON MENOR NUMERO DE COMPARENDOS ( y más corta posible) ==============")
    print()
    print("Total de vertices del camino: ", lt.size(vertices))
    print()
    print("***** secuencia de vertices del camino *****")
    print()
    print("Los 5 primeros y ultimos vertices son:")
    for i in range(1, 6):
        print(lt.getElement(vertices, i))
        
    print( "* * *")
        
    for i in range(lt.size(vertices)-4, lt.size(vertices)+1):
        print(lt.getElement(vertices, i))
    
    print()
    print("Total de arcos incluidos: ", lt.size(arcos))
    print()
    print_tabla(arcos)
    print()
    print("Total de comparendos del camino: ", comparendos)
    print("Total de kilometros del camino: ", km, " km")
    print()
    print("Tiepo de ejección [ms] ", d_time)


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

def print_tabla(list, sample=5, maxcol=None):
    size = lt.size(list)
    if size <= sample*2:
        print("Hay menos de", sample*2,  "registros...")
        print(tabulate(lt.iterator(list),headers="keys", tablefmt = "grid", showindex=False, maxcolwidths=maxcol))
    else:
        print("Hay más de", sample*2, "registros...")
        list_sample = lt.subList(list,1,sample)
        list_ultimos = lt.subList(list,size-(sample-1),sample)
        for dato in lt.iterator(list_ultimos):
            lt.addLast(list_sample, dato)
        print(tabulate(lt.iterator(list_sample),headers="keys", tablefmt = "grid", showindex=False, maxcolwidths=maxcol))

def print_carga(vertices, min_long, min_lat, max_long, max_lat, estaciones, comparendos, arcos, t_arcos, d_time):
    print("===================================================")
    print("================ COMPARENDOS 2019 =================")
    print("===================================================")
    print()
    print("Total de comparendos cargados: ", lt.size(comparendos))
    print()
    print_tabla(comparendos, maxcol=35)
    print()
    print("Total de estaciones de policia cargadas: ", lt.size(estaciones))
    print()
    print_tabla(estaciones, maxcol=35)
    print()
    print("Total de vertices en el grafo: ", lt.size(vertices))
    print()
    print_tabla(vertices)
    print()
    print("*********** Limites de la ciudad *************")
    print()
    print("     Latitud minima: ", min_long)
    print("     Latitud maxima: ", max_long)
    print("     Longitud minima: ", min_lat)
    print("     Longitud maxima: ", max_lat)
    print()
    print("Total de arcos del grafo: ", t_arcos)
    print()
    print_tabla(arcos)
    print()
    print("Tiempo totla de carga [ms]: ", d_time)


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
"""
if __name__ == "__main__":
    #Menu principal
"""
    
def thread_cycle():
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            vertices, min_long, min_lat, max_long, max_lat, estaciones, comparendos, arcos, t_arcos, d_time = load_data(control)
            print_carga(vertices, min_long, min_lat, max_long, max_lat, estaciones, comparendos, arcos, t_arcos, d_time)
        elif int(inputs) == 2:
            lat_i = float(input("Ingrese la latitud del punto de partida: \n"))
            long_i = float(input("Ingrese la longitud del punto de partida: \n"))
            lat_f = float(input("Ingrese la latitud del punto de llegda: \n"))
            long_f = float(input("Ingrese la lngitud del punto de llegada: \n"))
            print("Buscando camino ...")
            vertices, dist, d_time = controller.req_1(control, lat_i, long_i, lat_f, long_f)
            if vertices == None:
                print("Alguno de los puntos entre los que se desea buscar camino se encuentra fuera de los limites de Bogotá ")
            else:
                print_req_1(vertices, dist, d_time)

        elif int(inputs) == 3:
            lat_i = float(input("Ingrese la latitud del punto de partida: \n"))
            long_i = float(input("Ingrese la longitud del punto de partida: \n"))
            lat_f = float(input("Ingrese la latitud del punto de llegda: \n"))
            long_f = float(input("Ingrese la lngitud del punto de llegada: \n"))
            print("Buscando camino ...")
            vertices, dist, d_time = controller.req_2(control, lat_i, long_i, lat_f, long_f)
            if vertices == None:
                print("Alguno de los puntos entre los que se desea buscar camino se encuentra fuera de los limites de Bogotá ")
            print_req_2(vertices, dist, d_time)

        elif int(inputs) == 4:
            localidad= input("Ingrese la localidad dónde se desea instalar las cámaras: \n")
            m= int(input("Ingrese la cantidad de cámaras de video que se desean instalar (M): \n"))
            result , d_time = controller.req_3(control, localidad , m)
            print_req_3(result, d_time)

        elif int(inputs) == 5:
            n = int(input("Ingrese el numero de camaras de la red: \n"))
            
            total_vertices, lista_vertices, arcos, total_km, costo, d_time = controller.req_4(control, n)
            
            print_req_4(total_vertices, lista_vertices, arcos, total_km, costo, d_time)

        elif int(inputs) == 6:
            clase_carro= input("Ingrese la clase de vehiculo que desea consultar: \n")
            camaras= input("Ingrese la cantidad de camaras que desea instalar: \n")
            total_vertices, lis_vertices, arcos, total_km, costo, d_time= controller.req_5(control,clase_carro.upper(), camaras)
            print_req_5(control, d_time, total_vertices, lis_vertices, arcos, total_km, costo)

        elif int(inputs) == 7:
            print_req_6(control)


        elif int(inputs) == 8:
            lat_i = float(input("Ingrese la latitud del punto de partida: \n"))
            long_i = float(input("Ingrese la longitud del punto de partida: \n"))
            lat_f = float(input("Ingrese la latitud del punto de llegda: \n"))
            long_f = float(input("Ingrese la lngitud del punto de llegada: \n"))
            print("Buscando camino ...")
            vertices, arcos, comparendos, km, d_time = controller.req_7(control, lat_i, long_i, lat_f, long_f)
            if vertices == None:
                print("Alguno de los puntos entre los que se desea buscar camino se encuentra fuera de los limites de Bogotá ")
            print_req_7(vertices, arcos, comparendos, km, d_time)

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
