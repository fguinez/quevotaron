'''
Propósito del módulo: Abstraer la generación de gráficas a diferentes contextos
'''

# https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
from PIL import Image, ImageFont
from math import floor, ceil
import textwrap
import sys
import os
if os.getcwd()[-4:] == "draw":
    from image_utils import ImageDraw
    from palette import color_partido, color_coalicion, random_color, background_color

    path_base = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1])
    path_root = '/'.join(path_base.split('/')[:-1])
else:
    from draw.image_utils import ImageDraw
    from draw.palette import color_partido, color_coalicion, random_color, background_color

    path_root = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1])
    path_base = f"{path_root}/draw"




# Se definen las tipografías a utilizar
font_title_path = f'{path_root}/draw/fonts/IBM-Plex-Sans/IBMPlexSans-Bold.ttf'
title    = ImageFont.truetype(font_title_path,   80)
font_subtitle_path = f'{path_root}/draw/fonts/IBM-Plex-Sans/IBMPlexSans-Medium.ttf'
subtitle = ImageFont.truetype(font_subtitle_path, 40)
normal   = ImageFont.truetype(f'{path_root}/draw/fonts/IBM-Plex-Sans/IBMPlexSans-Medium.ttf', 20)
footnote = ImageFont.truetype(f'{path_root}/draw/fonts/IBM-Plex-Sans/IBMPlexSans-Text.ttf', 20)

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

def draw_point(draw, x, y, r, color):
    r = int(r)
    container = Image.new('RGB', (r*50, r*50), color=background_color)
    draw_container = ImageDraw(container)
    draw_container.ellipse((0, 0, r*50, r*50), fill=color)
    container = container.resize((r*2, r*2), Image.LANCZOS)
    draw.im_.paste(container, (x-r, y-r))

def draw_text_horizontal(draw, text, pos, font, fill, align='bottom'):
    x, y = pos
    labelsize = font.getsize(text)
    label = Image.new('RGBA', labelsize, background_color)
    draw_label = ImageDraw(label)
    draw_label.text((0, 0), text, font=font, fill=fill)
    label = label.rotate(90, expand=1)
    if align == 'bottom':
        draw.im_.paste(label, (x, y))
    else:
        draw.im_.paste(label, (x, y-labelsize[0]))

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
            draw_point(draw, x, y, r, color)
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
        i = d %  (cols if cols%2==0 else cols-1)
        j = d // (cols if cols%2==0 else cols-1)
        x = iniX + i*R*2
        y = iniY + j*R*2
        draw.line([(x,y), (x+2*R, y)], fill='#000000', width=5)
        draw_point(draw, x, y, r, grupos[grupo1][1])
        draw_point(draw, x+2*R, y, r, grupos[grupo2][1])
        d += 2
    endX = iniX + cols*R*2 - R
    endY = iniY +    j*R*2 + R
    return endX, endY

def _draw_legend_line(draw, grupos, lenX, iniY):
    iniX = (1080 - lenX) / 2
    for grupo in grupos:
        x = int(iniX + R)
        y = int(iniY + R)
        draw_point(draw, x, y, r, grupo[1])
        draw.text((iniX+40,iniY+5), grupo[0], font=normal, fill='#333344')
        iniX += 40 + normal.getsize(grupo[0])[0] + 20

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
    line = []
    len_line = -20
    for grupo in grupos.values():
        len_line_next = len_line + 40 + normal.getsize(grupo[0])[0]
        if len_line_next > lenX:
            _draw_legend_line(draw, line, len_line, iniY)
            line = []
            len_line = -20
            iniY += 40
        line.append(grupo)
        len_line += 20 + 40 + normal.getsize(grupo[0])[0]
    _draw_legend_line(draw, line, len_line, iniY)
    return iniY + 40 
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
            votes += len(conjunto)
    return votes

def center_image(im, height, min_padding=90):
    padding = (1080 - height) / 2
    if padding < min_padding:
        padding = min_padding
    padding = int(padding)
    container_size = (1080, height + padding*2 + 10)
    container = Image.open("draw/img/plantilla.png").resize(container_size)
    container.paste(im, (0, padding))
    return container, padding
     

def create_image(titulo='', subtitulo='', tipo='', resultado='', quorum='', nquorum=-1, grupos={},
                 opcionesH={}, opcionesV={}, pareos=[], fecha='', votid=''):
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
    im_size = (1080, 2000)
    im   = Image.open("draw/img/plantilla.png").resize(im_size)
    draw = ImageDraw(im)
    draw.im_ = im

    # Escribe encabezado
    title_size = draw.write_text_box((100, -40), titulo, box_width=880, box_height=200,
                   font_filename=font_title_path, font_size='fill', color=background_color)
    bajada_pos = [100, title_size[1]+5]
    bajada = tipo
    if subtitulo:
        bajada += f" — {subtitulo}"
    bajada_size = draw.write_text_box(bajada_pos, bajada, box_width=880, box_height=80,
                   font_filename=font_subtitle_path, font_size='fill', color=background_color,
                   max_font_size=25)
    headerH = title_size[1] + bajada_size[1] + 30
    if resultado.lower() == "rechazado":
        color_resultado = '#AA0033'
    else:
        color_resultado = '#00AA33'
    draw.text((700,headerH+20), resultado, font=subtitle, fill=color_resultado)
    if nquorum > 0:
        draw.text((120,headerH+20), f"Quorum: {quorum}", font=subtitle, fill='#333344')
        draw.text((130,headerH+70), f"Votos necesarios: {nquorum}", font=normal, fill='#9999AA')

    # Dibuja opciones
    total_col = 23
    global_iniX = (1080 - 40*total_col) // 2 - 20
    global_iniY = headerH+120
        #   Horizontal
    total_colH = total_col - len(opcionesH)
    votosH = sum_votes((opcionesH,))
    filas = floor(votosH / (total_colH-1)) + 1
    iniX, iniY  = (global_iniX, global_iniY)
    endY_max = -1
    posX = [] # Guarda las posiciones de inicio y término de cada opción
    for opcion in opcionesH:
        # Nombre de la opción escrito en vertical
        total_opcion = sum(opcionesH[opcion].values())
        text = f"{opcion}: {total_opcion}"
        draw_text_horizontal(draw, text, (iniX+10, iniY+20), font=normal, fill='#333344')
        # Despliegue de votos
        iniX += 40
        if filas == 0:
            continue
        columnas = ceil(total_opcion / filas)
        if columnas == 0:
            continue
        endX, endY = draw_points(draw, iniX, iniY, opcionesH[opcion], columnas, grupos)
        posX.append((iniX-40, endX))
        iniX = endX
        if endY > endY_max:
            endY_max = endY
        #   Vertical
    iniX, iniY = (global_iniX, endY_max)
    for opcion in opcionesV:
        # Nombre de la opción escrito en horizontal
        total_opcion = sum(opcionesV[opcion].values())
        draw.text((iniX+60, iniY+12), f"{opcion}: {total_opcion}", font=normal, fill='#333344')
        iniY += 40
        # Dibujar votos en vertical
        _, endY = draw_points(draw, iniX+40, iniY, opcionesV[opcion], total_col-1, grupos)
        iniY = endY
    if len(pareos) > 0:
        # Nombre de la opción 'Pareo' escrito en horizontal
        total_pareos = sum_votes(pareos)
        draw.text((iniX+60, iniY+12), f"Pareos: {total_pareos}", font=normal, fill='#333344')
        iniY += 40
        _, endY = draw_pareos(draw, iniX+40, iniY, pareos, total_col-1, grupos)
        iniY = endY
    
    # Dibuja leyenda
    global_endY = draw_legend(draw, 1000, iniY+40, grupos)
    
    # Centra la visualización
    im, padding = center_image(im, global_endY)

    # Redibuja el título, para evitar que sea cortado por center_image
    draw = ImageDraw(im)
    draw.write_text_box((100, padding-40), titulo, box_width=880, box_height=200,
                   font_filename=font_title_path, font_size='fill', color='#333344')
    bajada_pos[1] += padding
    draw.write_text_box(bajada_pos, bajada, box_width=880, box_height=80,
                   font_filename=font_subtitle_path, font_size='fill', color='#9999AA',
                   max_font_size=25)    

    # Escribir banner inferior con más información
    text = f"@QueVotaron   |   #VotaciónDiputados{votid}   |   {fecha}"
    posicion_banner = (im.size[0]//2, im.size[1]-40)
    draw.text(posicion_banner, text, font=footnote, fill='#9999AA', anchor="mt")
    return im




if __name__ == "__main__":
    titulo = "Suprime el rango etario para ejercer el permiso laboral establecido en el artículo 66 bis del Código del Trabajo."
    dimensiones = (880, 100)
    ajustar_fuente(title, titulo, dimensiones)