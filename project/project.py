
#bots
import random
import cv2
from io import BytesIO
import requests
import tweepy
from PIL import ImageOps
from PIL import Image
from PIL import ImageFile
from secrets import *

ImageFile.LOAD_TRUNCATED_IMAGES = True
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)

def tweet_image(url,username,status_id):
    filename = 'temp.png'
    request = requests.get(url,stream = True)
    if request.status_code == 200:
        i = Image.open(BytesIO(request.content))
        i.save(filename)
       # scramble(filename)
        reversecolor(filename)
        api.update_with_media('scramble.png',status='@{0}'.format(username),in_reply_to_status=status_id)
    else:
        print("unable to download image")

def reversecolor(filename):
    image=Image.open(filename)
    result=ImageOps.invert(image)
    result.save('scramble.png')
"""        
def scramble(filename):
    BLOCKLEN = 64
    img = Image.open(filename)
    width,height = img.size
    xblock = width//BLOCKLEN
    yblock = height//BLOCKLEN
    blockmap = [(xb*BLOCKLEN,yb*BLOCKLEN,(xb+1)*BLOCKLEN,(yb+1)*BLOCKLEN)
               for xb in range(xblock) for yb in range(yblock)]
    ls=list(blockmap)
    ls.reverse()
     #shuffle = list(blockmap)
     #random.shuffle(shuffle)
    result = Image.new(img.mode,(width,height))
    for box, sbox in zip(blockmap,ls):
        crop = img.crop(sbox)
        result.paste(crop,box)
    result.save('scramble.png')
"""
class BotStreamer(tweepy.StreamListener):
    def on_status(self,status):
        username = status.user.screen_name
        status_id = status.id
        
        if 'media' in status.entities:
            for image in status.entities['media']:
                tweet_image(image['media_url'],username,status_id)
myStreamListener = BotStreamer()
stream = tweepy.Stream(auth,myStreamListener)
stream.filter(track=['@jlwPythonProject'])
