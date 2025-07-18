# https://sashamaps.net/docs/resources/20-colors/
import random




background_color = '#fdfdbd'

# Paleta de partidos (incluyendo movimientos no legalizados)
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

# Paleta de partidos (solo legalizados)
partidos = {
    # Apruebo Dignidad - Frente Amplio
    'CS':   ['Convergencia Social',                  '#911eb4'],
    'CO':   ['Comunes',                              '#f032e6'],
    'RD':   ['Revolución Democrátiva',               '#FF8A8E'],
    # Apruebo Dignidad - Chile Digno
    'PC':   ['Partico Comunista',                    '#e6194B'],
    'FRVS': ['Federación Regionalista Verde Social', '#800000'],
    # Unidad Constituyente
    'PS':   ['Partido Socialista',                   '#fabed4'],
    'PL':   ['Partido Liberal',                      '#808000'],
    'PPD':  ['Partido Por la Democracia',            '#bfef45'],
    'PR':   ['Partido Radical',                      '#3cb44b'],
    'DC':   ['Democracia Cristiana',                 '#aaffc3'],
    # Chile Vamos
    'PRI':  ['Partido Regionalista Independiente',   '#004040'],
    'EVOP': ['Evopoli',                              '#469990'],
    'RN':   ['Renovación Nacional',                  '#42d4f4'],
    'UDI':  ['Unión Demócrata Independiente',        '#4363d8'],
    # Frente Social Cristiano
    'PCC':  ['Partico Conservador Cristiano',        '#2233AA'],
    'PREP': ['Partido Republicano',                  '#000075'],
    # Sin coalición
    'PEV':  ['Partido Ecologísta Verde',             '#9A6324'],
    'PH':   ['Partido Humanista',                    '#f58231'],
    'PDG':  ['Partido de la Gente',                  '#ffe119'],
    'IND':  ['Independiente',                        '#a9a9a9']
}


# Paleta de coaliciones (agrupando bancadas afines)
coaliciones = {
    'AD':  ['Apruebo Dignidad',    '#e6194B'],
    'NPC': ['Nuevo Pacto Social',  '#3cb44b'],
    'PDG': ['Partido de la Gente', '#ffe119'],
    'CV':  ['Chile Vamos',         '#42d4f4'],
    'REP': ['Republicanos',        '#000075'],
    'SC':  ['Sin Coalición',       '#a9a9a9']
}

# Retorna un color aleatorio
def random_color():
    colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
              '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4',
              '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000',
              '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9',
              '#ffffff', '#000000']
    return random.choice(colors)

# Retorna el color correspondiente al partido, según el diccionario de partidos
def color_partido(partido):
    return partidos[partido][1]

# Retorna el color correspondiente a la coalición, según el diccionario de coaliciones
def color_coalicion(coalicion):
    return coaliciones[coalicion][1]




if __name__ == "__main__":
    pass