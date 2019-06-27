import json
import time
import random
import logging

from .pocket_api_client import PocketAPIClient
from .scraper import Scraper
from .language_service_client import LanguageServiceClient
from .logger import Log

logger = Log.get_logger(__name__)

class PocketTaggerException(Exception):
    pass

class PocketTagger:
    pocket_client = None

    def __init__(self, consumer_key=None, access_token=None, gcloud_credentials_file=None):
        if consumer_key != None and access_token != None:
            self.pocket_client = self.get_pocket_client(consumer_key, access_token)
        self.scraper = Scraper()
        self.language_service_client = LanguageServiceClient(gcloud_credentials_file)

    def get_pocket_client(self, consumer_key=None, access_token=None):
        if self.pocket_client:
            return self.pocket_client
        elif consumer_key is None or access_token is None:
            raise PocketTaggerException
        else:
            return PocketAPIClient(consumer_key, access_token)

    def get_articles_from_api(self, *args, **kwargs):
        return self.get_pocket_client().get_articles_data(*args, **kwargs)

    def add_tags_to_articles(self, articles_with_tags):
        self.get_pocket_client().add_tags_to_articles(articles_with_tags)

    def get_articles_from_file(self, fileName):
        try:
            with open(fileName, 'r') as infile:
                articles = json.load(infile)
                return articles
        except Exception as e:
            logger.error('({}) {}'.format(fileName, e))
            return {}

    def save_articles_to_file(self, file_name, articles):
      with open(file_name, 'w') as file_name:
          json.dump(articles, file_name)

    def get_tags_for_articles(self, articles, *args, **kwargs):
        urls = []
        index = 1

        total_articles = len(articles.items())
        if total_articles == 0:
            logger.warning('No articles fetched from Pocket')

        for id, data in articles.items():
            url = data['given_url']
            tags = []

            try:
                logger.info('({}/{}) {}'.format(index, total_articles, url))
                webpage_content = self.scraper.get_webpage_content(url)
                if webpage_content:
                    tags = self.language_service_client.get_tags_from_webpage_content(webpage_content, *args, **kwargs)
            except Exception as e:
                logger.error('         ({}) {}'.format(url, e))

            if tags:
                logger.info('         Tags: {}'.format(', '.join(tags)))
            else:
                logger.warning('         ({}) No Tags found'.format(url))
            data['tags'] = tags
            index += 1
            # time.sleep(5)

        return articles
