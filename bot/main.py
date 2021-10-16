import path
import tweepy
import time
from dotenv import dotenv_values

env = dotenv_values(path.this_file()+"/.env")




class Bot:
    def __init__(self):
        self.auth_twitter = tweepy.OAuthHandler(env['API_KEY'], env['API_KEY_SECRET'])
        auth_twitter.set_access_token(env['ACCESS_TOKEN'], env['ACCESS_TOKEN_SECRET'])
        self.api_twitter = tweepy.API(auth)

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
        pass

    def tweet_votacion(self, votid, media_ids):
        # Máximo de caracteres sin link: 256
        link = f'https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion={votid}'
        tweet_text = f'Detalle de la votación: {link}'
        status = self.api_twitter.update_status(status=tweet_text, media_ids=media_ids)
        return status




if __name__ == "__main__":
    bot = Bot()
    bot.run()