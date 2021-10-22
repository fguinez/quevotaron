from diputados import api, votaciones
from draw import generar_visualizaciones
from utils import osx, color
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import tweepy
import json
import time
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

        self.ultimas_votaciones_publicadas = self.read_ultimas_votaciones_publicadas()

    @staticmethod
    def read_ultimas_votaciones_publicadas():
        path = f"{osx.this_file()}/tmp/ultimas_votaciones_publicadas.txt"
        if not os.path.exists(path):
            osx.create_file(path)
        with open(path, 'r') as file:
            ultimas_votaciones_publicadas = file.read().strip().splitlines()
        return [int(v) for v in ultimas_votaciones_publicadas]

    def write_ultimas_votaciones_publicadas(self):
        path = f"{osx.this_file()}/tmp/ultimas_votaciones_publicadas.txt"
        if not os.path.exists(path):
            osx.create_file(path)
        with open(path, 'w') as file:
            for votid in self.ultimas_votaciones_publicadas[-30:]:
                file.write(str(votid) + '\n')

    @staticmethod
    def write_votacion_info(votacion_info):
        path = f"{osx.this_file()}/tmp/json/{votacion_info['id']}.json"
        if not os.path.exists(path):
            osx.create_file(path)
        with open(path, 'w') as file:
            json.dump(votacion_info, file)

    def procesar_votid(self, votid, tweet=True, cloud=True):
        # Obtiene datos de votid
        votacion_info = votaciones.get_votacion(votid).json
        # Genera visualizaciones de voitid
        media_paths = generar_visualizaciones(votid, votacion_info)
        if tweet:
            # Twittea votid
            self.tweet_votacion(votid, media_paths)
        if cloud:
            self.write_votacion_info(votacion_info)
            # Sube la info a Google Drive
            self.subir_a_drive(votid)
        return media_paths

    def run(self, sleep=10):
        while True:
            try:
                nuevas_votaciones = self.get_nuevas_votaciones()
                for votid in nuevas_votaciones:
                    try:
                        print(f"Votación {votid}:", color.y("Pendiente"), end='\r')
                        self.procesar_votid(votid)
                        print(f"Votación {votid}:", color.g("Publicada"))
                    except Exception as err:
                        print(f"Votación {votid}:", color.r("Error"))
                        print(err)
                time.sleep(sleep)
            except KeyboardInterrupt:
                self.write_ultimas_votaciones_publicadas()
                print("\n*beep boop* Adiós!")
                exit()

    def get_nuevas_votaciones(self):
        recientes = api.get_votaciones_recientes()
        publicadas = self.ultimas_votaciones_publicadas
        nuevas_votaciones = set(recientes) - set(publicadas)
        return list(nuevas_votaciones)

    def tweet_votacion(self, votid, media_paths):
        # Máximo de caracteres sin link: 256
        link = f'https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion={votid}'
        tweet_text = f'Detalle de la votación: {link}'
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
        path = f'diputados/data/votaciones/{votid}.html'
        self._subir_a_drive(f"{votid}.html", path, self.folders['html'])
        path = f'tmp/json/{votid}.json'
        self._subir_a_drive(f"{votid}.json", path, self.folders['json'])
        path = f'visualizaciones/{votid}_coaliciones.png'
        self._subir_a_drive(f"{votid}_coaliciones.png", path, self.folders['vis'])
        path = f'visualizaciones/{votid}_partidos.png'
        self._subir_a_drive(f"{votid}_partidos.png", path, self.folders['vis'])



if __name__ == "__main__":
    bot = Bot()
    #bot.run()
    
    #exit()

    # Debug
    votids = osx.get_gen_votids()
    votids = [37093]
    for votid in votids:
        print(votid)
        paths = bot.procesar_votid(votid, tweet=False, cloud=False)
        for p in paths:
            print(p)
        print()