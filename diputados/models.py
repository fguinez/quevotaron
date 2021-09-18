import time




class Diputado:
    def __init__(self, id, nombre, partido, coalicion, distrito=None):
        self.id        = id
        self.nombre    = nombre
        self.partido   = partido
        self.coalicion = coalicion
        self.ausente = True
        self.voto = None
        self.pareo = False
        self.pareo_id = -1

        self.distrito = distrito

    def votar(self, opcion, pareo_id=-1):
        self.ausente = False
        # A favor (Apruebo / Afirmativo)
        if opcion.capitalize()[:2] in ["Ap", "Af"]:
            self.voto = "A favor"
        # Abstienen
        elif opcion.capitalize()[:2] == "Ab":
            self.voto = "Abstienen"
        # En contra (Rechazo)
        elif opcion.capitalize()[0] in ["E", "R"]:
            self.voto = "En contra"
        # Pareo
        elif opcion.capitalize()[0] == "P":
            self.voto = "Pareo"
            self.pareo = True
            self.pareo_id = pareo_id

class Votacion:
    def __init__(self, id, fecha, tipo, resultado, quorum, a_favor, abstencion, en_contra, diputados, votos):
        self.id         = int(id)
        self.fecha      = time.strptime(fecha, '%d %m %Y')
        self.tipo       = tipo
        self.resultado  = resultado
        self.quorum     = quorum
        self.diputados  = diputados
        self.a_favor    = a_favor
        self.abstencion = abstencion
        self.en_contra  = en_contra
        
        self.a_favor_partido    = {}
        self.abstencion_partido = {}
        self.en_contra_partido  = {}
        self.ausentes_partido   = {}
        self.pareos_partido = []

        self.a_favor_coalicion    = {}
        self.abstencion_coalicion = {}
        self.en_contra_coalicion  = {}
        self.ausentes_coalicion   = {}
        self.pareos_coalicion = []

        self.generar_detalle(votos)
        
    def generar_votos(self, votos, opcion):
        '''
        (str) opcion: A favor, En contra, Abstención
        '''
        opcion_title = list(filter(lambda voto: voto.text.lower() == opcion.lower(), votos))[0]
        votos_opcion = opcion_title.find_next("div")
        for voto in votos_opcion.find_all("a"):
            dipid = int(voto["href"].split('=')[-1])
            self.diputados[dipid].votar(opcion)

    def generar_pareos(self, votos):
        pareos_title = list(filter(lambda voto: voto.text.lower() == "pareos", votos))[0]
        pareos = pareos_title.find_next("div")
        for pareo in pareos.find_all("li"):
            diputado1, diputado2 = pareo.find_all("a")
            dipid1 = int(diputado1["href"].split('=')[-1])
            dipid2 = int(diputado2["href"].split('=')[-1])
            diputado1 = self.diputados[dipid1]
            diputado2 = self.diputados[dipid2]
            diputado1.votar("Pareo", pareo_id=dipid2)
            diputado2.votar("Pareo", pareo_id=dipid1)
            self.pareos_partido.append([diputado1.partido, diputado2.partido])
            self.pareos_coalicion.append([diputado1.coalicion, diputado2.coalicion])

    def generar_detalle(self, votos):
        self.generar_votos(votos, "A favor")
        self.generar_votos(votos, "Abstención")
        self.generar_votos(votos, "En Contra")
        self.generar_pareos(votos)
        self.ausentes = len(list(filter(lambda diputado: diputado.ausente,         self.diputados.values())))
        self.pareos   = len(list(filter(lambda diputado: diputado.voto == "Pareo", self.diputados.values())))
        for diputado in self.diputados.values():
            if diputado.ausente:
                self.append(self.ausentes_partido,   diputado.partido)
                self.append(self.ausentes_coalicion, diputado.coalicion)
            else:
                if diputado.voto == "A favor":
                    self.append(self.a_favor_partido,   diputado.partido)
                    self.append(self.a_favor_coalicion, diputado.coalicion)
                if diputado.voto == "Abstienen":
                    self.append(self.abstencion_partido,   diputado.partido)
                    self.append(self.abstencion_coalicion, diputado.coalicion)
                if diputado.voto == "En contra":
                    self.append(self.en_contra_partido,   diputado.partido)
                    self.append(self.en_contra_coalicion, diputado.coalicion)

    @staticmethod
    def append(my_dict, elem):
        if elem in my_dict.keys():
            my_dict[elem] += 1
        else:
            my_dict[elem] = 1
        return my_dict

    @property
    def info_partido(self):
        opcionesH = {
            "A favor": self.a_favor_partido,
            "Abstienen": self.abstencion_partido,
            "En contra": self.en_contra_partido
        }
        opcionesV = {
            "Ausentes": self.ausentes_partido
        }
        return opcionesH, opcionesV, self.pareos_partido

    @property
    def info_coalicion(self):
        opcionesH = {
            "A favor": self.a_favor_coalicion,
            "Abstienen": self.abstencion_coalicion,
            "En contra": self.en_contra_coalicion
        }
        opcionesV = {
            "Ausentes": self.ausentes_coalicion
        }
        return opcionesH, opcionesV, self.pareos_coalicion

    def __str__(self):
        text  = ""
        text += f"id:     {self.id}\n"
        text += f"tipo:   {self.tipo}\n"
        text += f"quorum: {self.quorum}\n"
        text += f"RESULTADO: {self.resultado}\n"
        text += f"A favor:   {self.a_favor}\n"
        text += f"Abstienen: {self.abstencion}\n"
        text += f"En contra: {self.en_contra}\n"
        text += f"Ausentes:  {self.ausentes}\n"
        text += f"Pareos:    {self.pareos}\n"
        return text