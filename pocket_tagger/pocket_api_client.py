import json
import logging

from pocket import Pocket, PocketException

from .logger import Log

logger = Log.get_logger(__name__)

class PocketAPIClient:
    pocket_client = None
    def __init__(self, consumer_key, access_token):
        self.pocket_client = Pocket(consumer_key, access_token)

    def get_articles_data(self, *args, **kwargs):
        # Fetch the articles
        try:
            # For list of optional parameters the API supports - https://getpocket.com/developer/docs/v3/retrieve
            response, headers = self.pocket_client.get(*args, **kwargs)
            return response.get('list')
        except PocketException as e:
            print(e)

    def add_tags_to_articles(self, articles_with_tags, replace=False):
        try:
            total_articles = len(articles_with_tags.items())
            if total_articles == 0:
                return
            pocket_instance = self.pocket_client
            # Start a bulk operation
            for id, data in articles_with_tags.items():
                pocket_instance = pocket_instance.tags_add(id, data['tags'])

            # and commit
            response, headers = self.pocket_client.commit()
            logger.info('Added the tags to articles.')
        except PocketException as e:
            logger.error(e)
