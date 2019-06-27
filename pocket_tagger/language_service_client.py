import sys
import os
import math
import logging

from google.cloud import language

from .logger import Log

logger = Log.get_logger(__name__)

class LanguageServiceClient:

    entity_salience_threshold = 0.7
    category_confidence_threshold = 0.3

    def __init__(self, crendentials_file=None):
        if crendentials_file:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = crendentials_file

        # Initialize google cloud language service client
        self.client = language.LanguageServiceClient()

    def get_tags_from_webpage_content(self, webpage_content, thresholds={}):
        if thresholds.get('entity_salience_threshold'):
            self.entity_salience_threshold = kwargs.get('entity_salience_threshold')
        if thresholds.get('category_confidence_threshold'):
            self.category_confidence_threshold = kwargs.get('category_confidence_threshold')

        entities = []
        entities = self.get_entities_from_content(webpage_content)
        categories = self.get_categories_from_content(webpage_content)
        return list(dict.fromkeys(entities + categories))  # Remove Duplicates

    def get_categories_from_content(self, webpage_content):
        categories = []
        doc_content = '. '.join([webpage_content['title'], webpage_content['description'], webpage_content['text']])
        if sys.getsizeof(doc_content) > 128000:
            max_len = len(doc_content)*128000/sys.getsizeof(doc_content)
            doc_content = doc_content[:math.floor(max_len)]

        document = language.types.Document(
            content = doc_content,
            # language='en',
            type=language.enums.Document.Type.PLAIN_TEXT,
            # type=language.enums.Document.Type.HTML,
            )

        response = self.client.classify_text(document)

        response_categories = response.categories
        logger.debug('         Categories: ')
        for category in response_categories:
            addCategory = False
            if category.confidence > self.category_confidence_threshold:
                addCategory = True
                labels = [label for label in category.name.split('/') if label]
                categories = categories + labels
            logger.debug('            {} {}: {}'.format('X' if not addCategory else ' ', category.name, category.confidence))
        return categories

    def get_entities_from_content(self, webpage_content):
        entities = []
        document = language.types.Document(
            content = '. '.join([webpage_content['title'], webpage_content['description']]),
            # language='en',
            type=language.enums.Document.Type.PLAIN_TEXT,
            )
        response = self.client.analyze_entities(
            document=document,
            encoding_type='UTF32',
            )

        logger.debug('         Entities: ')
        for entity in response.entities:
            addEntity = False
            if entity.salience > self.entity_salience_threshold:
                addEntity = True
                entities.append(entity.name.title())
            logger.debug('            {} {}: {}'.format('X' if not addEntity else ' ', entity.name.title(), entity.salience))
        return entities
