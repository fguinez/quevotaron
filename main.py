from diputados import api, votaciones
from draw import generar_visualizaciones
from utils import osx, color
import tweepy
import time
import os
from dotenv import dotenv_values

env = dotenv_values(osx.this_file()+"/.env")




class Bot:
    def __init__(self):
        self.auth_twitter = tweepy.OAuthHandler(env['API_KEY'], env['API_KEY_SECRET'])
        self.auth_twitter.set_access_token(env['ACCESS_TOKEN'], env['ACCESS_TOKEN_SECRET'])
        self.api_twitter = tweepy.API(self.auth_twitter)
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

    def procesar_votid(self, votid, tweet=True):
        # Obtiene datos de votid
        votacion_info = votaciones.get_votacion(votid).json
        # Genera visualizaciones de voitid
        media_paths = generar_visualizaciones(votid, votacion_info)
        if tweet:
            # Twittea votid
            self.tweet_votacion(votid, media_paths)
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
        media_ids = [self.api_twitter.media_upload(i).media_id_string  for i in media_paths]
        status = self.api_twitter.update_status(status=tweet_text, media_ids=media_ids)
        self.ultimas_votaciones_publicadas.append(votid)
        return status




if __name__ == "__main__":
    bot = Bot()
    bot.run()
    
    exit()

    votids = osx.get_gen_votids()
    for votid in votids:
        print(votid)
        paths = bot.procesar_votid(votid, tweet=False)
        for p in paths:
            print(p)
        print()