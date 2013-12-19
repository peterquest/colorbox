import colorDictionary
import random
import sys
import tweepy
from keys import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def get_random_color():
      r = lambda: random.randint(0,2)
      return ('%X%X%X' % (r(),r(),r()))

def give_usage(from_user, tweetID):
    api.update_status("@%s I don't recognize that color! Sorry. See usage." % 
                       from_user, in_reply_to_status_id = tweetID)

def parse_tweet(tweet_text):
    color = tweet_text.split("@peterquest ")[-1].lower()
    return color

def write_to_ledborg(color):
    print "in write to borg"
    LedBorg = open('/dev/ledborg', 'w')
    LedBorg.write(color)
    del LedBorg

def tweet_handler(tweet_text, from_user, tweetID):

    color = parse_tweet(tweet_text)

    if color in colorDictionary.colors:
      rgb = colorDictionary.colors[color] #lol
    else:
      rgb = get_random_color()
      give_usage(from_user, tweetID)

    print rgb
    write_to_ledborg(rgb)
      

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweet_handler(status.text, status.user.screen_name, status.id)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track=['@peterquest'])
