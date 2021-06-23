from collections import namedtuple
import time
import os

from models import Diputado
import api_handler as api




Militancia = namedtuple('Militancia', ['partido','coalicion','nombre']) 




def get_coaliciones():
    path = "data/coaliciones.csv"
    with open(path, 'r') as file:
        lines = file.readlines()
        lines = (line.strip().split(',') for line in lines)
        coaliciones = {line[0]: line[1] for line in lines}
    return coaliciones

def get_militancia(militancias):
    most_recent = time.gmtime(0)
    ultima_militancia = "IND"
    for militancia in militancias.findAll('Militancia'):
        fecha_inicio = militancia.FechaInicio.string
        fecha_inicio = time.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
        if fecha_inicio > most_recent:
            most_recent = fecha_inicio
            if militancia.Partido:
                ultima_militancia = militancia.Partido.Id.string
            else:
                ultima_militancia = "IND"
    return ultima_militancia

def get_militancias():
    path = "data/militancias.csv"
    if os.path.isfile(path):
        with open(path, 'r') as file:
            file.readline()                                          # Ignorar encabezado
            lines = file.readlines()
            lines = (line.strip().split(',') for line in lines)
            # {id: [partido, coalición, nombre]}
            militancias = {int(line[0]): Militancia(line[1], line[2], line[3]) for line in lines}
        return militancias
    diputados_periodo = api.get_diputados_periodo()
    diputados_vigentes = api.get_diputados_vigentes()
    militancias = {}
    coaliciones = get_coaliciones()
    with open(path, 'w') as file:
        file.write("id,partido,coalicion,nombre\n")
        for diputado in diputados_periodo.findAll('Diputado'):
            ids_vigentes = [int(d.DIPID.string) for d in diputados_vigentes.findAll('Diputado')]
            id = int(diputado.Id.string)
            if not id in ids_vigentes:
                continue
            nombre = f"{diputado.Nombre.string} {diputado.ApellidoPaterno.string} {diputado.ApellidoMaterno.string}"
            militancia = get_militancia(diputado.Militancias)
            file.write(f"{id},{militancia},{coaliciones[militancia]},{nombre}\n")
            militancias[id] = Militancia(militancia, coaliciones[militancia], nombre)
    return militancias

def create_diputado(diputado, militancia):
    '''
    <class 'bs4.element.Tag'> diputado
    '''
    id        = int(diputado.DIPID.string)
    nombre    = f"{diputado.Nombre.string} {diputado.Apellido_Paterno.string} {diputado.Apellido_Materno.string}"
    partido   = militancia.partido
    coalicion = militancia.coalicion
    return Diputado(id, nombre, partido, coalicion)

def get_diputados():
    diputados_vigentes = api.get_diputados_vigentes()
    militancias = get_militancias()
    diputados = {}
    for diputado in diputados_vigentes.findAll('Diputado'):
        id = int(diputado.DIPID.string)
        diputados[id] = create_diputado(diputado, militancias[id])
    return diputados