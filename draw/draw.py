'''
Propósito del módulo: Abstraer la generación de gráficas a diferentes contextos
'''

# https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
from palette import color_partido, color_coalicion, random_color
from PIL import Image, ImageDraw, ImageFont
from math import ceil
import sys
import os




# Situa todos los path en la carpeta draw
path_base = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1])

# Se definen las tipografías a utilizar
title    = ImageFont.truetype(f'{path_base}/fonts/IBM-Plex-Sans/IBMPlexSans-Bold.ttf',   80)
subtitle = ImageFont.truetype(f'{path_base}/fonts/IBM-Plex-Sans/IBMPlexSans-Medium.ttf', 40)
normal   = ImageFont.truetype(f'{path_base}/fonts/IBM-Plex-Sans/IBMPlexSans-Medium.ttf', 20)

R = 20
r = 0.7 * R




def sort_group(group):
    group = list(group)
    if 'SC' in list(group):
        group.remove('SC')
        group.append('SC')
    if 'IND' in list(group):
        group.remove('IND')
        group.append('IND')
    return group

def draw_points(draw, iniX, iniY, votos, cols, grupos):
    '''
    TODO: Completar documentación.
    [draw]

    [iniX]   (int) Posición de inicio en el eje X

    [iniY]   (int) Posición de inicio en el eje Y

    [votos]  (dict) Estructura que contiene los votos a agregar de la forma:
                        {<grupo1>: n, <grupo2>: n, ..., <grupoN>: n}

    [cols]   (int) Cantidad de columnas deseadas

    [grupos] (dict) Estructura que contiene información relacionada a los
             grupos (en esta función solo se utilizará el color de cada uno),
             sigue la forma:
                        {
                            <sigla1>: [<nombre1>, <color1>],
                            ...,
                            <siglaN>: [<nombreN>, <colorN>]
                        }
    '''
    iniX = iniX + R
    iniY = iniY + R
    d = 0
    for group in sort_group(votos.keys()):
        color = grupos[group][1]
        for _ in range(votos[group]):
            i = d %  cols
            j = d // cols
            x = iniX + i*R*2
            y = iniY + j*R*2
            draw.ellipse((x-r, y-r, x+r, y+r), fill=color)
            d += 1
    endX = iniX + cols*R*2 - R
    endY = iniY +    j*R*2 + R
    return endX, endY

def draw_pareos(draw, iniX, iniY, pareos, cols, grupos):
    '''
    TODO: Completar documentación.
    [draw]

    [iniX]   (int) Posición de inicio en el eje X

    [iniY]   (int) Posición de inicio en el eje Y

    [pareos] (dict) Estructura que contiene los grupos de los pareos a agregar
             de la forma:
                        [(<grupo1>, <grupo2>), (<grupo3>, <grupo4>), ...]

    [cols]   (int) Cantidad de columnas deseadas

    [grupos] (dict) Estructura que contiene información relacionada a los
             grupos (en esta función solo se utilizará el color de cada uno),
             sigue la forma:
                        {
                            <sigla1>: [<nombre1>, <color1>],
                            ...,
                            <siglaN>: [<nombreN>, <colorN>]
                        }
    '''
    R = 20
    r = 0.7 * R
    iniX = iniX + R
    iniY = iniY + R
    d = 0
    for grupo1, grupo2 in pareos:
        i = d %  cols
        j = d // cols
        x = iniX + i*R*2
        y = iniY + j*R*2
        draw.line([(x,y), (x+2*R, y)], fill='#000000', width=5)
        draw.ellipse((x-r,     y-r, x+r,     y+r), fill=grupos[grupo1][1])
        draw.ellipse((x-r+2*R, y-r, x+r+2*R, y+r), fill=grupos[grupo2][1])
        d += 2
    endX = iniX + cols*R*2 - R
    endY = iniY +    j*R*2 + R
    return endX, endY

def draw_legend(draw, lenX, iniY, grupos):
    '''
    [draw]
    
    [lenX]   (int) Ancho del cuadro de leyenda

    [iniY]   (int) Posición de partida del cuadro de leyenda

    [grupos] (dict) Estructura que contiene información relacionada a los
             grupos (en esta función solo se utilizará el color de cada uno),
             sigue la forma:
                    {
                        <sigla1>: [<nombre1>, <color1>],
                        ...,
                        <siglaN>: [<nombreN>, <colorN>]
                    }
    '''
    global_iniX = (1080 - lenX) / 2
    global_endX = 1080 - global_iniX
    global_iniY = iniY
    iniX = global_iniX
    for grupo in grupos.values():
        endX = iniX + 40 + draw.textsize(grupo[0], font=normal)[0] + 20
        if endX > global_endX:
            iniY += 40
        x = iniX + R
        y = iniY + R
        draw.ellipse((x-r, y-r, x+r, y+r), fill=grupo[1])
        draw.text((iniX+40,iniY), grupo[0], font=normal, fill='#333344')
    global_endY = iniY + 40
    # TODO: Dibujar marco con variables global_

def sum_votes(conjuntos):
    '''
    [conjuntos] (tup) Tupla que contiene elementos con la misma estructura entregada
                en los argumentos "opcionesH", "opcionesV" o "pareos" de la función 
                create_image.

                sum_votes retorna el total de votos sumando todos los elementos en
                el parámetro "conjuntos".
    '''
    votes = 0
    for conjunto in conjuntos:
        if isinstance(conjunto, dict):
            for option in conjunto:
                votes += sum(conjunto[option].values())
        elif isinstance(conjunto, list):
            votes += len(conjunto) * 2
    return votes


def create_image(titulo='', subtitulo='', resultado='', quorum='', nquorum=-1, grupos={},
                 opcionesH={}, opcionesV={}, pareos=[]):
    '''
    ----------
    PARÁMETROS
    ----------

    [titulo]    (str) Texto de encabezado

    [subtitulo] (str) Subtítulo bajo el encabezado

    [resultado] (str) Resultado de la votación, normalmente Aprobado o Rechazado

    [quorum]    (str) Nombre del quorum

    [nquorum]   (int) Cantidad de votos necesario para aprobar. Si su valor es -1
                se omite la información referida al quorum en la imagenc creada.


    [grupos]    Estructura que caracterisa a los grupos presentes en opcionesH
                y opcionesV. Normalmente estos grupos serán partidos, bancadas
                o coaliciones. Su forma será:
                {
                    <sigla1>: [<nombre1>, <color1>],
                    ...,
                    <siglaN>: [<nombreN>, <colorN>]
                }

                Un ejemplo sería:
                {
                    "PD": ["Partido Demócrata", "#f58231"],
                    "PR": ["Partido Republicano", "#911eb4"]
                }


    [opcionesH] Una estructura de la forma:
                {
                    <opcion1>: {<grupo1>: n, <grupo2>: n, ..., <grupoN>: n},
                    <opcion2>: {<grupo1>: n, <grupo2>: n, ..., <grupoN>: n},
                    ...,
                    <opcionN>: {<grupo1>: n, <grupo2>: n, ..., <grupoN>: n}
                }

                Ejemplo:
                {
                    "Apruebo":   {"PD": 13, "PR": 7, "IND": 5},
                    "Abstengo":  {"PD": 5, "PR": 15, "IND": 5},
                    "En Contra": {"PR": 25},
                }

                Estas opciones serán incluídas de la forma:
         ------------------------------------------------------------------
        |    votos option1    |   votos option2   |...|   votos optionN    |
         ------------------------------------------------------------------


    [opcionesV] Una estructura de la forma:
                {
                    <opcion1>: {<grupo1>: n, <grupo2>: n, ..., <grupoN>: n},
                    <opcion2>: {<grupo1>: n, <grupo2>: n, ..., <grupoN>: n},
                    ...,
                    <opcionN>: {<grupo1>: n, <grupo2>: n, ..., <grupoN>: n}
                }

                Ejemplo:
                {"Ausentes": {"PD": 5, "PR": 8, "IND": 2}}

                Estas opciones serán incluídas de la forma:
                         --------------------
                        |    votos option1   |
                         --------------------
                        |    votos option2   |
                         --------------------
                                    ...
                         --------------------
                        |    votos optionN   |
                         --------------------

    
    [pareos]    Si no es ingresado, no se imprimirán pareos en la
                votación. Si es ingresado, debe ser una lista de los pareos con
                la forma:
                [(<grupo1>, <grupo2>), (<grupo3>, <grupo4>), ...]

                Por ejemplo:
                [("PD", "PR"), ("PD", "PR"), ("PD", "IND")]


    -------
    RETURNA
    -------
    Una imagen con los datos ingresados
    '''
    # Abre imagen vacía
    im   = Image.open("draw/img/plantilla.png")
    draw = ImageDraw.Draw(im)

    # Escribe encabezado
    # TODO: Arreglar el ingreso de los títulos como argumento
    #titulo = input("Ingresa un título: ")
    titulo = "Título"
    draw.text((100,100), titulo,    font=title,    fill='#333344')
    #titulo = input("Ingresa un subtítulo: ")
    subtitulo = "Subtitulo subtitulo"
    draw.text((100,200), subtitulo, font=subtitle, fill='#9999AA')
    draw.text((700,250), resultado, font=subtitle, fill='#AA0033')
    if nquorum > 0:
        draw.text((120,250), f"Quorum: {quorum}", font=subtitle, fill='#333344')
        draw.text((120,300), f"Votos necesarios: {nquorum}", font=normal, fill='#9999AA')

    # Dibuja opciones
    total_col = 23
    global_iniX = (1080 - 40*total_col) // 2
    global_iniY = 350
        #   Horizontal
    total_colH = total_col - len(opcionesH)
    votosH = sum_votes((opcionesH,))
    filas = ceil(votosH / total_colH)
    iniX, iniY  = (global_iniX, global_iniY)
    endY_max = -1
    posX = [] # Guarda las posiciones de inicio y término de cada opción
    for opcion in opcionesH:
        #TODO: Nombre de la opción escrito en vertical
        iniX += 40
        if filas == 0:
            continue
        columnas = ceil(votosH / filas)
        endX, endY = draw_points(draw, iniX, iniY, opcionesH[opcion], columnas, grupos)
        posX.append((iniX-40, endX))
        iniX = endX
        if endY > endY_max:
            endY_max = endY
    #TODO: Cuadro delimitador de cada opción
    for iniX, endX in posX:
        # Dibujar cuadrado desde (iniX, global_iniY) hasta (endX, endY_max)
        pass
    #TODO END
        #   Vertical
    iniX, iniY = (global_iniX, endY_max)
    for opcion in opcionesV:
        #TODO: Nombre de la opción escrito en horizontal
        iniY += 40
        # Dibujar votos en vertical
        _, endY = draw_points(draw, iniX, iniY, opcionesV[opcion], total_col, grupos)
        #TODO: Cuadro delimitador de opcion
        iniY = endY
    if len(pareos) > 0:
        #TODO: Nombre de la opción 'Pareo' escrito en horizontal
        _, endY = draw_pareos(draw, iniX, iniY, pareos, total_col, grupos)
        #TODO: Cuadro delimitador de opción 'Pareo'
        iniY = endY
    
    # Dibuja leyenda
    lenX = 40*total_col
    draw_legend(draw, lenX, iniY+80, grupos)

    # Dibuja banner inferior
    # TODO: Dibujar banner inferior

    #im.show()
    return im