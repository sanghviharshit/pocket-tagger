import datetime
today = datetime.date.today()

from pocket_tagger.pocket_tagger import PocketTagger

def tag_em():
    try:
        # Google Cloud - Enable Natural Language Processing API for a project, and get your service account API key.
        # Save it as gcloud_credentials_file.json

        # Pocket API - Create a credentials.py file with the following lines
        '''
        pocket_credentials = {
            'consumer_key': 'your-consumer-key',
            'access_token': 'your-access-token'
        }
        '''
        from credentials import pocket_credentials

        tagger = PocketTagger(gcloud_credentials_file='gcloud_credentials_file.json',
                        consumer_key=pocket_credentials.get('consumer_key'),
                        access_token=pocket_credentials.get('access_token'))

        # For list of optional parameters the API supports - https://getpocket.com/developer/docs/v3/retrieve
        articles = tagger.get_articles_from_api(count=10, offset=10, detailType='complete')
        # Alternatively you can load the articles from file if you saved them previously using save_articles_to_file
        # articles = tagger.get_articles_from_file('20190621.json')

        # Generate tags for each article
        articles_with_tags = tagger.get_tags_for_articles(articles)

        # Save the articles with tags to file
        tagger.save_articles_to_file(today.strftime('%Y%m%d-with-tags.json'), articles_with_tags)

        # You can skip this step if you want to do a dry run. Verify the tags in the file we generated in the previous step.
        tagger.add_tags_to_articles(articles_with_tags)

    except Exception as e:
        print(e)

tag_em()
