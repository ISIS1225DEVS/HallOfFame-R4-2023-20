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


def load_data(control):
    """
    Carga los datos
    """
    contador_vertices, contador_arcos, contador_comparendos, contador_estaciones, lista_comparendos_10, lista_estaciones_10, lista_vertices_10, lista_arcos_10 = controller.load_data(control)
    return contador_vertices, contador_arcos, contador_comparendos, contador_estaciones, lista_comparendos_10, lista_estaciones_10, lista_vertices_10, lista_arcos_10


def print_carga_datos(contador_vertices, contador_arcos, contador_comparendos, contador_estaciones, lista_comparendos_10, lista_estaciones_10, lista_vertices_10, lista_arcos_10):
    print('HAY ' + str(contador_vertices) + ' VERTICES EN EL GRAFO')
    print('HAY ' + str(contador_arcos) + ' ARCOS EN EL GRAFO')
    print('HAY ' + str(contador_comparendos) + ' COMPARENDOS')
    print('HAY ' + str(contador_estaciones) + ' ESTACIONES')

    print('LOS PRIMEROS 5 Y ULTIMOS 5 COMPARENDOS SON')
    print(lista_comparendos_10)
    print('LAS PRIMEROS 5 Y ULTIMOS 5 ESTACIONES SON')
    print(lista_estaciones_10)
    print('LOS PRIMEROS 5 Y ULTIMOS 5 VERTICES SON')
    print(lista_vertices_10)
    print('LOS PRIMEROS 5 Y ULTIMOS 5 ARCOS SON')
    print(lista_arcos_10)
    


    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    punto_origen_lat = float(input('Ingresa el punto de origen - LAT: '))
    punto_origen_lon = float(input('Ingresa el punto de origen - LON: '))
    punto_destino_lat = float(input('Ingresa el punto de destino - LAT: '))
    punto_destino_lon = float(input('Ingresa el punto de destino - LON: '))
    distancia, cant_nodos, camino = controller.req_1(control, punto_origen_lat, punto_origen_lon, punto_destino_lat, punto_destino_lon)
    print('\n\n')
    print('LA DISTANCIA TOTAL DEL CAMINO ES DE: ' + str(distancia))
    print('LA CANTIDAD DE NODOS POR LA QUE PASA EL CAMINO ES DE: ' + str(cant_nodos))
    print('EL CAMINO HALLADO ES: ', camino)


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    localidad = input('Ingrese la localidad a evaluar: ')
    cantidad_cams = int(input('Ingrese la cantidad de camaras a agregar: '))
    cant_vertices, lista_vertices, lista_arcos, dist_total= controller.req_3(control, localidad, cantidad_cams)
    print('La cantidad de vertices por la que se pasa para llegar son: ' + str(cant_vertices))
    print(lista_vertices)
    print('\n\n\n')
    print('==========================LISTA DE ARCOS PARA LLEGAR A LOS DESTINOS==========================')
    print(lista_arcos)
    print('LA DISTANCIA TOTAL PARA LLEGAR A TODOS LOS DESTINOS ES DE ' + str(dist_total) + ' kilometros.')
    print('El costo total con 1.000.000COP por kilometro sería de: ' + str(dist_total*(10**6)) + ' pesos')


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    cantidad_cams = int(input('Ingrese la cantidad de camaras a agregar: '))
    r=controller.req_4(control,cantidad_cams)
    print(r)
    cantidad_cams = int(input('Ingrese la cantidad de camaras a agregar: '))
    cant_vertices, lista_vertices, lista_arcos, dist_total=controller.req_4(control,cantidad_cams)
    print('La cantidad de vertices por la que se pasa para llegar son: ' + str(cant_vertices))
    print(lista_vertices)
    print('\n\n\n')
    print('==========================LISTA DE ARCOS PARA LLEGAR A LOS DESTINOS==========================')
    print(lista_arcos)
    print('LA DISTANCIA TOTAL PARA LLEGAR A TODOS LOS DESTINOS ES DE ' + str(dist_total) + ' kilometros.')
    print('El costo total con 1.000.000COP por kilometro sería de: ' + str(dist_total*(10**6)) + ' pesos')

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
    num_comparendo_graves = int(input('Ingrese el numero de comparendos a analizar: '))
    hash_map = controller.req_6(control, num_comparendo_graves)
    key_set = mp.keySet(hash_map)
    for comparendo in lt.iterator(key_set):
        llv_dic = mp.get(hash_map, comparendo)
        dicc = me.getValue(llv_dic)
        print('\n')
        print('PARA ATENDER EL COMPARENDO UBICADO EN: ' + comparendo)
        print('SE ATENDERA DE LA ESTACION UBICADA EN EL VERTICE: ' + dicc['mejor_vert_est'])
        print('HAY UNA DISTANCIA DE: ' + str(dicc['distancia_estacion']) + ' KILOMETROS ENTRE LA ESTACION Y EL COMPARENDO')
        print('LOS VERTICES POR LOS QUE SE PASA SON: ', dicc['vertices'])
        print('LOS ARCOS POR LOS QUE SE PASA SON: ', dicc['arcos'])
        print('\n')




def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    punto_origen_lat = float(input('Ingresa el punto de origen - LAT: '))
    punto_origen_lon = float(input('Ingresa el punto de origen - LON: '))
    punto_destino_lat = float(input('Ingresa el punto de destino - LAT: '))
    punto_destino_lon = float(input('Ingresa el punto de destino - LON: '))

    cantidad_vertices, lista_vertices, lista_arcos, cant_comparendos, dist_km = controller.req_7(control, punto_origen_lat, punto_origen_lon, punto_destino_lat, punto_destino_lon)
    print('LA CANTIDAD DE VERTICES DEL CAMINO SON ' + str(cantidad_vertices))
    print('LA CANTIDAD DE COMPARENDOS DEL CAMINO SON ' + str(cant_comparendos))
    print('LA DISTANCIA DEL CAMINO ES ' + str(dist_km))
    print('LOS VERTICES POR LOS QUE HAY QUE PASAR SON: ')
    print(lista_vertices)
    print('LOS ARCOS POR LOS QUE HAY QUE PASAR SON: ')
    print(lista_arcos)


    


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
            contador_vertices, contador_arcos, contador_comparendos, contador_estaciones, lista_comparendos_10, lista_estaciones_10, lista_vertices_10, lista_arcos_10 = load_data(control)
            print_carga_datos(contador_vertices, contador_arcos, contador_comparendos, contador_estaciones, lista_comparendos_10, lista_estaciones_10, lista_vertices_10, lista_arcos_10)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

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
