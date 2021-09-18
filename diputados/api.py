from bs4 import BeautifulSoup
import requests
import os




url_base  = 'http://opendata.camara.cl/camaradiputados/WServices/'
url_base2 = 'http://opendata.camara.cl/wscamaradiputados.asmx/'




def get_html(url):
    html_str = requests.get(url = url).text
    if len(html_str) < 500:                                  # Si no llega respuesta con contenido
            raise Exception(f"Respuesta incompleta. Intenta más tarde.\nURL: {url}")
    return html_str

# Obtiene el html disponible en URL
def _get_data(path, url, force_request=False, parser='html.parser'):
    if os.path.isfile(path) and not force_request:          # Si los datos están guardados en local
        with open(path, 'r') as file:
            html = file.read()
    else:                                                   # Si los datos no están guardados en local
        html = get_html(url)
        with open(path, 'w') as file:
            file.write(html)
    data = BeautifulSoup(html, parser)
    return data

# Obtiene la información de un diputado
# URL utilizada: https://www.camara.cl/diputados/detalle/votaciones_sala.aspx?prmId={}
def get_diputado(dipid, force_request=False):
    path = f'diputados/data/diputados/{dipid}.html'
    url = f'https://www.camara.cl/diputados/detalle/votaciones_sala.aspx?prmId={dipid}'
    data = _get_data(path, url, force_request=force_request)
    return data

def get_diputados_periodo(force_request=False):
    path = 'diputados/data/diputados_periodo.xml'
    url = url_base + 'WSDiputado.asmx/retornarDiputadosPeriodoActual'
    data = _get_data(path, url, force_request=force_request, parser='xml')
    return data

def get_diputados_vigentes(force_request=False):
    path = 'diputados/data/diputados_vigentes.xml'
    url = 'http://opendata.camara.cl/wscamaradiputados.asmx/getDiputados_Vigentes'
    data = _get_data(path, url, force_request=force_request, parser='xml')
    return data

def get_diputados():
    path = 'diputados/data/diputados.xml'
    url = url_base + 'WSDiputado.asmx/retornarDiputados'
    data = _get_data(path, url)
    return data

def get_proyecto(prmNumeroBoletin):
    path = f'diputados/data/proyectos/{prmNumeroBoletin}.xml'
    url = url_base + f'WSLegislativo.asmx/retornarVotacionesXProyectoLey?prmNumeroBoletin={prmNumeroBoletin}'
    data = _get_data(path, url)
    return data

# Obtiene los resultados de una votación
# URL utilizada: https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion={}
def get_votacion(prmVotacionID):
    path = f'diputados/data/votaciones/{prmVotacionID}.html'
    url = f'https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion={prmVotacionID}'
    data = _get_data(path, url)
    return data




if __name__ == "__main__":
    get_votacion(36931)