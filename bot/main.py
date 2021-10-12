import path
import tweepy
from dotenv import dotenv_values

env = dotenv_values(path.this_file()+"/.env")

auth = tweepy.OAuthHandler(env['API_KEY'], env['API_KEY_SECRET'])
auth.set_access_token(env['ACCESS_TOKEN'], env['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)

images = (
    '/Users/fguinez/Documents/Visualizaciones/quevotaron/draw/img/logo.png',
    'draw/img/logo-root1.png',
    'draw/img/logo-root3.png',
    '/Users/fguinez/Documents/Visualizaciones/quevotaron/draw/img/logo-root2.png',
)
media_ids = [api.media_upload(i).media_id_string  for i in images]
tweet_text = ''
status = api.update_status(status=tweet_text, media_ids=media_ids)
#api.update_status(status="Hola mundo")