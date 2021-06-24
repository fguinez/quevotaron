from pprint import pprint
from votaciones_handler import get_votacion
from draw.draw import create_image









if __name__ == "__main__":
    votid = 36472#int(input("Ingresa un ID de votación: "))
    votacion = get_votacion(votid)
    print(votacion)
    print(votacion.a_favor_partido)
    print(votacion.en_contra_partido)
    print(votacion.abstencion_partido)
    print(votacion.ausentes_partido)

    titulo = "Tercer retiro del 10%"#input("Título de la ley: ")
    create_image(votacion, titulo, group='coalicion')
    '''
    get_diputados()
    prmVotacionID = 36336
    diputados_periodo  = api.get_diputados_periodo()
    diputados_vigentes = api.get_diputados_vigentes()


    diputados           = api.get_diputados()
    
    ids  = set(int(diputado.Id.string) for diputado in diputados_periodo.findAll('Diputado'))
    ids2 = set(int(diputado.DIPID.string) for diputado in diputados_vigentes.findAll('Diputado'))
    
    print(len(ids))
    print(len(ids2))

    diff = ids-ids2
    print(diff)
    print(len(diff))

    print(len(diputados.findAll('Diputado')))
    '''