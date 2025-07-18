import os
if os.getcwd()[-9:] == "diputados":
    from   models import Votacion
    from   handler import get_diputados
    import api
else:
    from   diputados.models import Votacion
    from   diputados.handler import get_diputados
    import diputados.api as api


# Recibe una fecha con el nombr completo del mes en español y lo reemplaza por
# el número del mes
def _replace_month(date):
    months = {'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04', 'mayo': '05',
              'junio': '06', 'julio': '07', 'agosto': '08', 'septiembre': '09',
              'octubre': '10', 'noviembre': '11', 'diciembre': '12'}
    date = date.split()
    date[1] = months[date[1].lower()]
    return " ".join(date)

def _get_data(votacion_info, dataname):
    dataclass = votacion_info.find_all(class_="dato")
    datatitles = list(filter(lambda d: dataname in d.text.lower(), dataclass))
    if len(datatitles):
        datatitle = datatitles[0]
        return datatitle.find_next('strong').text.strip()
    return ""               # En caso de que no existan datos con el texto dataname

# Obtiene el título de una votación por medio de su HTML
def get_titulo(votacion_info):
    titulo = _get_data(votacion_info, "materia")
    return titulo

# Obtiene el subtítulo de una votación por medio de su HTML
def get_subtitulo(votacion_info):
    subtitulo = _get_data(votacion_info, "artículo")
    return subtitulo

# Obtiene el id de proyecto de ley asociado a una votación por medio de su HTML
def get_proyecto(votacion_info):
    proyecto = _get_data(votacion_info, "proyecto ley")
    return proyecto

# Obtiene la fecha de una votación por medio de su HTML
def get_fecha(votacion_info):
    fecha = _get_data(votacion_info, "fecha")
    return _replace_month(fecha)

# Obtiene la sesión en que se realizó una votación por medio de su HTML
def get_sesion(votacion_info):
    texto = _get_data(votacion_info, "sesión")
    return texto

# Obtiene el trámite en que se encuentra el proyecto relacionado a una votación por medio de su HTML
def get_tramite(votacion_info):
    texto = _get_data(votacion_info, "trámite")
    return texto

# Obtiene el tipo de una votación por medio de su HTML
def get_tipo(votacion_info):
    resultado = _get_data(votacion_info, "tipo de votación")
    return resultado

# Obtiene el quorum de la votación por medio de su HTML
def get_quorum(votacion_info):
    quorum = _get_data(votacion_info, "quorum")
    return quorum

# Obtiene el resultado de la votación por medio de su HTML
def get_resultado(votacion_info):
    resultado = _get_data(votacion_info, "resultado")
    return resultado

# Obtiene la cantidad de votos a favor de la votación por medio de su HTML
def get_a_favor(votacion_info):
    a_favor = votacion_info.find("td").text
    return int(a_favor)

# Obtiene la cantidad de abstenciones de la votación por medio de su HTML
def get_abstencion(votacion_info):
    a_favor    = votacion_info.find("td")
    en_contra  = votacion_info.find("td").find_next("td")
    abstencion = en_contra.find_next("td").text
    return int(abstencion)

# Obtiene la cantidad de votos en contra de la votación por medio de su HTML
def get_en_contra(votacion_info):
    a_favor   = votacion_info.find("td")
    en_contra = a_favor.find_next("td").text
    return int(en_contra)

# Obtiene el objeto votación asociado al id entregado
def get_votacion(id_, path=f'tmp/html'):
    diputados = get_diputados()
    votacion_info = api.get_votacion(id_, path)
    titulo     = get_titulo(votacion_info)
    subtitulo  = get_subtitulo(votacion_info)
    proyecto   = get_proyecto(votacion_info)
    fecha      = get_fecha(votacion_info)
    sesion     = get_sesion(votacion_info)
    tramite    = get_tramite(votacion_info)
    tipo       = get_tipo(votacion_info)
    resultado  = get_resultado(votacion_info)
    quorum     = get_quorum(votacion_info)
    a_favor    = get_a_favor(votacion_info)
    abstencion = get_abstencion(votacion_info)
    en_contra  = get_en_contra(votacion_info)
    votos      = votacion_info.find_all('h3')
    return Votacion(
        id_, titulo, subtitulo, proyecto, fecha, sesion, tramite, tipo,
        resultado, quorum, a_favor, abstencion, en_contra, diputados, votos
    )




if __name__ == "__main__":
    v = get_votacion(36931)
    print(v.info_por_coalicion)