from   collections import namedtuple
import time
import os
import sys

from   models import Diputado
import api




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

def nombre2abreviacion(nombre):
    path = "data/abreviaciones.csv"
    with open(path, 'r') as file:
        lines = file.readlines()
        lines = (line.strip().split(',') for line in lines)
        abreviaciones = {line[0].lower(): line[1] for line in lines}
    return abreviaciones[nombre.lower()]

def _get_partido(diputado):
    regla = lambda p: "partido:" in p.text.lower()
    info = list(filter(regla, diputado.find_all("p")))[0]
    regla = lambda text: "partido" in text.lower()
    partido = list(filter(regla, info.text.split("\n")))[0]
    partido = partido.strip().split(": ")[-1]
    partido = partido.split(" ")
    if partido[0].lower() == "partido":
        partido = partido[1:]
    partido = " ".join(partido)
    partido = nombre2abreviacion(partido)
    return partido

def get_diputado(dipip):
    diputado = api.get_diputado(dipip)
    h2 = diputado.find("h2").text                 # Se encuentra el título
    nombre = " ".join(h2.split(" ")[1:])          # Se elimina 'Diputadx' del título, dejando solo el nombre
    partido = _get_partido(diputado)
    #coalicion = 
    return Diputado(dipip, nombre, partido, coalicion)


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




if __name__ == "__main__":
    # Se ajusta el directorio a la carpeta diputados
    path = sys.argv[0].split('/')
    if len(path) > 1:
        path = f"{os.getcwd()}/{path[0]}"
        os.chdir(path)

    # Zona de pruebas
    #print(get_diputado(945))
        
    print(os.getcwd())
    print(nombre2abreviacion("Revolución Remocrática"))
