from pprint import pprint
from bs4 import BeautifulSoup
import requests
import xmltojson
import json
import os





url_base = 'http://opendata.camara.cl/camaradiputados/WServices/'
url_base2 = 'http://opendata.camara.cl/wscamaradiputados.asmx/'




def get_xml(url):
    xml_str = requests.get(url = url).text
    return xml_str

def _get_data(path, url, force_request=False):
    if os.path.isfile(path) and not force_request:          # Si los datos están guardados en local
        with open(path, 'r') as file:
            xml = file.read()
    else:                                                   # Si los datos no están guardados en local
        xml = get_xml(url)
        with open(path, 'w') as file:
            file.write(xml)
    data = BeautifulSoup(xml, 'xml')
    return data

def get_diputados_vigentes(force_request=False):
    path = 'data/diputados_vigentes.xml'
    url = url_base + 'WSDiputado.asmx/retornarDiputadosPeriodoActual'
    data = _get_data(path, url, force_request=force_request)
    return data

    
def get_diputados_vigentes2(force_request=False):
    path = 'data/diputados_vigentes2.xml'
    url = 'http://opendata.camara.cl/wscamaradiputados.asmx/getDiputados_Vigentes'
    data = _get_data(path, url, force_request=force_request)
    return data


def get_diputados():
    path = 'data/diputados.xml'
    url = url_base + 'WSDiputado.asmx/retornarDiputados'
    data = _get_data(path, url)
    return data

def get_proyecto(prmNumeroBoletin):
    path = f'data/proyectos/{prmNumeroBoletin}.xml'
    url = url_base + f'WSLegislativo.asmx/retornarVotacionesXProyectoLey?prmNumeroBoletin={prmNumeroBoletin}'
    data = _get_data(path, url)
    return data

def get_votacion(prmVotacionID):
    path = f'data/votaciones/{prmVotacionID}.xml'
    url = url_base2 + f'getVotacion_Detalle?prmVotacionID={prmVotacionID}'
    data = _get_data(path, url)
    return data

if __name__ == "__main__":
    
    prmVotacionID = 36336
    diputados_vigentes  = get_diputados_vigentes()
    diputados_vigentes2 = get_diputados_vigentes2()

    diputados           = get_diputados()
    
    ids  = set(int(diputado.Id.string)    for diputado in diputados_vigentes.findAll('Diputado'))
    ids2 = set(int(diputado.DIPID.string) for diputado in diputados_vigentes2.findAll('Diputado'))

    print(len(ids))
    print(len(ids2))

    diff = ids-ids2
    print(diff)
    print(len(diff))

    print(len(diputados.findAll('Diputado')))