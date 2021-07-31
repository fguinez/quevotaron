from pprint import pprint
from diputados.votaciones_handler import get_votacion
from draw.draw import create_image
from draw.palette import partidos, coaliciones
import sys







# COPIADO DESDE DIPUTADOS
# TODO: Modificar en base a la subcarpeta 'constituyentes'

if __name__ == "__main__":
    votid = 36472#int(input("Ingresa un ID de votación: "))
    if len(sys.argv) > 1:
        votid = int(sys.argv[1])
    votacion = get_votacion(votid)
    print(votacion)
    print(votacion.a_favor_partido)
    print(votacion.en_contra_partido)
    print(votacion.abstencion_partido)
    print(votacion.ausentes_partido)

    titulo = "Tercer retiro del 10%"#input("Título de la ley: ")
    if len(sys.argv) > 2:
        titulo = sys.argv[2]
    opcionesH, opcionesV, pareos = votacion.info_partido
    im = create_image(titulo, grupos=partidos,
                      opcionesH=opcionesH, opcionesV=opcionesV, pareos=pareos)
    im.show()