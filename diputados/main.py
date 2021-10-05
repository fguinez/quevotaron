from votaciones import get_votacion
import api
import json
import sys
import os




# Define el path a la carpeta diputados
path_diputados = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1])
# Define el path a la carpeta root
path_root = '/'.join(path_diputados.split('/')[:-1])




if __name__ == "__main__":

    #votids = [36472, 36976, 36975, 36974, 36973]
    #votids += api.get_votaciones_recientes()
    votids = [36472, 37017, 37020, 36971]
    if len(sys.argv) > 1:
            votids = [int(sys.argv[1])]
    
    for votid in votids:
        print(votid)

        # Define el path a la información necesaria para crear la visualización
        filename = f"{votid}.json"
        path = f"{path_root}/draw/data/diputados/{filename}"

        if not os.path.exists(path):
            # Obtenemos la información de la votación
            votacion = get_votacion(votid)
            # Guardamos el objeto de la votación
            with open(path, 'w') as file:
                json.dump(votacion.json, file)

        titulo = ""
        # Si fue ingresado como argumento, rescatamos el título de la visualización
        if len(sys.argv) > 2:
            titulo = sys.argv[2]

        # Cambiamos el directorio actual a la carpeta raiz
        os.chdir(path_root)

        # Ejecutamos la generación de la visualización de la votación
        os.system(f"python3 draw/main.py {path} {titulo}")