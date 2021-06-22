import time




class Diputado:
    def __init__(self, id, nombre, apellido_paterno, apellido_materno, partido, coalicion):
        self.id        = id
        self.nombre    = nombre + apellido_paterno + apellido_materno
        self. partido  = partido
        self.coalicion = coalicion
        self.ausente = True
        self.voto = None
        self.pareo = False
        self.pareo_id = -1

    def votar(self, opcion, pareo_id=-1):
        self.ausente = False
        # A favor (Apruebo / Afirmativo)
        if opcion.capitalize()[0] == "Ap":
            self.voto = "A favor"
        # En contra (Rechazo)
        elif opcion.capitalize()[0] == "E":
            self.voto = "En contra"
        # Abstienen
        elif opcion.capitalize()[0] == "Ab":
            self.voto = "Abstienen"
        elif opcion.capitalize()[0] == "P":
            self.voto = "Pareo"
            self.pareo = True
            self.pareo_id = pareo_id

class Votacion:
    def __init__(self, id, fecha, tipo, resultado, quorum, a_favor, abstencion, en_contra):
        self.id = id
        self.fecha = time.strptime(fecha, '%Y-%m-%dT%H:%M:%S')
        self.tipo = tipo
        self.resultado = resultado
        self.quorum = quorum
        self.a_favor = a_favor
        self.abstencion = abstencion
        self.en_contra = en_contra
        #self.pareo
        #self.ausentes