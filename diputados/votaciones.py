from   diputados.models import Votacion
from   diputados.handler import get_diputados
import diputados.api as api




def get_votacion(id):
    diputados = get_diputados()
    votacion_info = api.get_votacion(id)
    fecha      = votacion_info.Fecha.string
    tipo       = votacion_info.Tipo.string.capitalize()
    resultado  = votacion_info.Resultado.string.capitalize()
    quorum     = votacion_info.Quorum.string.capitalize()
    a_favor    = int(votacion_info.TotalAfirmativos.string)
    abstencion = int(votacion_info.TotalAbstenciones.string)
    en_contra  = int(votacion_info.TotalNegativos.string)
    votos  = votacion_info.findAll('Voto')
    pareos = votacion_info.findAll('Pareo')
    return Votacion(id, fecha, tipo, resultado, quorum, a_favor, abstencion, en_contra, diputados, votos, pareos) 