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
from datetime import datetime
sys.setrecursionlimit(2**30)
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

def ask_bono():
    print('¿Desea guardar un archivo con el resultado?')
    print('1. Si')
    print('2. No')
    user = int(input('Digite su opción: '))
    if user == 1:
        bono = True
    else:
        bono = False
    return bono

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    d_time = controller.load_data(control)
    list_vertex = control['model']['lst_vertices']    
    list_arcos = control['model']['lst_arcos']
    list_multas = control['model']['lst_comparendos']
    list_estaciones = control['model']['lst_estaciones']

    print_tabulate(list_vertex, ['id', 'lat', 'long'], True)
    print_tabulate(list_arcos, ['vertexA', 'vertexB'], True)
    keys_multas = ['OBJECTID', 'LATITUD', 'LONGITUD', 'FECHA_HORA', 'MEDIO_DETECCION', 'CLASE_VEHICULO', 'TIPO_SERVICIO', 'INFRACCION', 'DES_INFRACCION']
    print_tabulate(list_multas, keys_multas, True)
    keys_estaciones = ['OBJECTID', 'EPONOMBRE', 'EPOLATITUD', 'EPOLONGITU', 'EPODESCRIP', 'EPODIR_SITIO', 'EPOSERVICIO', 'EPOHORARIO', 'EPOTELEFON', 'EPOCELECTR']
    print_tabulate(list_estaciones, keys_estaciones, True)
    borders = control['model']['borders']
    print('Borders:', borders)
    print('Tiempo de carga:', d_time, 'ms')

def print_tabulate(data_struct, columns, loaddata=False):
    try:
        data = data_struct

        print('Tamaño de la consulta:', lt.size(data))
        if data == None:
            return 'No hay datos'

        #Filtrar solo ultimos y primeros 3 datos si es muy grande la lista
        if not loaddata:
            data = controller.get_first_last_three(data_struct)
            print('Se encontraron más de 6 resultados...')
        elif loaddata:
            data = controller.get_first_last_five(data_struct)
            print('Se encontraron más de 10 resultados...')

        #Lista vacía para crear la tabla
        reduced = []

        #Iterar cada línea de la lista
        for temblor in lt.iterator(data):
            line = []
            #Iterar las columnas para solo imprimir las deseadas
            for column in columns:
                line.append(temblor[column])
            reduced.append(line)
        table = tabulate(reduced, headers=columns, tablefmt="grid", maxcolwidths=30)
        print(table)
    except:
        print(controller.colorama.Fore.RED + 'Hubo un error al intentar de imprimir la tabla')
        print(controller.colorama.Fore.RESET)

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, lat_origin, long_origin, lat_dest, long_dest, bono):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    total_distancy, total_vertex, path = controller.req_1(control, lat_origin, long_origin, lat_dest, long_dest, bono)
    print('Distancia total (km):', round(total_distancy/1000, 3))
    print('Total de vértices:', total_vertex)
    print_tabulate(path, ['vertices'], True)


def print_req_2(control, lat_origin, long_origin, lat_dest, long_dest, bono):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    total_distancy, total_vertex, path = controller.req_2(control, lat_origin, long_origin, lat_dest, long_dest, bono)
    print('Distancia total (en metros):', round(total_distancy/1000, 3))
    print('Total de vértices:', total_vertex)
    print_tabulate(path, ['vertices'], True)


def print_req_3(control, localidad, num_cam):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    sub_n, dist, dT = controller.req_3(control, localidad, num_cam)
    print(f"Tiempo Algoritmo: {dT}")
    print(f"Total vértices: {num_cam}")
    print("Vértices incluidos: ")
    for vertice in lt.iterator(sub_n):
        print(vertice[0])
    print(f"Cantidad de kilómetros: {dist}")
    print(f"Costo monetario(COP): {dist*1000000}")


def print_req_4(control, camaras, bono):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    vertices, arcos, total_weight = controller.req_4(control, camaras, bono)
    print('Total de km:', round(total_weight/1000, 3))
    print('Costo monetario:', round(total_weight*1000), '$')
    print('Vertices:')
    print_tabulate(vertices, ['vertices'], True)
    print_tabulate(arcos, ['vertexA', 'vertexB', 'weight'], True)


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control, comparendos, bono):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pathTo = controller.req_6(control, comparendos, bono)
    i = 1
    for element in lt.iterator(pathTo):
        print('Información del comparendo #' + str(i) + ' más grave\n')
        print('Estación de policia más cercana:', element['station'])
        print('Vértice del comparendo:', element['vertex_fee'])
        print('Gravedad del comparendo:', element['fee']['INFRACCION'])
        print('Total de distancia (km):', round((element['km']/1000), 3))
        print('Total de vértices:', element['total_vertex'])
        print('RECORRIDO:\n')
        print_tabulate(element['arcos'], ['vertexA', 'vertexB', 'weight'], True)
        i += 1
    pass


def print_req_7(control, lat_origin, long_origin, lat_dest, long_dest, bono):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    total_distancy, total_vertex, path = controller.req_7(control, lat_origin, long_origin, lat_dest, long_dest, bono)
    print('Total de km:', round(total_distancy/1000, 3))
    print('Total de vértices:', total_vertex)
    print('Arcos:')
    print_tabulate(path, ['vertexA', 'vertexB', 'weight'])


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        try:
            print_menu()
            inputs = input('Seleccione una opción para continuar\n')
            if int(inputs) == 1:
                print("Cargando información de los archivos ....\n")
                control = new_controller()
                data = load_data(control)
            elif int(inputs) == 2:
                #Punto de origen
                lat_origin = float(input('Ingrese la latitud del punto de origen: '))
                long_origin = float(input('Ingrese la longitud del punto de origen: '))
                #Punto de destino
                lat_dest = float(input('Ingrese la latitud del punto de destino: '))
                long_dest = float(input('Ingrese la longitud del punto de destino: '))
                bono = ask_bono()
                print_req_1(control, lat_origin, long_origin, lat_dest, long_dest, bono)

            elif int(inputs) == 3:
                #Punto de origen
                lat_origin = float(input('Ingrese la latitud del punto de origen: '))
                long_origin = float(input('Ingrese la longitud del punto de origen: '))
                #Punto de destino
                lat_dest = float(input('Ingrese la latitud del punto de destino: '))
                long_dest = float(input('Ingrese la longitud del punto de destino: '))
                bono = ask_bono()
                print_req_2(control, lat_origin, long_origin, lat_dest, long_dest, bono)

            elif int(inputs) == 4:
                localidad = input("Ingrese la localidad: ")
                num_cam = int(input("Ingrese el número de cámaras: "))
                print_req_3(control, localidad, num_cam)

            elif int(inputs) == 5:
                camaras = int(input('Ingrese la cantidad de cámaras: '))
                bono = ask_bono()
                print_req_4(control, camaras, bono)

            elif int(inputs) == 6:
                print_req_5(control)

            elif int(inputs) == 7:
                comparendos = int(input('Digite la cantidad de comparendos para buscar: '))
                bono = ask_bono()
                print_req_6(control, comparendos, bono)

            elif int(inputs) == 8:
                lat_origin = float(input('Ingrese la latitud del punto de origen: '))
                long_origin = float(input('Ingrese la longitud del punto de origen: '))
                #Punto de destino
                lat_dest = float(input('Ingrese la latitud del punto de destino: '))
                long_dest = float(input('Ingrese la longitud del punto de destino: '))
                bono = ask_bono()
                print_req_7(control, lat_origin, long_origin, lat_dest, long_dest, bono)

            elif int(inputs) == 9:
                print_req_8(control)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa")
                
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except Exception as exp:
            print(controller.colorama.Fore.RED + 'Hubo un error, vuelva a intentar. :(')
            print(controller.colorama.Fore.RESET)
            print('Error:')
            print(exp)
    sys.exit(0)
