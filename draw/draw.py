# https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
from PIL import Image, ImageDraw, ImageFont
from math import ceil
import sys

from draw.palette import color_partido, color_coalicion, random_color




title   = ImageFont.truetype('fonts/IBM-Plex-Sans/IBMPlexSans-Bold.ttf',   80)
section = ImageFont.truetype('fonts/IBM-Plex-Sans/IBMPlexSans-Medium.ttf', 40)



def sort_group(group):
    group = list(group)
    if 'SC' in list(group):
        group.remove('SC')
        group.append('SC')
    if 'IND' in list(group):
        group.remove('IND')
        group.append('IND')
    return group

def draw_points(draw, iniX, iniY, votos, cols=20, group='coalicion'):
    color_group = color_partido if group == 'partido' else color_coalicion
    R = 20
    r = 0.7 * R
    initX = iniX + R
    initY = iniY + R
    d = 0
    for group in sort_group(votos.keys()):
        color = color_group(group)
        for _ in range(votos[group]):
            i = d %  cols
            j = d // cols
            x = initX + i*R*2
            y = initY + j*R*2
            draw.ellipse((x-r, y-r, x+r, y+r), fill=color)
            d += 1
    endX = initX + cols*R*2 - R
    endY = initY +    j*R*2 + R
    return endX, endY

def draw_pareos(draw, iniX, iniY, pareos, cols=20, group='coalicion'):
    color_group = color_partido if group == 'partido' else color_coalicion
    R = 20
    r = 0.7 * R
    initX = iniX + R
    initY = iniY + R
    d = 0
    for pareo1, pareo2 in pareos:
        i = d %  cols
        j = d // cols
        x = initX + i*R*2
        y = initY + j*R*2
        draw.line([(x,y), (x+2*R, y)], fill='#000000', width=5)
        draw.ellipse((x-r,     y-r, x+r,     y+r), fill=color_group(pareo1))
        draw.ellipse((x-r+2*R, y-r, x+r+2*R, y+r), fill=color_group(pareo2))
        d += 2
    endX = initX + cols*R*2 - R
    endY = initY +    j*R*2 + R
    return endX, endY

def create_image(votacion, titulo, group='coalicion'):
    if group.lower() == 'coalicion':
        votos_a_favor    = votacion.a_favor_coalicion
        votos_abstencion = votacion.abstencion_coalicion
        votos_en_contra  = votacion.en_contra_coalicion
        votos_ausentes   = votacion.ausentes_coalicion
        votos_pareos     = votacion.pareos_coalicion
    elif group.lower() == 'partido':
        votos_a_favor    = votacion.a_favor_partido
        votos_abstencion = votacion.abstencion_partido
        votos_en_contra  = votacion.en_contra_partido
        votos_ausentes   = votacion.ausentes_partido
        votos_pareos     = votacion.pareos_partido
    im   = Image.open("img/plantilla.png")
    draw = ImageDraw.Draw(im)
    draw.text((100,100), titulo, font=title, fill='#333333')
    votan = 155 - (votacion.ausentes + votacion.pareos) # A favor + Abstienen + En contra
    filas = ceil(votan / 20)
    col_a_favor    = ceil(votacion.a_favor    / filas)
    col_abstencion = ceil(votacion.abstencion / filas)
    col_en_contra  = ceil(votacion.en_contra  / filas)
    total_col = col_a_favor + col_abstencion + col_en_contra
    #fil_ausentes = ceil(votacion.ausentes / 20)
    #fil_pareos   = ceil(votacion.pareos / 20)
    
    global_iniX = (1080 - 40*total_col - 120) // 2
    global_iniY = 300

    # Dibuja a favor
    iniX, iniY  = (global_iniX, global_iniY)
    endX, endY1 = draw_points(draw, iniX, iniY, votos_a_favor, col_a_favor, group)
    # Dibuja abstencion
    iniX, iniY  = (endX+60, iniY)
    endX, endY2 = draw_points(draw, iniX, iniY, votos_abstencion, col_abstencion, group)
    # Dibuja en contra
    iniX, iniY3 = (endX+60, iniY)
    _,    endY3 = draw_points(draw, iniX, iniY, votos_en_contra, col_en_contra, group)
    # Dibuja ausentes
    endY = max(endY1 ,endY2 ,endY3)
    iniX, iniY = (global_iniX, endY+60)
    _, endY = draw_points(draw, iniX, iniY, votos_ausentes, total_col+3, group)
    # Dibuja pareo
    iniX, iniY = (global_iniX, endY+60)
    _, endY = draw_pareos(draw, iniX, iniY, votos_pareos, total_col+3, group)


    im.show()