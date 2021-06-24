# https://sashamaps.net/docs/resources/20-colors/
import random



def random_color():
    colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
              '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4',
              '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000',
              '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9',
              '#ffffff', '#000000']
    return random.choice(colors)

def color_partido():
    pass

def color_coalicion(coalicion):
    if coalicion == 'AD':
        return '#e6194B'
    if coalicion == 'UC':
        return '#3cb44b'
    if coalicion == 'CV':
        return '#4363d8'
    return '#a9a9a9'