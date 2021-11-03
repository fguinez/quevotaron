from diputados import api, votaciones
from draw import generar_visualizaciones
from utils import osx, color, str_fecha
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from math import ceil
import tweepy
import json
import time
import datetime as dt
import os
from dotenv import dotenv_values

env = dotenv_values(osx.this_file()+"/.env")




class Bot:
    def __init__(self):
        # Twitter
        auth_twitter = tweepy.OAuthHandler(env['API_KEY'], env['API_KEY_SECRET'])
        auth_twitter.set_access_token(env['ACCESS_TOKEN'], env['ACCESS_TOKEN_SECRET'])
        self.twitter = tweepy.API(auth_twitter)
        # Drive
        gauth = GoogleAuth()           
        self.drive = GoogleDrive(gauth)  
        self.folders = {
            'html': "1quICwB6EvhRqzjh1BBkiUaE7Xbtf81DF",
            'json': "1cZTZRe58wHsO9ww_SPmoiSMg2CWSkzRr",
            'vis':  "1Snf3bP4tHCX7JxtJcKKRDEi_I7_vVLFT"
        }

        # Paths
        self.paths = {
            'ultimas_votaciones_publicadas': "tmp/ultimas_votaciones_publicadas.txt",
            'html': "tmp/html",
            'json': "tmp/json",
            'vis':  "tmp/visualizaciones"
        }
        for key, path in self.paths.items():
            if key == 'ultimas_votaciones_publicadas':
                osx.create_file(path)
            else:
                osx.create_dirs(path)

        self.ultimas_votaciones_publicadas = self.read_ultimas_votaciones_publicadas()


    def read_ultimas_votaciones_publicadas(self):
        path = self.paths['ultimas_votaciones_publicadas']
        with open(path, 'r') as file:
            ultimas_votaciones_publicadas = file.read().strip().splitlines()
        return [int(v) for v in ultimas_votaciones_publicadas]

    def write_ultimas_votaciones_publicadas(self):
        path = self.paths['ultimas_votaciones_publicadas']
        with open(path, 'w') as file:
            for votid in self.ultimas_votaciones_publicadas[-30:]:
                file.write(str(votid) + '\n')

    def read_votacion_info(self, votid):
        path = self.paths['html']
        votacion_info = votaciones.get_votacion(votid, path=path).json
        return votacion_info

    def write_votacion_info(self, votacion_info):
        path = self.paths['json'] + f"/{votacion_info['id']}.json"
        with open(path, 'w') as file:
            json.dump(votacion_info, file)

    def procesar_votid(self, votid, tipo=None, tweet=True, cloud=True, fecha=False):
        # Obtiene datos de votid
        votacion_info = self.read_votacion_info(votid)
        if tipo:
            votacion_info['tipo'] += f" (Votación {tipo})"
        # Genera visualizaciones de voitid
        media_paths = generar_visualizaciones(votid, votacion_info, path=self.paths['vis'])
        if tweet:
            # Twittea votid
            if fecha:
                fecha = str_fecha(votacion_info['fecha'])
            self.tweet_votacion(votid, media_paths, fecha=fecha)
        self.write_votacion_info(votacion_info)
        if cloud:
            # Sube la info a Google Drive
            self.subir_a_drive(votid)
        return media_paths

    def run(self, sleep=30):
        while True:
            try:
                nuevas_votaciones = self.get_nuevas_votaciones()
                for votid, tipo in nuevas_votaciones:
                    try:
                        print(f"Votación {votid}:", color.y("Pendiente"), end='\r')
                        self.procesar_votid(votid, tipo, fecha=True)
                        print(f"Votación {votid}:", color.g("Publicada"))
                    except Exception as err:
                        print(f"Votación {votid}:", color.r("Error    "))
                        print(err)
            except ConnectionError as err:
                print(err)
                print(color.r("ERROR:"), "Ha ocurrido un error de conexión. Esperando 1 hora... ")
                time.sleep(60*60)
                print(color.g("OK"))
            hora_actual = dt.datetime.now()
            if hora_actual.hour > 23 or hora_actual.hour < 9:
                # Se duerme de 23 a 9 horas
                hora_regreso = dt.datetime(hora_actual.year, hora_actual.month, hora_actual.day, 9)
                if hora_actual.hour > 23:
                    hora_regreso += dt.timedelta(days=1)
                diff = (hora_regreso - hora_actual).total_seconds()
                print(f"Durmiendo por {diff/60/60:.2f} horas... ", end='', flush=True)
                time.sleep(ceil(diff))
                print(color.g("OK"))
            time.sleep(sleep)

    def get_nuevas_votaciones(self):
        ids_recientes, tipos_recientes = api.get_votaciones_recientes()
        recientes = zip(ids_recientes, tipos_recientes)
        ids_publicadas = self.ultimas_votaciones_publicadas
        ids_nuevas_votaciones = set(ids_recientes) - set(ids_publicadas)
        nuevas_votaciones = filter(lambda r: r[0] in ids_nuevas_votaciones, recientes)
        nuevas_votaciones = sorted(nuevas_votaciones, key=lambda v: v[0])
        return list(nuevas_votaciones)

    def tweet_votacion(self, votid, media_paths, fecha=None):
        # Máximo de caracteres sin link: 256
        link = f'https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion={votid}'
        tweet_text = f'#VotaciónDiputados{votid}\n\n'
        if fecha:
            tweet_text += f'Fecha: {fecha}\n'
        tweet_text += f'Detalle: {link}'
        media_ids = [self.twitter.media_upload(i).media_id_string  for i in media_paths]
        status = self.twitter.update_status(status=tweet_text, media_ids=media_ids)
        self.ultimas_votaciones_publicadas.append(votid)
        return status

    def _subir_a_drive(self, filename, path, folder):
        gfile = self.drive.CreateFile({
            'title': filename,
            'parents': [{'id': folder}]
        })
        gfile.SetContentFile(path)
        gfile.Upload()

    def subir_a_drive(self, votid):
        path = f"{self.paths['html']}/{votid}.html"
        self._subir_a_drive(f"{votid}.html", path, self.folders['html'])
        path = f"{self.paths['json']}/{votid}.json"
        self._subir_a_drive(f"{votid}.json", path, self.folders['json'])
        path = f"{self.paths['vis']}/{votid}_coaliciones.png"
        self._subir_a_drive(f"{votid}_coaliciones.png", path, self.folders['vis'])
        path = f"{self.paths['vis']}/{votid}_partidos.png"
        self._subir_a_drive(f"{votid}_partidos.png", path, self.folders['vis'])



if __name__ == "__main__":
    bot = Bot()
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.write_ultimas_votaciones_publicadas()
        print("\n*beep boop* Adiós!")
        exit()

    exit()

    # Debug
    votids = osx.get_gen_votids()
    votids = bot.get_nuevas_votaciones()
    #votids = list(filter(lambda v: int(v) >= 36971 and int(v) < 37071, votids))
    #print(votids)
    votids = [(36725, 'mixta')]
    for votid, tipo in votids:
        print(votid)
        try:
            paths = bot.procesar_votid(votid, tipo, tweet=False, cloud=False, fecha=True)
        except IndexError as err:
            print(votid, "no existe")
            continue
        for p in paths:
            print(p)
        print()