# TODO: Fusionar los módulos api, handler y votaciones. Sus funciones realmente responden
# a las mismas funcionalidades y generan un message chain.

from bs4 import BeautifulSoup
import requests
import sys
import os




# Situa todos los path en la carpeta diputados
if os.getcwd()[-9:] == "diputados":
    path_base = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1])
else:
    path_base = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1]) + '/diputados'

url_base  = 'http://opendata.camara.cl/camaradiputados/WServices/'
url_base2 = 'http://opendata.camara.cl/wscamaradiputados.asmx/'




def get_html(url):
    html_str = requests.get(url = url).text
    if len(html_str) < 500:                                  # Si no llega respuesta con contenido
            raise Exception(f"Respuesta incompleta. Intenta más tarde.\nURL: {url}")
    return html_str

# Obtiene el html disponible en URL
def _get_data(path, url, force_request=False, save_html=True, parser='html.parser'):
    if os.path.isfile(path) and not force_request and save_html:  # Si los datos están guardados en local
        with open(path, 'r') as file:
            html = file.read()
    else:                                                         # Si los datos no están guardados en local
        html = get_html(url)
        if save_html:
            with open(path, 'w') as file:
                file.write(html)
    data = BeautifulSoup(html, parser)
    return data

def _get_tipos_votaciones_recientes(data):
    divs = [d.find_next("div", {"class": "inferiores"}).div for d in data]
    tipos = []
    for div in divs:
        if div['class'][0] == 'izq':
            div = div.div.text.split(' ')[1].lower()
            if div == "unica":
                div = "única"
            tipos.append(div)
        else:
            tipos.append(None)
    return tipos

# Obtiene un listado con los ids, de las últimas 20 votaciones realizadas
# URL utilizada: https://www.camara.cl/legislacion/sala_sesiones/votaciones.aspx
def get_votaciones_recientes(con_votids=True, con_tipos=True):
    url = 'https://www.camara.cl/legislacion/sala_sesiones/votaciones.aspx'
    data = _get_data("", url, save_html=False)
    data = data.find_all("div", {"class": "datos_votacion"})
    to_return = []
    if con_votids:
        hrefs = [d.find_next("a")["href"] for d in data]
        votids = [int(href.split('=')[-1]) for href in hrefs]
        to_return.append(votids)
    if con_tipos:
        tipos = _get_tipos_votaciones_recientes(data)
        to_return.append(tipos)
    return to_return
    

# Obtiene la información de un diputado
# URL utilizada: https://www.camara.cl/diputados/detalle/votaciones_sala.aspx?prmId={}
def get_diputado(dipid, force_request=False):
    path = f'{path_base}/data/diputados/{dipid}.html'
    url = f'https://www.camara.cl/diputados/detalle/votaciones_sala.aspx?prmId={dipid}'
    data = _get_data(path, url, force_request=force_request)
    return data

# Obtiene la información de los diputados del periodo actual (no necesariamente vigentes),
# se incluyen quienes fueron electos pero ya no están ejerciendo y quienes asumieron en su
# reemplazo.
# URL utilizada: http://opendata.camara.cl/camaradiputados/WServices/WSDiputado.asmx/retornarDiputadosPeriodoActual
def get_diputados_periodo(force_request=False):
    path = f'{path_base}/data/diputados_periodo.xml'
    url = url_base + 'WSDiputado.asmx/retornarDiputadosPeriodoActual'
    data = _get_data(path, url, force_request=force_request, parser='xml')
    return data

# Obtiene la información de los diputados actualmente en ejercicio
# URL utilizada: http://opendata.camara.cl/wscamaradiputados.asmx/getDiputados_Vigentes
def get_diputados_vigentes(force_request=False):
    path = f'{path_base}/data/diputados_vigentes.xml'
    url = 'http://opendata.camara.cl/wscamaradiputados.asmx/getDiputados_Vigentes'
    data = _get_data(path, url, force_request=force_request, parser='xml')
    return data

# Obtiene la información histórica de todos los diputados que alguna vez ejercieron
# URL utilizada: http://opendata.camara.cl/camaradiputados/WServices/WSDiputado.asmx/retornarDiputados
def get_diputados():
    path = f'{path_base}/data/diputados.xml'
    url = url_base + 'WSDiputado.asmx/retornarDiputados'
    data = _get_data(path, url)
    return data

def get_proyecto(prmNumeroBoletin):
    path = f'{path_base}/data/proyectos/{prmNumeroBoletin}.xml'
    url = url_base + f'WSLegislativo.asmx/retornarVotacionesXProyectoLey?prmNumeroBoletin={prmNumeroBoletin}'
    data = _get_data(path, url)
    return data

# Obtiene los resultados de una votación
# URL utilizada: https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion={}
def get_votacion(prmVotacionID, path=f'tmp/html'):
    path = f'{path}/{prmVotacionID}.html'
    url = f'https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion={prmVotacionID}'
    data = _get_data(path, url)
    return data




if __name__ == "__main__":
    votids = get_votaciones_recientes()
    print(len(votids))
    print(votids)