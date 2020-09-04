from newsapi import NewsApiClient
from textblob import TextBlob
from datetime import datetime
import configparser
import itertools
import nltk
import os
import re
import sys

sys.path.insert(0, os.getcwd())  # Resolve Importing errors


def clean_text(unclean_text):
    unclean_text = re.sub(r'\[.*?\]', '', unclean_text)
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", unclean_text).split())


def flatten_array(array_list):
    return list(itertools.chain.from_iterable(array_list))


class RetrieveArticles:
    def __init__(self, stock_name, number_articles):
        # Get News API Information
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join("config_files", "auth.cfg"))

        self.news_api = NewsApiClient(api_key=self.config.get('NewsAPI', 'api_key'))
        self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.stock_name = stock_name
        self.number_articles = number_articles
        self.article_content = []
        self.sentences = []
        self.main_execution()

    def main_execution(self):
        article_headlines = self.retrieve_articles()
        self.separate_articles(article_headlines)
        for individual_sentence in self.article_content:
            self.sentences.append(self.separate_sentences(individual_sentence))
        self.sentences = flatten_array(self.sentences)

    def retrieve_articles(self):
        current_date = str(datetime.today().strftime('%Y-%m-%d'))
        return self.news_api.get_everything(q=self.stock_name,
                                            from_param=current_date,
                                            to=current_date,
                                            language='en',
                                            sort_by='relevancy'
                                            )

    def separate_articles(self, article_headlines):
        break_number = 0
        for individual_article in article_headlines['articles']:
            if break_number == self.number_articles:
                break
            article_description = individual_article['description']
            article_content = individual_article['content']
            if article_content and article_description and len(article_description) > 3 and TextBlob(
                    article_description).detect_language() == 'en':
                if self.stock_name.lower() in article_content.lower() or self.stock_name.lower() in article_description.lower():
                    self.article_content.append(clean_text(article_description))
                    self.article_content.append(clean_text(article_content))
                    break_number += 1

    def separate_sentences(self, text_article):
        return self.tokenizer.tokenize(text_article)

    def return_articleSentences(self):
        return self.sentences

