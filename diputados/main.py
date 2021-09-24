from votaciones import get_votacion
import pickle
import sys
import os




# Define el path a la carpeta diputados
path_diputados = os.getcwd() + '/'.join([''] + sys.argv[0].split('/')[:-1])
# Define el path a la carpeta root
path_root = '/'.join(path_diputados.split('/')[:-1])




if __name__ == "__main__":
    votid = 36472
    if len(sys.argv) > 1:
        votid = int(sys.argv[1])

    # Define el path a la información necesaria para crear la visualización
    filename = f"{votid}.pkl"
    path = f"{path_root}/draw/data/diputados/{filename}"

    if not os.path.exists(path):
        # Obtenemos la información de la votación
        votacion = get_votacion(votid)
        # Guardamos el objeto de la votación
        with open(path, 'wb') as file:
            pickle.dump(votacion.info, file)

    titulo = ""
    # Si fue ingresado como argumento, rescatamos el título de la visualización
    if len(sys.argv) > 2:
        titulo = sys.argv[2]

    # Cambiamos el directorio actual a la carpeta raiz
    os.chdir(path_root)

    # Ejecutamos la generación de la visualización de la votación
    os.system(f"python3 draw/main.py {path} {titulo}")