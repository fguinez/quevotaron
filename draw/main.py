import json
import sys
import os

if os.getcwd()[-4:] == "draw":
    from maker import create_image
    from palette import partidos, coaliciones

    # Path hacia la carpeta draw
    path_draw = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1])
    # Path hacia la carpeta root
    path_root = '/'.join(path_draw.split('/')[:-1])
else:
    from draw.maker import create_image
    from draw.palette import partidos, coaliciones

    # Path hacia la carpeta draw
    path_draw = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1]) + "/draw"
    # Path hacia la carpeta root
    path_root = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1])




def generar_visualizaciones(votid, votacion_info, titulo=None, path='tmp/visualizaciones'):
    subtitulo              = votacion_info["subtitulo"]
    tipo                   = votacion_info["tipo"]
    resultado              = votacion_info["resultado"]
    quorum                 = votacion_info["quorum"]
    nquorum                = votacion_info["nquorum"]
    votacion_por_partido   = votacion_info["info_por_partido"]
    votacion_por_coalicion = votacion_info["info_por_coalicion"]

    # Si no fue ingresado como argumento, rescatamos el título de votacion_info
    if titulo == None:
        titulo = votacion_info["titulo"]

    path_partidos    = f'{path}/{votid}_partidos.png'
    path_coaliciones = f'{path}/{votid}_coaliciones.png'

    # Creamos la visualización por partidos
    opcionesH, opcionesV, pareos = votacion_por_partido
    im = create_image(titulo, subtitulo, tipo, resultado=resultado,
                      quorum=quorum, nquorum=nquorum, grupos=partidos,
                      opcionesH=opcionesH, opcionesV=opcionesV, pareos=pareos)
    im.save(path_partidos)

    # Creamos la visualización por coalicion
    opcionesH, opcionesV, pareos = votacion_por_coalicion
    im = create_image(titulo, subtitulo, tipo, resultado=resultado,
                      quorum=quorum, nquorum=nquorum, grupos=coaliciones,
                      opcionesH=opcionesH, opcionesV=opcionesV, pareos=pareos)
    im.save(path_coaliciones)

    return [path_coaliciones, path_partidos]




if __name__ == "__main__":
    # Recuperamor el path al objeto con la información de la votación
    path_votacion = sys.argv[1]
    # Extraemos el id de la votación del nombre de archivo
    votid = path_votacion.split('/')[-1].split('.')[0]

    # Cargamos el objeto Votación
    with open(path_votacion, 'r') as file:
        votacion_info = json.load(file)
    if len(sys.argv) > 2:
        titulo = sys.argv[2]
        generar_visualizaciones(votid, votacion_info, titulo=titulo)
    generar_visualizaciones(votid, votacion_info)
