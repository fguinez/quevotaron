# https://sashamaps.net/docs/resources/20-colors/
import random




partidos = {
    'CS':   ['Convergencia Social',                  '#911eb4'],
    'CO':   ['Comunes',                              '#f032e6'],
    'RD':   ['Revolución Democrátiva',               '#dcbeff'],
    'UN':   ['Unir',                                 '#fabed4'],
    'PC':   ['Partico Comunista',                    '#e6194B'],
    'FRVS': ['Federación Regionalista Verde Social', '#800000'],
    'AH':   ['Acción Humanista',                     '#f58231'],
    'PS':   ['Partido Socialista',                   '#808000'],
    'PPD':  ['Partido Por la Democracia',            '#bfef45'],
    'PL':   ['Partido Liberal',                      '#fffac8'],
    'PR':   ['Partido Radical',                      '#ffe119'],
    'DC':   ['Democracia Cristiana',                 '#aaffc3'],
    'EVOP': ['Evopoli',                              '#42d4f4'],
    'RN':   ['Renovación Nacional',                  '#4363d8'],
    'UDI':  ['Unión Demócrata Independiente',        '#000075'],
    'PEV':  ['Partido Ecologísta Verde',             '#9A6324'],
    'PH':   ['Partido Humanista',                    '#ffd8b1'],
    'PLR':  ['Partido Republicano',                  '#469990'],
    'IND':  ['Independiente',                        '#a9a9a9']
}


coaliciones = {
    'AD': ['Apruebo Dignidad',     '#e6194B'],
    'UC': ['Unidad Constituyente', '#3cb44b'],
    'CV': ['Chile Vamos',          '#4363d8'],
    'SC': ['Sin Coalición',        '#a9a9a9']
}



def random_color():
    colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
              '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4',
              '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000',
              '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9',
              '#ffffff', '#000000']
    return random.choice(colors)

def color_partido(partido):
    # Apruebo Dignidad - Frente Amplio
    if partido == 'CS':                 # Convergencia Social
        return '#911eb4'
    if partido == 'CO':                 # Comunes
        return '#f032e6'
    if partido == 'RD':                 # Revolución Democrátiva
        return '#dcbeff'
    if partido == 'UN':                 # Unir
        return '#fabed4'
    # Apruebo Dignidad - Chile Digno
    if partido == 'PC':                 # Partico Comunista
        return '#e6194B'
    if partido == 'FRVS':               # Federación Regionalista Verde Social
        return '#800000'
    if partido == 'AH':                 # Acción Humanista
        return '#f58231'
    # Unidad Constituyente
    if partido == 'PS':                 # Partido Socialista
        return '#808000'
    if partido == 'PPD':                # Partido Por la Democracia
        return '#bfef45'
    if partido == 'PL':                 # Partido Liberal
        return '#fffac8'
    if partido == 'PR':                 # Partido Radical
        return '#ffe119'
    if partido == 'DC':                 # Democracia Cristiana
        return '#aaffc3'
    # Chile Vamos
    if partido == 'EVOP':               # Evopoli
        return '#42d4f4'
    if partido == 'RN':                 # Renovación Nacional
        return '#4363d8'
    if partido == 'UDI':                # Unión Demócrata Independiente
        return '#000075'
    # Sin coalición
    if partido == 'PEV':                # Partido Ecologísta Verde
        return '#9A6324'
    if partido == 'PH':                 # Partido Humanista
        return '#ffd8b1'
    if partido == 'PLR':                # Partido Republicano
        return '#469990'
    if partido == 'IND':                # Independiente
        return '#a9a9a9'

def color_coalicion(coalicion):
    # Apruebo Dignidad
    if coalicion == 'AD':
        return '#e6194B'
    # Unidad Constituyente
    if coalicion == 'UC':
        return '#3cb44b'
    # Chile Vamos
    if coalicion == 'CV':
        return '#4363d8'
    return '#a9a9a9'