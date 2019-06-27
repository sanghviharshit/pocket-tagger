import requests
import logging

from bs4 import BeautifulSoup

from .logger import Log

logger = Log.get_logger(__name__)

class Scraper:
    def get_webpage_content(self, url):
        title = ''
        description = ''
        text = ''

        # Make the request and check object type
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (sanghviharshit/Auto Pocket tagger) Chrome/18 Safari/535.19'})
        # Extract HTML from Response object
        html = r.text
        # Create a BeautifulSoup object from the HTML
        soup = BeautifulSoup(html, 'html5lib')

        # Get title and description
        try:
            if soup.title:
                title = soup.title.get_text()
            elif soup.h1:
                title = soup.h1.get_text()
            logger.info('         Title: {}'.format(title))

            meta = soup.find('meta', attrs={'name': 'description'})
            for tag, value in meta.attrs.items():
                if tag == 'content':
                    description = value
                    break
            if not description:
                if soup.h2:
                    description = soup.h2.get_text()

            logger.info('         Description: {}'.format(description))

        except Exception as e:
            logger.warning('         ({}) Could not find title/description. {}'.format(url, e))
            pass

        text = self.get_clean_text(soup)

        webpage_content = {
            'title': title,
            'description': description,
            'text': text
        }
        return webpage_content

    def get_clean_text(self, soup):
        # kill all script and style elements
        for script in soup(['script', 'style']):
            script.decompose()    # rip it out

        # get body text
        text_body = soup.body.get_text()
        # break into lines and remove leading and trailing space on each
        text_lines = (line.strip() for line in text_body.splitlines())
        # break multi-headlines into a line each
        text_chunks = (phrase.strip() for line in text_lines for phrase in line.split('  '))
        # drop blank lines
        clean_text = '\n'.join(chunk for chunk in text_chunks if chunk)
        return clean_text
