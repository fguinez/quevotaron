from bs4 import BeautifulSoup
import requests
import os




url_base  = 'http://opendata.camara.cl/camaradiputados/WServices/'
url_base2 = 'http://opendata.camara.cl/wscamaradiputados.asmx/'




def get_xml(url):
    xml_str = requests.get(url = url).text
    if len(xml_str) < 500:                                  # Si no llega respuesta con contenido
            raise Exception(f"Respuesta incompleta. Intenta más tarde.\nURL: {url}")
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

def get_diputados_periodo(force_request=False):
    path = 'data/diputados_periodo.xml'
    url = url_base + 'WSDiputado.asmx/retornarDiputadosPeriodoActual'
    data = _get_data(path, url, force_request=force_request)
    return data

    
def get_diputados_vigentes(force_request=False):
    path = 'data/diputados_vigentes.xml'
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
    get_diputados_periodo()
    get_diputados_vigentes()