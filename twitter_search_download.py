'''
Extension of the twitter_stream_download to include older tweets that can still be accessed by the API
'''
import tweepy
from tweepy import OAuthHandler
#from TwitterSearch import *
import time
import argparse
import string
import config
import json
import os

#below copied from twitter_search_download
parser = argparse.ArgumentParser(description="Twitter Downloader")
parser.add_argument("-q",
                    "--query",
                    dest="query",
                    help="Query/Filter",
                    default='-')
parser.add_argument("-d",
                    "--data-dir",
                    dest="data_dir",
                    help="Output/Data Directory")
parser.add_argument("-n",
                    "--number",
                    dest="num",
                    help="Output/Data Directory")


args = parser.parse_args()
auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)
api = tweepy.API(auth)

query = args.query
max_tweets = int(args.num)

#twitter API only returns max 100 tweets at a time, defaults to 15
#stack overflow solution:
#https://stackoverflow.com/questions/22469713/managing-tweepy-api-search
searched_tweets = []
last_id = -1
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query, count=count, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break 

fname = 'search_' + query + '.json'
data = args.data_dir
fpath = os.path.join(data,fname)

 
for tweet in searched_tweets:
    with open(fpath, 'a') as f:
        f.write(json.dumps(tweet._json))
        f.write('\n') 






