#!/usr/bin/env python
import tweepy
import json
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
 
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
access_token = 'access_token'
access_secret = 'access_secret'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

class MyListener(StreamListener):

    def __init__(self, api=None):
        super(MyListener, self).__init__()
        self.num_tweets = 0
 
    def on_data(self, data):
        try:
            with open('pokemon.json', 'a') as f:
                f.write(data)
            self.num_tweets += 1
            if self.num_tweets < 10:
                return True
            else:
                return False
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return True

    def on_error(self, status):
        print(status)
        return True


if __name__ == "__main__":
    twitter_stream = Stream(auth, MyListener())
    twitter_stream.filter(track=['#pokemongo'])





    