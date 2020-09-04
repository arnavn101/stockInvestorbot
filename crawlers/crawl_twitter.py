from tweepy import OAuthHandler
import configparser
import os
import re
import sys
import tweepy
sys.path.insert(0, os.getcwd())  # Resolve Importing errors


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


class CrawlTweets:
    def __init__(self, stock_name, number_tweets):
        # Get Twitter API Information
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join("config_files", "auth.cfg"))

        # create OAuthHandler object 
        self.auth = OAuthHandler(self.config.get('Twitter', 'consumer_key'),
                                 self.config.get('Twitter', 'consumer_secret'))
        # set access token and secret 
        self.auth.set_access_token(self.config.get('Twitter', 'account_key'),
                                   self.config.get('Twitter', 'account_secret'))
        # create API object to fetch tweets
        self.api = tweepy.API(self.auth)

        # Set variables and execute tweet retrieval
        self.tweets = []
        self.stock_name = stock_name
        self.number_tweets = number_tweets
        self.get_tweets(stock_name, number_tweets)

    def get_tweets(self, query, count=10):
        fetched_tweets = self.api.search(q=query, count=count, lang="en")
        for tweet in fetched_tweets:
            text_tweet = clean_tweet(tweet.text)
            if tweet.retweet_count > 0:
                if text_tweet not in self.tweets:
                    self.tweets.append(text_tweet)
            else:
                self.tweets.append(text_tweet)

    def return_tweets(self):
        return self.tweets
