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
from DISClib.ADT import graph as gr
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback
import webbrowser

default_limit = 1000
sys.setrecursionlimit(default_limit*1000000)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def tabulatedData(registers, headers, detailHeaders=None, detailSize=None):
    width = detailSize if detailSize else 12
    table = []
    if lt.isEmpty(registers):
        return '\nCould not find the content.'
    for register in lt.iterator(registers):
        row = []
        for header in headers:
            datum = register[header]
            if detailHeaders and type(datum) == dict:
                datum =  tabulatedData(datum, detailHeaders)
            row.append(f'{datum} '.title()[:100])
        table.append(row)
    return tabulate(table, [header.replace('_', ' ').title() for header in headers], tablefmt='fancy_grid', maxheadercolwidths=width, maxcolwidths=width[:len(headers)-1] if detailSize and detailHeaders else width)

def newController():
    return controller.newController()

def printMenu():
    print("MENU")
    print("1- Load data")
    print("2- (Req. 1)")
    print("3- (Req. 2)")
    print("4- (Req. 3)")
    print("5- (Req. 4)")
    print("6- (Req. 5)")
    print("7- (Req. 6)")
    print("8- (Req. 7)")
    print("0- Go out\n")

def loadData(control):
    print("Loading data from files...\n")
    startTime = controller.getTime()
    controller.loadData(control)
    endTime = controller.getTime()
    print(f'Total infractions loaded: {lt.size(control["infractions"])}')
    print('The first and last 5 infractions are:')
    headers = ['OBJECTID', 'LATITUD', 'LONGITUD', 'FECHA_HORA', 'MEDIO_DETECCION', 'CLASE_VEHICULO', 'TIPO_SERVICIO', 'INFRACCION', 'DES_INFRACCION']
    print(tabulatedData(controller.firstAndLastNData(control["infractions"], 5), headers))
    print(f'\nTotal stations loaded: {lt.size(control["stations"])}')
    print('The first and last 5 stations are:')
    headers = ['OBJECTID', 'EPONOMBRE', 'EPOLATITUD', 'EPOLONGITU', 'EPODESCRIP', 'EPODIR_SITIO', 'EPOSERVICIO', 'EPOHORARIO', 'EPOTELEFON', 'EPOCELECTR']
    print(tabulatedData(controller.firstAndLastNData(control["stations"], 5), headers))
    print(f'\nTotal vertices loaded: {gr.numVertices(control["distanceGraph"])}')
    print('The first and last 5 vertices are:')
    headers = ['id', 'latitude', 'longitude']
    print(tabulatedData(controller.firstAndLastNData(control['vertices'], 5), headers))
    print(f"\nThe area is delimated by:\nMin Latitude: {round(control['metaData']['latitudes'][0], 4)} and Max Latitude: {round(control['metaData']['latitudes'][1], 4)}\nMin Longitude: {round(control['metaData']['longitudes'][0], 4)} and Max Longitude: {round(control['metaData']['longitudes'][1], 4)}\n")
    print(f'Total edges loaded: {gr.numEdges(control["distanceGraph"])}')
    print('The first and last 5 edges are:')
    headers = ['vertex', 'adjacentVertex']
    print(tabulatedData(controller.firstAndLastNData(control['edges'], 5), headers))
    deltaTime = round(controller.deltaTime(endTime, startTime), 2)
    print(f'\nExecution time: {deltaTime} ms')

def req1(control, startPoint, arrivalPoint):
    startTime = controller.getTime()
    filtered, metaData, deltaOfMemory= controller.req1(control, startPoint, arrivalPoint)
    endTime = controller.getTime()
    print(f'Starting point: {startPoint}')
    print(f'Arrival point: {arrivalPoint}\n')
    print(f"Total distance between starting point and arrival point: {round(metaData['totalDistance'], 4)} km")
    print(f"Total vertices visited: {metaData['totalVertex']}\n")
    print("The first and last 10 vertices on the route are:")
    headers = ['Starting Point', 'Arrival Point', 'Distance']
    print(tabulatedData(controller.firstAndLastNData(filtered, 10), headers))
    deltaTime = round(controller.deltaTime(endTime, startTime), 2)
    print(f'\nExecution time: {deltaTime} ms')
    print(f'Memory used: {deltaOfMemory}')
    displayMap(metaData)

def req2(control, startPoint, arrivalPoint):
    startTime = controller.getTime()
    filtered, metaData, deltaOfMemory = controller.req2(control, startPoint, arrivalPoint)
    endTime = controller.getTime()
    print(f'Starting point: {startPoint}')
    print(f'Arrival point: {arrivalPoint}\n')
    print(f"Total distance between starting point and arrival point: {round(metaData['totalDistance'], 4)} km")
    print(f"Total vertices visited: {metaData['totalVertex']}\n")
    print("The first and last 10 vertices on the route are:")
    headers = ['Starting Point', 'Arrival Point', 'Distance']
    print(tabulatedData(controller.firstAndLastNData(filtered, 10), headers))
    deltaTime = round(controller.deltaTime(endTime, startTime), 2)
    print(f'\nExecution time: {deltaTime} ms')
    print(f'Memory used: {deltaOfMemory}')
    displayMap(metaData)

def req3(control, locality, M):
    startTime = controller.getTime()
    filtered, metaData, deltaOfMemory = controller.req3(control, locality, M)
    endTime = controller.getTime()
    print(f"The best net of {M} cameras for the locality {locality.title()} has:")
    print(f"Total cameras: {metaData['totalVertices']}")
    print(f"Total distance: {round(metaData['totalDistance'], 4)} km")
    print(f"Total cost: ${round(metaData['totalDistance'], 4) * 1000000} pesos")
    print(f"\nThe steps are: ")
    headers = ['Starting Point', 'Arrival Point', 'Distance']
    print(tabulatedData(filtered, headers))
    deltaTime = round(controller.deltaTime(endTime, startTime), 2)
    print(f'\nExecution time: {deltaTime} ms')
    print(f'Memory used: {deltaOfMemory}')
    displayMap(metaData)

def req4(control, M):
    startTime = controller.getTime()
    filtered, metaData, deltaOfMemory = controller.req4(control, M)
    endTime = controller.getTime()
    print(f"The best net of {M} cameras according to the highest severity")
    print(f"Total cameras: {metaData['totalVertices']}")
    print(f"Total distance: {round(metaData['totalDistance'], 4)} km")
    print(f"Total cost: ${round(metaData['totalDistance'], 4) * 1000000} pesos")
    print(f"\nThe steps are: ")
    headers = ['Starting Point', 'Arrival Point', 'Distance']
    print(tabulatedData(filtered, headers))
    deltaTime = round(controller.deltaTime(endTime, startTime), 2)
    print(f'\nExecution time: {deltaTime} ms')
    print(f'Memory used: {deltaOfMemory}')
    displayMap(metaData)

def req5(control, vehicle, M):
    startTime = controller.getTime()
    filtered, metaData, deltaOfMemory = controller.req5(control, vehicle, M)
    endTime = controller.getTime()
    print(f"The best net of {M} cameras for the vehicle's class {vehicle.title()} has:")
    print(f"Total cameras: {metaData['totalVertices']}")
    print(f"Total distance: {round(metaData['totalDistance'], 4)} km")
    print(f"Total cost: ${round(metaData['totalDistance'], 4) * 1000000} pesos")
    print(f"\nThe steps are: ")
    headers = ['Starting Point', 'Arrival Point', 'Distance']
    print(tabulatedData(filtered, headers))
    deltaTime = round(controller.deltaTime(endTime, startTime), 2)
    print(f'\nExecution time: {deltaTime} ms')
    print(f'Memory used: {deltaOfMemory}')
    displayMap(metaData)

def req6(control, M):
    startTime = controller.getTime()
    filtered, metaData, deltaOfMemory = controller.req6(control, M)
    endTime = controller.getTime()
    print(f"The shortest paths to the {M} most several infractions are:")
    for path in lt.iterator(filtered):
        metaData = path['metaData']
        print(f"\n\nCalculating the shortest path from:")
        print(tabulatedData(metaData['infraction'], ['NUM_COMPARENDO', 'FECHA_HORA', 'CLASE_VEHICULO', 'TIPO_SERVICIO', 'INFRACCION']))
        print(f"Total vertices: {metaData['totalVertices']}")
        print(f"Total distance: {round(metaData['totalDistance'], 4)} km")
        print(f"The steps are: ")
        headers = ['Starting Point', 'Arrival Point', 'Distance']
        print(tabulatedData(path, headers))
    deltaTime = round(controller.deltaTime(endTime, startTime), 2)
    print(f'\nExecution time: {deltaTime} ms')
    print(f'Memory used: {deltaOfMemory}')
    displayMap(metaData)

def req7(control, startPoint, arrivalPoint):
    startTime = controller.getTime()
    filtered, metaData, deltaOfMemory = controller.req7(control, startPoint, arrivalPoint)
    endTime = controller.getTime()
    print(f'Starting point: {startPoint}')
    print(f'Arrival point: {arrivalPoint}\n')
    print(f"Total distance between starting point and arrival point: {round(metaData['totalDistance'], 4)} km")
    print(f"Total infractions between starting point and arrival point: {metaData['totalInfractions']}")
    print(f"Total vertices visited: {metaData['totalVertices']}\n")
    print("The first and last 10 vertices on the route are:")
    headers = ['Starting Point', 'Arrival Point', 'Distance', 'Num Infractions']
    print(tabulatedData(controller.firstAndLastNData(filtered, 10), headers))
    deltaTime = round(controller.deltaTime(endTime, startTime), 2)
    print(f'\nExecution time: {deltaTime} ms')
    print(f'Memory used: {deltaOfMemory}')
    displayMap(metaData)

def displayMap(metaData):
    if metaData["map"]:
        print("Do you want to watch the interactive map?\n1- Yes\n2- No")
        if input("Response: ") == "1":
            webbrowser.open_new_tab(f'{metaData["path"]}.html')

# Se crea el controlador asociado a la vista
control = newController()

# main del reto
if __name__ == "__main__":
    print("Welcome!\n")
    working = True
    while working:
        printMenu()
        inputs = input('Select an option to continue\n-> ')
        print()
        try:
            if int(inputs) == 1:
                loadData(control)

            elif int(inputs) == 2:
                req1(control, (input('Starting Latitude: '), input('Starting Longitude: ')), (input('Arrival Latitude: '), input('Arrival Longitude: ')))
            
            elif int(inputs) == 3:
                req2(control, (input('Starting Latitude: '), input('Starting Longitude: ')), (input('Arrival Latitude: '), input('Arrival Longitude: ')))

            elif int(inputs) == 4:
                req3(control, input('Locality: '), int(input('M: ')))
            
            elif int(inputs) == 5:
                req4(control, int(input('M: ')))
            
            elif int(inputs) == 6:
                req5(control, input("Vehicle's class: "), int(input('M: ')))
            
            elif int(inputs) == 7:
                req6(control, int(input('M: ')))
            
            elif int(inputs) == 8:
                req7(control, (input('Starting Latitude: '), input('Starting Longitude: ')), (input('Arrival Latitude: '), input('Arrival Longitude: ')))
            
            elif int(inputs) == 0:
                print("\nThanks for using the program.")
                working = False
            
            else:
                print("Wrong choice, choose again.\n")

        except ValueError:
            print("Please enter a valid option.\n")
        
        if working:
            input('\nPress any key to continue...\n\n')
    sys.exit(0)