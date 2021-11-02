from   collections import namedtuple
import time
import os
import sys

if os.getcwd()[-9:] == "diputados":
    from   models import Diputado
    import api

    path_base = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1])
else:
    from   diputados.models import Diputado
    import diputados.api as api

    path_base = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1]) + '/diputados'


    

Militancia = namedtuple('Militancia', ['partido','coalicion','nombre']) 




def get_coaliciones():
    path = f"{path_base}/data/coaliciones.csv"
    with open(path, 'r') as file:
        lines = file.readlines()
        lines = (line.strip().split(',') for line in lines)
        coaliciones = {line[0]: line[1] for line in lines}
    return coaliciones

def get_militancia(militancias):
    most_recent = time.gmtime(0)
    ultima_militancia = "IND"
    for militancia in militancias.find_all('Militancia'):
        fecha_inicio = militancia.FechaInicio.string
        fecha_inicio = time.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
        if fecha_inicio > most_recent:
            most_recent = fecha_inicio
            if militancia.Partido:
                ultima_militancia = militancia.Partido.Id.string
            else:
                ultima_militancia = "IND"
    return ultima_militancia

def get_militancias(filename="integrantes.csv"):
    path = f"{path_base}/data/{filename}"
    if os.path.isfile(path):                            # En caso de que el archivo ya exista, se lee
        with open(path, 'r') as file:
            file.readline()                                          # Ignorar encabezado
            lines = file.readlines()
            lines = (line.strip().split(',') for line in lines)
            # {id: [partido, coalición, nombre]}
            militancias = {int(line[0]): Militancia(line[1], line[2], line[3]) for line in lines}
        return militancias
    # En caso de que el archivo no exista, se escribe
    militancias = {}
    diputados_vigentes = api.get_diputados_vigentes()
    ids_vigentes = [int(d.DIPID.string) for d in diputados_vigentes.find_all('Diputado')]
    with open(path, 'w') as file:
        file.write("id,partido,coalicion,nombre\n")
        for dipid in ids_vigentes:
            diputado = get_diputado(dipid)
            file.write(f"{dipid},{diputado.partido},{diputado.coalicion},{diputado.nombre}\n")
            militancias[dipid] = Militancia(diputado.partido, diputado.coalicion, diputado.nombre)
    return militancias

# Recibe el nombre de un partido y retorna su abreviación
def partido2abreviacion(nombre):
    path = f"{path_base}/data/partidos.csv"
    with open(path, 'r') as file:
        lines = file.readlines()
        lines = (line.strip().split(',') for line in lines)
        abreviaciones = {line[0].lower(): line[1] for line in lines}
    return abreviaciones[nombre.lower()]

# Recibe el nombre de una bancada y retorna la abreviación de la coalición respectiva
def bancada2abreviacion(nombre):
    path = f"{path_base}/data/bancadas.csv"
    with open(path, 'r') as file:
        lines = file.readlines()
        lines = (line.strip().split(',') for line in lines)
        abreviaciones = {line[0].lower(): line[1] for line in lines}
    return abreviaciones[nombre.lower()]

# Obtiene la abreviación del partido correspondiente al diputado ingresado
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
    partido = partido2abreviacion(partido)
    return partido

# Obtiene la abreviación de la coalición correspondiente al diputado ingresado
def _get_coalicion(diputado, partido=""):
    regla = lambda p: "bancada:" in p.text.lower()
    info = list(filter(regla, diputado.find_all("p")))[0]
    regla = lambda text: "bancada" in text.lower()
    coalicion = list(filter(regla, info.text.split("\n")))[0]
    coalicion = coalicion.strip().split(": ")[-1]
    coalicion = coalicion.replace(',', '')
    coalicion = bancada2abreviacion(coalicion)
    # Excepciones
    if partido == "FRVS":
        coalicion = "AD"
    return coalicion

# Obtiene la información de un diputado en particular (en ocasiones, logra más detalle que get_diputados)
def get_diputado(dipid):
    diputado = api.get_diputado(dipid)
    h2 = diputado.find("h2").text                 # Se encuentra el título
    nombre = " ".join(h2.split(" ")[1:])          # Se elimina 'Diputadx' del título, dejando solo el nombre
    partido = _get_partido(diputado)
    coalicion = _get_coalicion(diputado, partido)
    return Diputado(dipid, nombre, partido, coalicion)

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
    for diputado in diputados_vigentes.find_all('Diputado'):
        id = int(diputado.DIPID.string)
        diputados[id] = create_diputado(diputado, militancias[id])
    return diputados




if __name__ == "__main__":
    # Zona de pruebas
    #print(get_diputado(945))
        
    get_militancias("integrantes.csv")
