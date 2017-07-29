
# coding: utf-8

# In[1]:

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json


# In[2]:

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)
api = tweepy.API(auth)


# In[3]:

query = '#watvwex'
max_tweets = 1000


# In[15]:

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


# In[16]:

len(searched_tweets)


# In[18]:

ids = []


# In[19]:

for tweet in searched_tweets:
    ids.append(tweet.id)


# In[20]:

len(ids)


# In[24]:

for tweet in searched_tweets:
    with open('test.json', 'a') as f:
        f.write(json.dumps(tweet._json))
        f.write('\n')


# In[ ]:



