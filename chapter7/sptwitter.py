"""
Get status on Twitter

df = stats_df(user="KingJames")
In [34]: df.describe()
Out[34]: 
       favorite_count  retweet_count
count      200.000000     200.000000
mean     11680.670000    4970.585000
std      20694.982228    9230.301069
min          0.000000      39.000000
25%       1589.500000     419.750000
50%       4659.500000    1157.500000
75%      13217.750000    4881.000000
max     128614.000000   70601.000000

In [35]: df.corr()
Out[35]: 
                favorite_count  retweet_count
favorite_count        1.000000       0.904623
retweet_count         0.904623       1.000000

"""

import time

import twitter
from . import config
import pandas as pd
import numpy as np
from twitter.error import TwitterError

def api_handler():
    """Creates connection to Twitter API"""
    
    api = twitter.Api(consumer_key=config.CONSUMER_KEY,
    consumer_secret=config.CONSUMER_SECRET,
    access_token_key=config.ACCESS_TOKEN_KEY,
    access_token_secret=config.ACCESS_TOKEN_SECRET)
    return api

def tweets_by_user(api, user, count=200):
    """Grabs the "n" number of tweets.  Defaults to 200"""

    tweets = api.GetUserTimeline(screen_name=user, count=count)
    return tweets

def stats_to_df(tweets):
    """Takes twitter stats and converts them to a dataframe"""

    records = []
    for tweet in tweets:
        records.append({"created_at":tweet.created_at,
            "screen_name":tweet.user.screen_name, 
            "retweet_count":tweet.retweet_count,
            "favorite_count":tweet.favorite_count})
    df = pd.DataFrame(data=records)
    return df

def stats_df(user):
    """Returns a dataframe of stats"""

    api = api_handler()
    tweets = tweets_by_user(api, user)
    df = stats_to_df(tweets)
    return df

def twitter_handles(sleep=.5,data="data/twitter_nba_combined.csv"):
    """yield handles"""

    nba = pd.read_csv(data) 
    for handle in nba["twitter_handle"]:
        time.sleep(sleep) #Avoid throttling in twitter api
        try:
            df = stats_df(handle)
        except TwitterError as error:
            print("Error {handle} and error msg {error}".format(
                handle=handle,error=error))
            df = None
        yield df

def median_engagement(data="data/twitter_nba_combined.csv"):
    """Median engagement on twitter"""

    favorite_count = []
    retweet_count = []
    nba = pd.read_csv(data)
    for record in twitter_handles(data=data):
        print(record)
        #None records stored as Nan value
        if record is None:
            print("NO RECORD: {record}".format(record=record))
            favorite_count.append(np.nan)
            retweet_count.append(np.nan)
            continue
        try:
            favorite_count.append(record['favorite_count'].median())
            retweet_count.append(record["retweet_count"].median())
        except KeyError as error:
            print("No values found to append {error}".format(error=error))
            favorite_count.append(np.nan)
            retweet_count.append(np.nan)
        
    print("Creating DF")
    nba['twitter_favorite_count'] = favorite_count
    nba['twitter_retweet_count'] = retweet_count
    return nba

def create_twitter_csv(data="data/nba_2016_2017_wikipedia.csv"):
    nba = median_engagement(data)
    nba.to_csv("data/nba_2016_2017_wikipedia_twitter.csv")
    