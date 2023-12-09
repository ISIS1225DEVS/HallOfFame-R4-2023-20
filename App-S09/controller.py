"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import time
import csv
import tracemalloc
import json
import colorama

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        'model': None
    }
    control['model'] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    i_time = get_time()
    dir_vertex = cf.data_dir + 'tickets//bogota_vertices.txt'
    total_vertex = 228046
    dir_edges = cf.data_dir + 'tickets//bogota_arcos.txt'
    total_edges = 228046
    #dir_fees = cf.data_dir + 'tickets//Comparendos_2019_Bogota_D_C.geojson'
    dir_fees = cf.data_dir + 'tickets//comparendos_2019_bogota_vertices.csv'
    total_fees = 402500
    #dir_stations = cf.data_dir + 'tickets//estacionpolicia.json'
    dir_stations = cf.data_dir + 'tickets//estacionpolicia_bogota_vertices.csv'
    total_stations = 21
    borders = {'minlat': model.math.inf, 'minlong': model.math.inf, 'maxlat': -1000000000, 'maxlong': -100000000}
    i= 0
    """
    """
    input_file_s = csv.DictReader(open(dir_stations, encoding='utf-8'), delimiter=',')
    for line in input_file_s:
        line = fix_format(line)
        model.stations_first(control['model'], line)
    
    with open(dir_vertex, 'r') as vertex_file:
        print('Cargando archivo de vértices...')
        for line in vertex_file:
            list = line.split(',')
            info = {
                'id': int(list[0]),
                'long': float(list[1]),
                'lat': float(list[2]),
                'station': None,
                'fees': model.lt.newList('ARRAY_LIST'),
                'closest_station': ''
            }
            borders['minlat'] = update_min(borders['minlat'], info, 'lat')
            borders['minlong'] = update_min(borders['minlong'], info, 'long')
            borders['maxlat'] = update_max(borders['maxlat'], info, 'lat')
            borders['maxlong'] = update_max(borders['maxlong'], info, 'long')
            model.load_data(control['model'], info)
            i+= 1
            #progress_bar(i, total_vertex)

    i=0
    input_file = csv.DictReader(open(dir_fees, encoding='utf-8'), delimiter=',')
    print('Cargando archivo de comparendos...')
    for line in input_file:
        info = line
        info = fix_format(info)
        model.add_fee(control['model'], info)
        i += 1
        #progress_bar(i, total_fees)

    print('Ordenando multas por gravedad...')
    model.merg.sort(control['model']['ordered_fees'], model.sort_fees)

    print('Cargando archivo de estaciones...')
    input_file_s = csv.DictReader(open(dir_stations, encoding='utf-8'), delimiter=',')
    for line in input_file_s:
        line = fix_format(line)
        model.add_station(control['model'], line)
    i = 0
    with open(dir_edges, 'r') as edges_file:
        print('Cargando archivo de arcos...')
        for line in edges_file:
            if '#' not in line:
                line = line.strip()
                list = line.split(' ')
                info = []
                for e in list:
                    info.append(int(e))
                model.load_edges(control['model'], info)
                i+= 1
                #progress_bar(i, total_edges)

    control['model']['borders'] = borders
    f_time = get_time()
    d_time = delta_time(i_time, f_time)
    print(colorama.Fore.GREEN + 'CARGA DE DATOS COMPLETADA' + '\n')
    print(colorama.Fore.RESET)
    return d_time
    
def progress_bar(progress, total):
    color = colorama.Fore.YELLOW
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    print(color + f'\r|{bar}| {percent:.2f}%', end='\r')
    if progress == total:
        print(colorama.Fore.GREEN + f'\r|{bar}| {percent:.2f}%', end='\r')
        print(colorama.Fore.RESET, '\n')

def fix_format(info):
    float_keys = ['LATITUD', 'LONGITUD', 'EPOLATITUD', 'EPOLONGITU']
    int_keys = ['ANO', 'OBJECTID', 'VERTICES']
    for key in info.keys():
        if info[key] in (None, '', ' '):
            if (key in float_keys) or (key in int_keys):
                info[key] = 0
            else:
                if key == 'INFRACCION':
                    info[key] = 'A00'
                else:
                    info[key] = 'Unknown'
        else:
            if (key not in float_keys) and (key not in int_keys):
                if key == 'INFRACCION':
                    if len(info[key]) < 3:
                        info[key] = info[key][0] + '00'
                info[key] = info[key].strip()
            else:
                if key in float_keys:
                    info[key] = float(info[key])
                elif key in int_keys:
                    info[key] = int(info[key])

    return info

def update_min(min, data, coord):
    if data[coord] < min:
        return data[coord]
    else:
        return min
    
def update_max(min, data, coord):
    if data[coord] > min:
        return data[coord]
    else:
        return min

def get_first_last_five(list):
    data = model.get_first_last_five(list)
    return data

def get_first_last_three(list):
    data = model.get_first_last_three(list)
    return data

# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, lat_origin, long_origin, lat_dest, long_dest, bono):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    itime = get_time()
    total_distancy, total_vertex, path = model.req_1(control['model'], lat_origin, long_origin, lat_dest, long_dest, bono)
    ftime = get_time()
    dtime = delta_time(itime, ftime)
    print(f'Tiempo de carga:{dtime:3f}')
    return total_distancy, total_vertex, path


def req_2(control, lat_origin, long_origin, lat_dest, long_dest, bono):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    itime = get_time()
    total_distancy, total_vertex, path = model.req_2(control['model'], lat_origin, long_origin, lat_dest, long_dest, bono)
    ftime = get_time()
    dtime = delta_time(itime, ftime)
    print(f'Tiempo de carga:{dtime:3f}')
    return total_distancy, total_vertex, path
    pass


def req_3(control, localidad, num_cam):
    """
    Retorna el resultado del requerimiento 3
    """
    sT = get_time()
    sub_n, dist  = model.req_3(control["model"], localidad, num_cam)
    fT = get_time()
    dT = delta_time(sT, fT)
    return sub_n, dist, dT


def req_4(control, camaras, bono):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    itime = get_time()
    vertices, arcos, total_weight = model.req_4(control['model'], camaras, bono)
    ftime = get_time()
    dtime = delta_time(itime, ftime)
    print(f'Tiempo de carga:{dtime:3f}')
    return vertices, arcos, total_weight


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control, comparendos, bono):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    itime = get_time()
    lst = model.req_6(control['model'], comparendos, bono)
    ftime = get_time()
    dtime = delta_time(itime, ftime)
    print(f'Tiempo de carga:{dtime:3f}')
    return lst


def req_7(control, lat_origin, long_origin, lat_dest, long_dest, bono):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    itime = get_time()
    total_distancy, total_vertex, path = model.req_7(control['model'], lat_origin, long_origin, lat_dest, long_dest, bono)
    ftime = get_time()
    dtime = delta_time(itime, ftime)
    print(f'Tiempo de carga:{dtime:3f}')
    return total_distancy, total_vertex, path



def req_8(control, lat_origin, long_origin, lat_dest, long_dest, bono):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
