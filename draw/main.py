from draw import create_image
from palette import partidos, coaliciones
import json
import sys
import os




# Path hacia la carpeta draw
path_draw = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1])
# Path hacia la carpeta root
path_root = '/'.join(path_draw.split('/')[:-1])




if __name__ == "__main__":
    # Recuperamor el path al objeto con la información de la votación
    path_votacion = sys.argv[1]
    # Extraemos el id de la votación del nombre de archivo
    votid = path_votacion.split('/')[-1].split('.')[0]

    # Cargamos el objeto Votación
    with open(path_votacion, 'r') as file:
        votacion_info = json.load(file)
    resultado              = votacion_info["resultado"]
    quorum                 = votacion_info["quorum"]
    nquorum                = votacion_info["nquorum"]
    votacion_por_partido   = votacion_info["info_por_partido"]
    votacion_por_coalicion = votacion_info["info_por_coalicion"]

    titulo = votacion_info["titulo"]
    # Si fue ingresado como argumento, rescatamos el título de la visualización
    if len(sys.argv) > 2:
        titulo = sys.argv[2]

    # Creamos la visualización por partidos
    opcionesH, opcionesV, pareos = votacion_por_partido
    im = create_image(titulo, resultado=resultado, quorum=quorum,
                      nquorum=nquorum, grupos=partidos,
                      opcionesH=opcionesH, opcionesV=opcionesV, pareos=pareos)
    im.save(f'{path_root}/visualizaciones/{votid}_partidos.png')

    # Creamos la visualización por coalicion
    opcionesH, opcionesV, pareos = votacion_por_coalicion
    im = create_image(titulo, resultado=resultado, quorum=quorum,
                      nquorum=nquorum, grupos=coaliciones,
                      opcionesH=opcionesH, opcionesV=opcionesV, pareos=pareos)
    im.save(f'{path_root}/visualizaciones/{votid}_coaliciones.png')