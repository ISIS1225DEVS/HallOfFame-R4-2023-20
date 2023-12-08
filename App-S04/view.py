﻿"""
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
    # Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control


def print_menu():
    print("\nBienvenido")
    print("0- Cargar información")
    print("1- Buscar camino de un punto A a un punto B")
    print("2- Buscar camino con menos intersecciones entre un punto A y un punto B")
    print("3- Buscar red de fibra óptica menos costosa para los M puntos con más comparendos de una localidad")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Buscar ruta más corta desde alguna estación de policía hasta los M comparendos más graves")
    print("7- Buscar camino con menos comparendos entre un punto A y un punto B")
    print("8- Graficar algún requerimiento (No implementado)")
    print('9- Monitoreo de memoria')
    print("10- Salir")


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Carga de datos
# =============================================================================================================================================================================
# =============================================================================================================================================================================

def load_data(control, memflag):
    """
    Carga los datos
    """
    # Realizar la carga de datos
    print("\nCargando...\n")
    count, time, memory = controller.load_data(control, memflag)
    print('\nInformación cargada')
    return count, time, memory

def askMemflag(memflag):
    print('\nMonitoreando memoria: '+str(memflag)+'\n')
    if memflag:
        print('Quiere seguir monitoreando memoria? ')
        print('1- Sí')
        print('2- No')
        meminput = int(input('Seleccione una opción:\n> '))
        if meminput == 2:
            memflag = False
    else:
        print('Quiere monitorear memoria? ')
        print('1- Sí')
        print('2- No')
        meminput = int(input('Seleccione una opción:\n> '))
        if meminput == 1:
            memflag = True
    return memflag

def printTable(lst, columns, n=3, colwidths=None):
    print(f'Mostrando los {n} primeros y {n} últimos datos cargados:')
    table_list = controller.createTopNList(lst, n)
    if colwidths is None:
        print(tabulate(lt.iterator(table_list), tablefmt='grid', headers=columns))
    else:
        print(tabulate(lt.iterator(table_list), tablefmt='grid', headers=columns, maxcolwidths=colwidths))

def printCityLimits(count):
    limits = count['limits']
    latmax = limits['latmax']
    latmin = limits['latmin']
    longmax = limits['longmax']
    longmin = limits['longmin']
    
    print('\nMostrando los límites de la ciudad:')
    columns = ['','Límite máximo', 'Límite mínimo']
    table = [['Latitud', latmax, latmin],
             ['Longitud', longmax, longmin]]
    print(tabulate(table, tablefmt='grid', headers=columns))

def printLoadedData(control, count, time, memory):
    """
        Función que imprime un dato dado su ID
    """
    # Realizar la función para imprimir un elemento
    # print title
    bars = '='
    neg = '\n'
    print(neg)
    print(bars*49)
    print(bars*8 + ' Imprimiendo información cargada ' + bars*8)
    print(bars*49)
    print(neg)
    
    # get lists
    stations, tickets, vertices, edges = controller.getDataLists(control)
    # print time and memory
    deltaTimeAndMemory(time, memory)
    # print tickets
    columns = ['ID', 'Latitud', 'Longitud', 'Fecha', ' Medio de detección',
               'Vehículo', 'Servicio', 'Infracción', 'Descripción']
    size = controller.getListSize(tickets)
    colwidths = [None, None, None, None, None,
               None, None, 20, 30]
    print(f'{neg}{bars*4} Comparendos {bars*4}{neg}')
    print(f'Total de comparendos: {size}{neg}')
    printTable(tickets, columns, 5, colwidths)
    
    # print stations
    columns = ['ID', 'Nombre', 'Latitud', 'Longitud', 'Descripción',
              'Dirección', 'Servicio', 'Horario', 'Teléfono', 'Correo electrónico']
    size = controller.getListSize(stations)
    colwidths = [None, 10, None, None, 10,
              10, 30, 20, None, None]
    print(f'{neg}{bars*4} Estaciones {bars*4}{neg}')
    print(f'Total de estaciones: {size}{neg}')
    printTable(stations, columns, 5, colwidths)
    
    # print vertices
    columns = ['ID', 'Latitud', 'Longitud']
    size = controller.getListSize(vertices)
    print(f'{neg}{bars*4} Vertices cargados {bars*4}{neg}')
    print(f'Total de vertices: {size}{neg}')
    printTable(vertices, columns, 5)
    
    printCityLimits(count)
    
    # print edges
    columns = ['ID', 'ID de vecinos cargados']
    size = controller.getEdges(control)
    print(f'{neg}{bars*4} Arcos cargados {bars*4}{neg}')
    print('Total de arcos: '+str(size) + neg)
    printTable(edges, columns, 5)
    
# print time and memory
    
def deltaTimeAndMemory(time, memory):
    if memory is not None:
        print(f'\nTiempo [ms]: {round(time, 3)}')
        print(f'Memoria [kb]: {round(memory, 3)}')
    else:
        print(f'\nTiempo [ms]: {round(time, 3)}')


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Requerimientos
# =============================================================================================================================================================================
# =============================================================================================================================================================================


# =============================================================================================================================================================================
# req1

def print_req_1(control, memflag):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # Imprimir el resultado del requerimiento 1
    prueba = int(input('\nDesea realizar una prueba?\n1- Sí\n2- No\n> '))
    if prueba != 1:
        lati = input('\nIngrese una latitud inicial: ')
        longi = input('Ingrese una longitud inicial: ')
        latf = input('Ingrese una latitud final: ')
        longf = input('Ingrese una longitud final: ')
    else:
        lati = 4.60293518548777
        longi = -74.06511801444837
        latf = 4.693518613347496
        longf = -74.13489678235523
    
    print('\nCargando información...')
    
    path_q, count, time, memory = controller.req1(control, lati, longi, latf, longf, memflag)
    
    deltaTimeAndMemory(time, memory)
    
    if not qu.isEmpty(path_q):
        distance = count['distance']
        path_size = qu.size(path_q)
        print(f'\nDistancia total del camino [km]: {round(distance, 3)}')
        print(f'Total de vertices en el camino: {path_size}\n')
        if path_size <= 500:
            print('Mostrando camino:')
        else:
            print('Mostrando primeras y últimas 3 paradas')
        i = 0
        while not qu.isEmpty(path_q):
            vertex = qu.dequeue(path_q)
            if path_size <= 500:
                if i == 0:
                    print(f'Vértice de partida: {vertex}')
                elif i == path_size-1:
                    print(f'Vértice destino: {vertex}')
                else:
                    print(f'Parada número {i}: {vertex}')
            else:
                if i == 0:
                    print(f'Vértice de partida: {vertex}')
                elif i == path_size-1:
                    print(f'Vértice destino: {vertex}')
                elif i in [1,2,3] or i in [path_size-4, path_size-3, path_size-2]:
                    print(f'Parada número {i}: {vertex}')
            i += 1
                
        print('\nInformación cargada\n')
            
    else:
        print('\nNo se encontró ningún camino')


# =============================================================================================================================================================================
# req2

def print_req_2(control, memflag):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # Imprimir el resultado del requerimiento 2
    prueba = int(input('\nDesea realizar una prueba?\n1- Sí\n2- No\n> '))
    if prueba != 1:
        lati = input('\nIngrese una latitud inicial: ')
        longi = input('Ingrese una longitud inicial: ')
        latf = input('Ingrese una latitud final: ')
        longf = input('Ingrese una longitud final: ')
    else:
        lati = '4.60293518548777'
        longi = '-74.06511801444837'
        latf = '4.693518613347496'
        longf = '-74.13489678235523'
    
    print('\nCargando información...')
    
    path_q, count, time, memory = controller.req2(control, lati, longi, latf, longf, memflag)
    
    deltaTimeAndMemory(time, memory)
    
    if not qu.isEmpty(path_q):
        distance = count['distance']
        path_size = qu.size(path_q)
        print(f'\nDistancia total del camino [km]: {round(distance, 3)}')
        print(f'Total de vertices en el camino: {path_size}\n')
        if path_size <= 500:
            print('Mostrando camino:')
        else:
            print('Mostrando primeras y últimas 3 paradas')
        i = 0
        while not qu.isEmpty(path_q):
            vertex = qu.dequeue(path_q)
            if path_size <= 500:
                if i == 0:
                    print(f'Vértice de partida: {vertex}')
                elif i == path_size-1:
                    print(f'Vértice destino: {vertex}')
                else:
                    print(f'Parada número {i}: {vertex}')
            else:
                if i == 0:
                    print(f'Vértice de partida: {vertex}')
                elif i == path_size-1:
                    print(f'Vértice destino: {vertex}')
                elif i in [1,2,3] or i in [path_size-4, path_size-3, path_size-2]:
                    print(f'Parada número {i}: {vertex}')
            i += 1
                
        print('\nInformación cargada\n')
            
    else:
        print('\nNo se encontró ningún camino')
    

# =============================================================================================================================================================================
# req3

def print_req_3(control, memflag):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # Imprimir el resultado del requerimiento 3
    prueba = int(input('\nDesea realizar una prueba?\n1- Si\n2- No\n> '))
    if prueba != 1:
        cameras = int(input('\nCantidad de cámaras a instalar: '))
        localidad = input('Ingrese el nombre de la localidad a evaluar: ')
        localidad = localidad.lower()
    else:
        cameras = 20
        localidad = 'chapinero'
    
    cost = 1000000
    
    print('\nCargando información...')
    
    paths, vertex_path_list, first_vertex_index, count, time, memory = controller.req3(control, cameras, localidad, cost, memflag)
    
    deltaTimeAndMemory(time, memory)
    paths = paths['edgeTo']
    c = 1
    if count["distance"] != 0:
        print(f'\nKilometraje total de la red: {round(count["distance"], 3)} [km]')
        print(f'Costo total de la red: ${round(count["cost"], 3)} COP')
        print('\n==== Arcos incluidos ====\n')
        # count = controller.getReq3Vertices(paths, vertex_path_list, count)
        st.push(count['included_vertices'], first_vertex_index)
        for vertex in lt.iterator(vertex_path_list):
            if vertex not in count["total_vertices"]:
                        count['total_vertices'].append(vertex)
            if vertex != first_vertex_index:
                entry = mp.get(paths, vertex)
                edge = me.getValue(entry)
                st.push(count['included_vertices'], vertex)
                vi = edge['vertexA']
                vf = edge['vertexB']
                print(f'Arco número {c}: {vi} --> {vf}')
                c += 1
        print('\n')
        print('='*40)
        print(f'\nTotal de vértices: {len(count["total_vertices"])}')
        print('\n==== Vértices principales incluidos ====')
        print('\n')
        while not st.isEmpty(count['included_vertices']):
            print(st.pop(count['included_vertices']))

        print('\nInformación cargada\n')

    else:
        print('\nNo se encontró ninguna red óptima')


# =============================================================================================================================================================================
# req4

def print_req_4(control, memflag):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    wholein = int(input('\nDesea seguir la malla vial?\n1- No\n2- Sí\n> '))
    if wholein == 1:
        whole = False
    else:
        whole = True
    
    prueba = int(input('\nDesea realizar una prueba?\n1- Si\n2- No\n> '))
    if prueba != 1:
        cameras = int(input('Cantidad de cámaras de video que desea instalar: '))
    else:
        cameras = 20
    cost = 1000000
    
    print('\nCargando información...')
    
    paths, vertex_path_list, first_vertex_index, count, time, memory = controller.req_4(control, cameras, cost, whole, memflag)
    
    deltaTimeAndMemory(time, memory)
    paths = paths['edgeTo']
    c = 1
    if count["distance"] != 0:
        print(f'\nKilometraje total de la red: {round(count["distance"], 3)} [km]')
        print(f'Costo total de la red: ${round(count["cost"], 3)} COP')
        print('\n==== Arcos incluidos ====\n')
        # count = controller.getReq3Vertices(paths, vertex_path_list, count)
        st.push(count['included_vertices'], first_vertex_index)
        for vertex in lt.iterator(vertex_path_list):
            if vertex not in count["total_vertices"]:
                        count['total_vertices'].append(vertex)
            if vertex != first_vertex_index:
                entry = mp.get(paths, vertex)
                edge = me.getValue(entry)
                st.push(count['included_vertices'], vertex)
                vi = edge['vertexA']
                vf = edge['vertexB']
                print(f'Arco número {c}: {vi} --> {vf}')
                c += 1
        print('\n')
        print('='*40)
        print(f'\nTotal de vértices: {len(count["total_vertices"])}')
        print('\n==== Vértices principales incluidos ====')
        print('\n')
        while not st.isEmpty(count['included_vertices']):
            print(st.pop(count['included_vertices']))

        print('\nInformación cargada\n')

    else:
        print('\nNo se encontró ninguna red óptima')


# =============================================================================================================================================================================
# req5

def print_req_5(control, memflag):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    '''vehicle = 'AUTOMÓVIL'
    cameras = 10
    cost = None
    answer = controller.req_5(control, cameras, vehicle, cost, memflag)
    print(answer)'''
    prueba = int(input('\nDesea realizar una prueba?\n1- Si\n2- No\n> '))
    if prueba != 1:
        cameras = int(input('Cantidad de cámaras a instalar: '))
        vehicle = input('Ingrese el tip de vehiculo a evaluar: ')
    else:
        cameras = 10
        vehicle = 'AUTOMÓVIL'
    
    cost = 1000000
    
    print('\nCargando información...')
    
    paths, vertex_path_list, first_vertex_index, count, time, memory = controller.req5(control, cameras, vehicle, cost, memflag)
    
    deltaTimeAndMemory(time, memory)
    paths = paths['edgeTo']
    c = 1
    if count["distance"] != 0:
        print(f'\nKilometraje total de la red: {round(count["distance"], 3)} [km]')
        print(f'Costo total de la red: ${round(count["cost"], 3)} COP')
        print('\n==== Arcos incluidos ====\n')
        # count = controller.getReq3Vertices(paths, vertex_path_list, count)
        st.push(count['included_vertices'], first_vertex_index)
        for vertex in lt.iterator(vertex_path_list):
            if vertex not in count["total_vertices"]:
                        count['total_vertices'].append(vertex)
            if vertex != first_vertex_index:
                entry = mp.get(paths, vertex)
                edge = me.getValue(entry)
                st.push(count['included_vertices'], vertex)
                vi = edge['vertexA']
                vf = edge['vertexB']
                print(f'Arco número {c}: {vi} --> {vf}')
                c += 1
        print('\n')
        print('='*40)
        print(f'\nTotal de vértices: {len(count["total_vertices"])}')
        print('\n==== Vértices principales incluidos ====')
        print('\n')
        while not st.isEmpty(count['included_vertices']):
            print(st.pop(count['included_vertices']))

        print('\nInformación cargada\n')

    else:
        print('\nNo se encontró ninguna red óptima')


# =============================================================================================================================================================================
# req6

def print_req_6(control, memflag):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # Imprimir el resultado del requerimiento 6
    prueba = int(input('\nDesea realizar una prueba?\n1- Si\n2- No\n> '))
    if prueba != 1:
        tickets = int(input('\nCantidad de comparendos: '))
    else:
        tickets = 20
    
    print('\nCargando información...')
    
    paths, ticket_q, count, time, memory= controller.req6(control, tickets, memflag)
    
    deltaTimeAndMemory(time, memory)
    c = 1
    if not mp.isEmpty(paths):
        print(f'\nTotal de comparendos encontrados: {qu.size(ticket_q)}\n')
        print('==== Arcos incluidos ====')
        while not qu.isEmpty(ticket_q):
            vertex = qu.dequeue(ticket_q)
            st.push(count['included_vertices'], vertex)
            if vertex not in count["total_vertices"]:
                count['total_vertices'].append(vertex)
                
            entry = mp.get(paths, vertex)
            v = me.getValue(entry)
            gravedad = v['gravedad']
            path_stack = v['path']
            dist = v['dist']
            index = v['index']
            name = v['station']
            path_size = st.size(path_stack)
            print(f'\nVértice más cercano al comparendo número {c}: {index}')
            print(f'Gravedad del comparendo: {gravedad}')
            print(f'Estación más cercana: {name}')
            print(f'Distancia desde la estación más cercana [km]: {round(dist, 2)}')
            if tickets >= 5:
                print('Mostrando primeros y últimos 3 arcos del camino:')
            else:
                print('Mostrando todos los arcos del camino:')
            i = 0
            while not st.isEmpty(path_stack):
                edge = st.pop(path_stack)
                if tickets >= 5:
                    if i in [0,1,2]:
                        vi = edge['vertexA']
                        vf = edge['vertexB']
                        print(f'{vi} --> {vf}')
                    elif i in [path_size-3, path_size-2, path_size-1]:
                        vi = edge['vertexA']
                        vf = edge['vertexB']
                        print(f'{vi} --> {vf}')
                else:
                    vi = edge['vertexA']
                    vf = edge['vertexB']
                    print(f'{vi} --> {vf}')
                    
                if vi not in count["total_vertices"]:
                        count['total_vertices'].append(vi)
                if vf not in count["total_vertices"]:
                    count['total_vertices'].append(vf)
                    
                i += 1
            c += 1
            
        print('\n')
        print('='*40)
        print(f'\nTotal de vértices: {len(count["total_vertices"])}')
        print('\n==== Vértices principales incluidos ====')
        print('\n')
        while not st.isEmpty(count['included_vertices']):
            print(st.pop(count['included_vertices']))
        
        print('\nInformación cargada\n')
                
    else:
        print('\nNo se encontrararon caminos óptimos')


# =============================================================================================================================================================================
# req7

def print_req_7(control, memflag):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    prueba = int(input('\nDesea realizar una prueba?\n1- Sí\n2- No\n> '))
    if prueba != 1:
        lati = input('\nIngrese una latitud inicial: ')
        longi = input('Ingrese una longitud inicial: ')
        latf = input('Ingrese una latitud final: ')
        longf = input('Ingrese una longitud final: ')
    else:
        lati = 4.60293518548777
        longi = -74.06511801444837
        latf = 4.693518613347496
        longf = -74.13489678235523
    
    print('\nCargando información...')
    
    path_stack, count, time, memory = controller.req7(control, lati, longi, latf, longf, memflag)
    
    deltaTimeAndMemory(time, memory)
    
    if not qu.isEmpty(path_stack):
        distance = count['distance']
        tickets = count['tickets']
        path_size = qu.size(path_stack)
        print(f'\nDistancia total del camino [km]: {round(distance, 3)}')
        print(f'Total de comparendos en el camino: {tickets}')
        print(f'Total de vertices en el camino: {path_size}')
        if path_size <= 500:
            print('\nMostrando camino:')
        else:
            print('\nMostrando primeras y últimas 3 paradas')
        i = 0
        while not st.isEmpty(path_stack):
            a = qu.dequeue(path_stack)
            vi = a['vertexA']
            vf = a['vertexB']
            if i == 0:
                print(f'Vértice de partida: {vi}')
            
            if path_size <= 500:
                print(f'Arco número {i}: {vi} --> {vf}')
            else:
                if i in [1,2,3] or i in [path_size-3, path_size-2, path_size-1]:
                    print(f'Arco número {i}: {vi} --> {vf}')
                    
            if i == path_size:
                print(f'Vértice destino: {vf}')
                
            i += 1
                
        print('\nInformación cargada\n')
            
    else:
        print('\nNo se encontró ningún camino')


# =============================================================================================================================================================================
# req8

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# =============================================================================================================================================================================
# =============================================================================================================================================================================
# Main
# =============================================================================================================================================================================
# =============================================================================================================================================================================


# Se crea el controlador asociado a la vista
def menu_cycle():
    """
    Menu principal
    """
    control = new_controller()
    working = True
    memflag = False
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n> ')
        if int(inputs) == 0:
            if control['loaded']:
                control = new_controller()
            count, time, memory = load_data(control, memflag)
            printLoadedData(control, count, time, memory)
            
        elif int(inputs) == 1 and control['loaded']:
            print_req_1(control, memflag)

        elif int(inputs) == 2 and control['loaded']:
            print_req_2(control, memflag)

        elif int(inputs) == 3 and control['loaded']:
            print_req_3(control, memflag)

        elif int(inputs) == 4 and control['loaded']:
            print_req_4(control, memflag)

        elif int(inputs) == 5 and control['loaded']:
            print_req_5(control, memflag)

        elif int(inputs) == 6 and control['loaded']:
            print_req_6(control, memflag)

        elif int(inputs) == 7 and control['loaded']:
            print_req_7(control, memflag)

        elif int(inputs) == 8 and control['loaded']:
            print_req_8(control)
        
        elif int(inputs) == 9:
            memflag = askMemflag(memflag)

        elif int(inputs) == 10:
            working = False
            print("\nGracias por utilizar el programa.\n")
            
        else:
            print("\nOpción inválida.\n")
    sys.exit(0)

# main del reto
if __name__ == "__main__":
    threading.stack_size(67108864*2) # 128MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=menu_cycle)
    thread.start()