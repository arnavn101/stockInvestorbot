import os
import pickle
import requests
import statistics
import sys
import warnings
sys.path.insert(0, os.getcwd())  # Resolve Importing errors
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from crawlers.retrieveArticles import RetrieveArticles
from colorama import Fore, init
from crawlers.crawl_reddit import CrawlSubReddit
from crawlers.crawl_twitter import CrawlTweets
import itertools
import nltk

# TODO --> store sentiment values in a 2D array

# Download requirements & filter valid warnings
warnings.filterwarnings('ignore')
# nltk.download('vader_lexicon')

# colors
init(convert=True)
BLUE = Fore.BLUE
GRAY = Fore.LIGHTBLACK_EX
YELLOW = Fore.YELLOW
MAGENTA = Fore.MAGENTA
RESET = Fore.RESET


class retrieve_Sentiments():
    def __init__(self, stock_name, articlePerWebsite):
        self.stock_name = stock_name
        self.articlePerWebsite = articlePerWebsite
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.date_sentiments = []
        self.specific_date_sentiment = []
        self.socialMedia_sentiments = {"Twitter": [], "Reddit": []}
        self.list_finalSentiments = []
        self.main_execution()

    def main_execution(self):

        self.articlesFetcher = RetrieveArticles(self.stock_name, self.articlePerWebsite)
        self.gather_articleSentiments(self.articlesFetcher.return_articleSentences())
        self.retrieveMain_sentiment()
        if len(self.specific_date_sentiment) != 0:
            self.list_finalSentiments.append(self.specific_date_sentiment[0])
        print(f"{GRAY}Articles Sentiment : {RESET}", f"{BLUE}{((self.specific_date_sentiment))}{RESET}")

        self.sentiments_socialMedia()
        for social_mediaPlatform in self.return_dictKeys(self.socialMedia_sentiments):
            specific_mediaSentiment = self.socialMedia_sentiments[social_mediaPlatform]
            if len(specific_mediaSentiment) > 0:
                social_mediaSentiment = self.round_sentiment(self.return_meanArray(specific_mediaSentiment))
                self.list_finalSentiments.append(social_mediaSentiment)
                print(f"{GRAY}{social_mediaPlatform.lower()}{RESET}", f"{BLUE}{social_mediaSentiment}{RESET}")
        finale_sentiment = self.round_sentiment(self.return_final_sentiment())
        print(f"{MAGENTA}Average Sentiment : {RESET}{YELLOW}{finale_sentiment}{RESET}")
        self.save_sentiment(finale_sentiment)

    def return_dictKeys(self, dict_object):
        return [*dict_object]

    def save_sentiment(self, sentiment_value):
        # Open pickle files to read variables
        load_variables = open(os.path.join('storage_dir', 'saved_sentiments.pkl'), 'rb')

        # Keep track of variables
        previous_sentiments = pickle.load(load_variables)

        # Close the pickle file
        load_variables.close()

        # Open the pickle file for writing variables
        save_variables = open(os.path.join('storage_dir', 'saved_sentiments.pkl'), 'wb')

        # Change previous_sentiments
        previous_sentiments[self.stock_name.lower()] = sentiment_value

        # Save variables for next day
        pickle.dump(previous_sentiments, save_variables)

    def round_sentiment(self, sentiment_value):
        return round(sentiment_value, 3)

    @staticmethod
    def retrieve_stockSymbol(stock_name):
        URL_API = f"http://d.yimg.com/autoc.finance.yahoo.com/autoc"
        PARAMS = {'query': stock_name, 'region': 1, 'lang': 'en'}
        get_request = requests.get(url=URL_API, params=PARAMS)

        # extracting data in json format 
        stockData_json = get_request.json()
        length_response = len(list(stockData_json["ResultSet"]["Result"]))

        if length_response != 0:
            return str(stockData_json["ResultSet"]["Result"][0]["symbol"])
        return ""

    def return_final_sentiment(self):
        if len(self.list_finalSentiments) != 0:
            return self.return_meanArray(self.list_finalSentiments)
        return 0

    def return_meanArray(self, arrayInput):
        return statistics.mean(arrayInput)

    def flatten_array(self, array_list):
        return list(itertools.chain.from_iterable(array_list))

    def return_dictValues(self, dict_object):
        return list(dict_object.values())

    def return_sentiments(self, bodyText, socialMedia=False):
        sentiment_score = self.sentiment_analyzer.polarity_scores(bodyText)['compound']
        if not socialMedia:
            self.date_sentiments.append(sentiment_score)
        else:
            self.socialMedia_sentiments[socialMedia].append(sentiment_score)

    def retrieveMain_sentiment(self):
        if len(self.date_sentiments) != 0:
            self.specific_date_sentiment.append(round(sum(self.date_sentiments) / float(len(self.date_sentiments)), 3))

    @staticmethod
    def retrieve_contentsFile(filename):
        return [line.rstrip() for line in open(filename)]

    def retrieve_subredditPosts(self):
        list_subreddits = retrieve_Sentiments.retrieve_contentsFile(os.path.join("config_files", "subreddits_list.txt"))
        list_posts = []
        for subreddit in list_subreddits:
            reddit_crawler = CrawlSubReddit(str(subreddit), self.stock_name,
                                            retrieve_Sentiments.retrieve_stockSymbol(self.stock_name), 5)
            list_posts.append(reddit_crawler.return_listSentences())
        return self.flatten_array(list_posts)

    def retrieve_twitterTweets(self):
        twitter_crawler = CrawlTweets(self.stock_name, 10)
        return twitter_crawler.return_tweets()

    def sentiments_socialMedia(self):
        reddit_post_list = []
        twitter_tweet_list = []
        reddit_post_list.append(self.retrieve_subredditPosts())
        twitter_tweet_list.append(self.retrieve_twitterTweets())
        final_redditList = self.flatten_array(reddit_post_list)
        final_twitterList = self.flatten_array(twitter_tweet_list)

        for individual_post in final_redditList:
            self.return_sentiments(individual_post, socialMedia="Reddit")
        for individual_tweet in final_twitterList:
            self.return_sentiments(individual_tweet, socialMedia="Twitter")

    def gather_articleSentiments(self, listSentences):
        # Account for empty file
        if len(listSentences) == 0:
            pass
        else:
            for individual_sentence in listSentences:
                self.return_sentiments(individual_sentence)
