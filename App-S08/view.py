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
    print_tabulate(list_arcos, ['id', 'edges'], True)
    keys_multas = ['OBJECTID', 'LATITUD', 'LONGITUD', 'FECHA_HORA', 'MEDIO_DETECCION', 'CLASE_VEHICULO', 'TIPO_SERVICIO', 'INFRACCION', 'DES_INFRACCION']
    print_tabulate(list_multas, keys_multas, True)
    keys_estaciones = ['OBJECTID', 'EPONOMBRE', 'EPOLATITUD', 'EPOLONGITU', 'EPODESCRIP', 'EPODIR_SITIO', 'EPOSERVICIO', 'EPOHORARIO', 'EPOTELEFON', 'EPOCELECTR']
    print_tabulate(list_estaciones, keys_estaciones, True)
    borders = control['model']['borders']
    print('Borders:', borders)
    print('Tiempo de carga:', d_time, 'ms')

def print_tabulate(data_struct, columns, loaddata=False):
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

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, lat_origin, long_origin, lat_dest, long_dest):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    total_distancy, total_vertex, path = controller.req_1(control, lat_origin, long_origin, lat_dest, long_dest)
    print('Distancia total (en metros):', total_distancy)
    print('Total de vértices:', total_vertex)
    lst = []
    pathstr = ''
    for element in lt.iterator(path):
        lst.append(element)
        pathstr += '-->' + str(element)
    print(lst)
    print(path)


def print_req_2(control, lat_origin, long_origin, lat_dest, long_dest):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    total_distancy, total_vertex, path = controller.req_2(control, lat_origin, long_origin, lat_dest, long_dest)
    print('Distancia total (en metros):', total_distancy)
    print('Total de vértices:', total_vertex)
    lst = []
    pathstr = ''
    for element in lt.iterator(path):
        lst.append(element)
        pathstr += '-->' + str(element)
    print(lst)
    print(path)


def print_req_3(control, camaras, localidad):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    total_distancy, total_vertex = controller.req_3(control, camaras, localidad)
    print('Distancia total (en metros):', total_distancy)
    print('Total de vértices:', total_vertex)
    print('Generando un costo de: '  + (total_distancy * 10000000))
 
def print_req_4(control, camaras):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    req4 = controller.req_4(control, m)
    return req4


def print_req_5(control, camaras, tipo_vehiculo):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    respuesta = controller.req_5(control, camaras, tipo_vehiculo)

def print_req_6(control, comparendos):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pathTo = controller.req_6(control, comparendos)
    i = 1
    for element in lt.iterator(pathTo):
        print('Información del comparendo #' + str(i) + ' más grave\n')
        print('Estación de policia más cercana:', element['station'])
        print('Vértice del comparendo:', element['vertex_fee'])
        print('Gravedad del comparendo:', element['fee']['INFRACCION'])
        print('Total de distancia (km):', round((element['km']/1000), 3))
        print('Total de vértices:', element['total_vertex'])
        print('RECORRIDO:\n')
        
        for minipath in element['arcos']:
            print(minipath['vertexB'], '-->', minipath['vertexA'])
        print('\n')
        i += 1
    pass


def print_req_7(control, lat_origin, long_origin, lat_dest, long_dest):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    total_distancy, total_vertex, path = controller.req_7(control, lat_origin, long_origin, lat_dest, long_dest)
    print('Distancia total (en metros):', total_distancy)
    print('Total de vértices:', total_vertex)
    i = 1
    str_final = ''
    for vertex in lt.iterator(path):
        if str_final == '':
            str_final += str(vertex)
        else:
            str_final += ' --> ' + str(vertex)
    print(str_final)


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
        #try:
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
            print_req_1(control, lat_origin, long_origin, lat_dest, long_dest)

        elif int(inputs) == 3:
            #Punto de origen
            lat_origin = float(input('Ingrese la latitud del punto de origen: '))
            long_origin = float(input('Ingrese la longitud del punto de origen: '))
            #Punto de destino
            lat_dest = float(input('Ingrese la latitud del punto de destino: '))
            long_dest = float(input('Ingrese la longitud del punto de destino: '))
            print_req_2(control, lat_origin, long_origin, lat_dest, long_dest)

        elif int(inputs) == 4:
            camaras = int(input("Ingrese la cantidad de cámaras de video que se desean instalar: "))
            localidad = input("Ingrese la localidad donde se desean instalar: ")
            print_req_3(control, camaras, localidad)

        elif int(inputs) == 5:
            m = int(input('Ingrese cantidad: '))
            print_req_4(control, m)

        elif int(inputs) == 6:
            camaras = int(input("Ingrese el número de cámaras que deséa instalar: "))
            tipo_vehiculo = input("Ingrese el tipo de vehiculo que desea consultar: ")
            print_req_5(control, camaras, tipo_vehiculo)

        elif int(inputs) == 7:
            comparendos = int(input('Digite la cantidad de comparendos para buscar: '))
            print_req_6(control, comparendos)

        elif int(inputs) == 8:
            lat_origin = float(input('Ingrese la latitud del punto de origen: '))
            long_origin = float(input('Ingrese la longitud del punto de origen: '))
            #Punto de destino
            lat_dest = float(input('Ingrese la latitud del punto de destino: '))
            long_dest = float(input('Ingrese la longitud del punto de destino: '))
            print_req_7(control, lat_origin, long_origin, lat_dest, long_dest)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
        #except Exception as exp:
        #    print('Hubo un error, vuelva a intentar.')
        #    print('Error:')
        #    print(exp)
    sys.exit(0)