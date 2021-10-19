from diputados import api
from utils import osx
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
            ultimas_votaciones_publicadas = file.read().splitlines()
        return ultimas_votaciones_publicadas

    def write_ultimas_votaciones_publicadas(self):
        path = f"{osx.this_file()}/tmp/ultimas_votaciones_publicadas.txt"
        if not os.path.exists(path):
            osx.create_file(path)
        with open(path, 'w') as file:
            for votid in self.ultimas_votaciones_publicadas:
                file.write(str(votid) + '\n')

    def run(self, sleep=10):
        while True:
            nuevas_votaciones = self.get_nuevas_votaciones()
            for votid in nuevas_votaciones:
                # Obtiene datos de votid
                pass
                # Genera visualizaciones de voitid
                #media_ids = pass
                # Twittea votid
                self.tweet_votacion(votid, media_ids)
            time.sleep(sleep)

    def get_nuevas_votaciones(self):
        recent = api.get_votaciones_recientes()

    def tweet_votacion(self, votid, media_ids):
        # Máximo de caracteres sin link: 256
        link = f'https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion={votid}'
        tweet_text = f'Detalle de la votación: {link}'
        status = self.api_twitter.update_status(status=tweet_text, media_ids=media_ids)
        return status




if __name__ == "__main__":
    bot = Bot()
    #bot.run()
    #a = bot.write_ultimas_votaciones_publicadas()
    print(bot.ultimas_votaciones_publicadas)
    bot.ultimas_votaciones_publicadas.append(123456)
    bot.write_ultimas_votaciones_publicadas()