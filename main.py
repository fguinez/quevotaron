from pprint import pprint
import xmltojson
import json

import api_handler as api


def create_diputado(diputado, militancias):
    '''
    <class 'bs4.element.Tag'> diputado
    '''
    return Diputado(id, nombre, apellido_paterno, apellido_materno, partido, coalicion)

def get_diputados():
    diputados_vigentes = api.get_diputados_vigentes()
    diputados_periodo = api.get_diputados_periodo()
    for diputado in diputados_vigentes.findAll('Diputado'):
        same_id = lambda d: d.Id.string == diputado.DIPID.string
        d = filter(same_id, diputados_periodo.findAll('Diputado'))
        militancias = list(d)[0].Militancias
        create_diputado(diputado, militancias)
        

        #
        break





if __name__ == "__main__":
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