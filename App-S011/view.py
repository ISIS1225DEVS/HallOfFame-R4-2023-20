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

default_limit = 1000
sys.setrecursionlimit(default_limit*1000)
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

    control= controller.new_controller()
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


arcosFile= "Data/bogota_arcos.txt"
verticesFile="Data/bogota_vertices.txt"
#comparendosFile="Data/comparendos_2019_bogota_vertices.csv"
#esatcionesFile="Data/estacionpolicia.json"
comparendosFile="Data/comparendos_2019_bogota_vertices.csv"
esatcionesFile="Data/estacionpolicia_bogota_vertices.csv"



def load_data(control,arcosFile,verticesFile,comparendosFile,esatcionesFile):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    data= controller.load_data(control, arcosFile, verticesFile, comparendosFile, esatcionesFile)
    return data





def print_data(control):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    data= controller.printCarga(control)
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print("     NUMERO DE ESTACIONES CARGADAS: "+ str(data[0]))
    print("-----------------------------------------------------------------------")
    print("     PRIMEROS 5    :")
    print(tabulate(lt.iterator(data[1])))
    print("     ULTIMOS 5    :")
    print(tabulate(lt.iterator(data[2])))
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print("     NUMERO DE COMPARENDOS CARGADOS: "+ str(data[3]))
    print("-----------------------------------------------------------------------")
    print("     PRIMEROS 5    :")
    print(tabulate(lt.iterator(data[4])))
    print("     ULTIMOS 5    :")
    print(tabulate(lt.iterator(data[5])))
   
    
    

def print_req_1(control, iniLong, iniLati, desLong, desLati):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    data= controller.req_1(control, iniLong, iniLati, desLong, desLati)
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print("     DISTANCIA ENTRE LAS UBICACIONES: "+ str(data[0]))
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print("     NUMERO DE VERTICES EN EL CAMINO ENCONTRADO: "+ str(data[1]))
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    contador=0
    print("El camino de búsqueda entre la base y estación es:")
    path = data[2]
    if path is not None:
        while (not st.isEmpty(path)):
            stop = st.pop(path)
            print(stop)
            contador+=1
        print("El camino tiene una longitud de: " + str(contador))
    pass
    

    


def print_req_2(control, iniLong, iniLati, desLong, desLati):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2

    data= controller.req_1(control, iniLong, iniLati, desLong, desLati)
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print("     DISTANCIA ENTRE LAS UBICACIONES: "+ str(data[0]))
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print("     NUMERO DE VERTICES EN EL CAMINO ENCONTRADO: "+ str(data[1]))
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    contador=0
    print("El camino de búsqueda entre la base y estación es:")
    path = data[2]
    if path is not None:
        while (not st.isEmpty(path)):
            stop = st.pop(path)
            print(stop)
            contador+=1
        print("El camino tiene una longitud de: " + str(contador))
    
    pass




def print_req_3(analyzer):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    m = input("Ingrese la cantidad de cámaras deseadas: ")
    localidad = input("Ingrese la localidad: ")

    data = controller.req_3(analyzer, localidad, m)

    if data is None:
        print("No se encontró la localidad ingresada")
        return

    verticesIdentificados, verticesUtilizados, arcos, kms, precio = data

    print("VERTICES IDENTIFICADOS")
    print("=" * 20)
    for v in lt.iterator(verticesIdentificados):
        print(" -", v)

    print("=" * 20)
    print("VERTICES UTILIZADOS")
    print("=" * 20)
    for v in lt.iterator(verticesUtilizados):
        print(" -", v)

    print("=" * 20)
    print("ARCOS UTILIZADOS")
    print("=" * 20)
    print(tabulate(lt.iterator(arcos), headers="keys", tablefmt="prettys"))

    print("\nKilómetros totales:", kms)
    print("\nPrecio total:", precio)



def print_req_4(control):
    m = input("Ingrese la cantidad de cámaras deseadas: ")

    verticesIdentificados, verticesUtilizados, arcos, kms, precio = controller.req_4(control, m)

    print("VERTICES IDENTIFICADOS")
    print("=" * 20)
    for v in lt.iterator(verticesIdentificados):
        print(" -", v)

    print("=" * 20)
    print("VERTICES UTILIZADOS")
    print("=" * 20)
    for v in lt.iterator(verticesUtilizados):
        print(" -", v)

    print("=" * 20)
    print("ARCOS UTILIZADOS")
    print("=" * 20)
    print(tabulate(lt.iterator(arcos), headers="keys", tablefmt="prettys"))

    print("\nKilómetros totales:", kms)
    print("\nPrecio total:", precio)


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    data = controller.req_5(control, input("Ingrese la cantidad de cámaras: "), input("Ingrese el tipo de vehiculo: "))

    if data is None:
        print("No se encontró el tipo de vehiculo ingresado")
        return

    verticesIdentificados, verticesUtilizados, arcos, kms, precio = data

    print("VERTICES IDENTIFICADOS")
    print("=" * 20)
    for v in lt.iterator(verticesIdentificados):
        print(" -", v)

    print("=" * 20)
    print("VERTICES UTILIZADOS")
    print("=" * 20)
    for v in lt.iterator(verticesUtilizados):
        print(" -", v)

    print("=" * 20)
    print("ARCOS UTILIZADOS")
    print("=" * 20)
    #print(tabulate(lt.iterator(arcos), headers="keys", tablefmt="pretty"))
    print(tabulate(lt.iterator(arcos)))
    print("\nKilómetros totales:", kms)
    print("\nPrecio total:", precio)


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    m = input("Ingrese la cantidad de comparendos graves deseados: ")
    data = controller.req_6(control, m)

    for part in lt.iterator(data):
        print("Estacion", part["estacion"], "atendiendo comparendo en", part["atendiendo"], "desde", part["desde"])
        print("Camino de", part["distancia"], "km:")
        #print(tabulate(lt.iterator(part["camino"]), headers="keys", tablefmt="pretty"))
        print(tabulate(lt.iterator(part["camino"])))


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    data= controller.req_7(control)


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
            data = load_data(control,arcosFile,verticesFile,comparendosFile,esatcionesFile)
            print_data(control)
        elif int(inputs) == 2:
            iniLong= float(input(" Origen longitud:   "))
            #iniLong=-74.06511801444837
            iniLati= float(input(" Origen latitud:   "))
            #iniLati=4.60293518548777
            desLong= float(input(" Destino longitud:   "))
            #desLong=-74.13489678235523
            desLati= float(input(" Destino latitud:   "))
            #desLati= 4.693518613347496
            print_req_1(control, iniLong, iniLati, desLong, desLati)

        elif int(inputs) == 3:
            iniLong= float(input(" Origen longitud:   "))
            #iniLong=-74.06511801444837
            iniLati= float(input(" Origen latitud:   "))
            #iniLati=4.60293518548777
            desLong= float(input(" Destino longitud:   "))
            #desLong=-74.13489678235523
            desLati= float(input(" Destino latitud:   "))
            #desLati= 4.693518613347496
            print_req_2(control, iniLong, iniLati, desLong, desLati)
            

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