# Auto Pocket Tagger

Use Google cloud's Natural Language Processing API to automatically analyze the webpage from articles saved in your Pocket list, derive tags/keywords based on the content of the page, and add tags to the articles in Pocket list for free.

> Pocket has suggested tags service for their paid premium plans. You can find more about it [here](https://help.getpocket.com/article/906-pocket-premium-suggested-tags). This still requires manual work of adding the tags to each article one-by-one. This package automates all of it for free.

## Features
- Uses [Python wrapper](https://github.com/tapanpandita/pocket) for [Pocket API](http://getpocket.com/api/docs) to retrieve articles in the `My List`
- Uses [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) to scrape webpages
- Uses Google Cloud's [Natural Language Processing API](https://cloud.google.com/natural-language/) to generate list of categories and entities from the content of the webpage
- Uses Pocket API to add tags to articles in your `My List`


## Usage

### Installation

#### Install published version from pypi
```shell
$ pip install pocket-tagger
```

#### Install latest version from git
```shell
$ pip install git+https://github.com/sanghviharshit/pocket-tagger
```


### Prerequisites
#### [Google Cloud](https://cloud.google.com/natural-language/docs/quickstart)

This package relies on Google cloud natural language processing API, which requires billing enabled on your project.
You can find the quickstart instructions [here](https://cloud.google.com/natural-language/docs/quickstart)
**Options:**
1. Create a service account and download the credentials file - https://cloud.google.com/video-intelligence/docs/common/auth
```python
tagger = PocketTagger(gcloud_credentials_file="gcloud_credentials_file.json")
```
2. or Configure gloud locally - https://cloud.google.com/sdk/gcloud/reference/init
```python
tagger = PocketTagger()
```

#### [Pocket API](https://getpocket.com/developer/)

To fetch the articles list and add tags, you need a developer key from [here](https://getpocket.com/developer/)
Create a new Application with `modify` and `retrieve` permissions. Save the Consumer Key and Access Token.
```python
tagger = PocketTagger(consumer_key='your-consumer-key',
                access_token='your-access-token')
```

### [Examples](./examples)

```python
# Initialize PocketTagger with GCloud and Pocket API Credentials
tagger = PocketTagger(gcloud_credentials_file="gcloud_credentials_file.json",
                consumer_key='pocket-consumer-key',
                access_token='pocket-access-token')

# Check https://getpocket.com/developer/docs/v3/retrieve for additional list of options you can pass for retrieving pocket list
articles = tagger.get_articles_from_api(count=10, offset=10, detailType='complete')

# Alternatively you can load the articles from file if you saved them previously using save_articles_to_file
# articles = tagger.get_articles_from_file("20190621.json")
# Generate tags for each article
articles_with_tags = tagger.get_tags_for_articles(articles)

# Save the articles with tags to file. You can use this file to verify it looks good before running the final step to tag the articles.
tagger.save_articles_to_file(today.strftime('%Y%m%d-with-tags.json'), articles_with_tags)

# You can skip this step if you want to do a dry run. Verify the tags in the file we generated in the previous step.
tagger.add_tags_to_articles(articles_with_tags)
```

### Optional overrides
You can override the default thresholds for [entity](https://cloud.google.com/natural-language/docs/reference/rest/v1/Entity
) salience and [category](https://cloud.google.com/natural-language/docs/reference/rest/v1/ClassificationCategory) confidence

```python
thresholds = {
  'entity_salience_threshold': 0.7
  'category_confidence_threshold': 0.3
}
articles_with_tags = tagger.get_tags_for_articles(articles, thresholds)
```

## Sample

Sample output from running it for my 490 items long Pocket list
> `X` under Entities or Categories denotes the NLP client returned those as potential candidates, but we skipped them because it didn't meet the threshold. You can see the last line `Tags: abc, xyz` for list of tags pocket-tagger added for each URL.

```
(1/490) https://www.reddit.com/r/explainlikeimfive/comments/bvweym/eli5_why_do_coffee_drinkers_feel_more_clear/?utm_source=share&utm_medium=ios_app
         Title: ELI5: Why do coffee drinkers feel more clear headed after consuming caffeine? Why do some get a headache without it? Does caffeine cause any permanent brain changes and can the brain go back to 'normal' after years of caffeine use? : explainlikeimfive
         Description: r/explainlikeimfive: **Explain Like I'm Five is the best forum and archive on the internet for layperson-friendly explanations.** &nbsp; Don't Panic!
         Entities:
            X Coffee Drinkers: 0.2438652664422989
            X Eli5: 0.14941969513893127
            X Caffeine: 0.12065556645393372
            X Caffeine: 0.0874909833073616
            X Some: 0.06917785853147507
            X Headache: 0.0606028214097023
            X Brain: 0.03606536239385605
            X Explainlikeimfive: 0.033727116882801056
            X Brain Changes: 0.03211209550499916
            X Caffeine Use: 0.029848895967006683
            X R: 0.02966366335749626
            X Forum: 0.028598546981811523
            X Internet: 0.022404097020626068
            X Archive: 0.022404097020626068
            X Explainlikeimfive: 0.017647551372647285
            X Don'T Panic: 0.009302889928221703
            X Five: 0.007013489492237568
            X Five: 0.0
         Categories:
              /Food & Drink/Beverages/Coffee & Tea: 0.6700000166893005
         Tags: Food & Drink, Beverages, Coffee & Tea
(2/490) https://www.reddit.com/r/television/comments/bnpwe3/enjoy_three_full_minutes_of_the_cast_of_game_of/?utm_source=share&utm_medium=ios_app
         Title: Enjoy three full minutes of the cast of 'Game of Thrones' expressing disappointment in Season 8. : television
         Description: r/television:
         Entities:
            X Cast: 0.31218624114990234
            X Disappointment: 0.20341947674751282
            X Season: 0.20341947674751282
            X Game Of Thrones: 0.13265934586524963
            X Television: 0.08712445199489594
            X Television: 0.06119102984666824
            X 8: 0.0
            X Three: 0.0
         Categories:
              /Arts & Entertainment/TV & Video/TV Shows & Programs: 0.75
         Tags: Arts & Entertainment, TV & Video, TV Shows & Programs
(3/490) https://www.reddit.com/r/homeautomation/comments/awvf5r/local_realtime_person_detection_for_rtsp_cameras/
         Title: Local realtime person detection for RTSP cameras : homeautomation
         Description: r/homeautomation: A subreddit focused on automating your home, housework or household activity. Sensors, switches, cameras, locks, etc. Any …
         Entities:
            X Realtime Person Detection: 0.3057926297187805
            X Homeautomation: 0.15315502882003784
            X Cameras: 0.14035314321517944
            X Rtsp: 0.07461880147457123
            X Homeautomation: 0.051411159336566925
            X Home: 0.047811269760131836
            X Housework: 0.04366889223456383
            X Subreddit: 0.04183248057961464
            X R: 0.04132793843746185
            X Cameras: 0.032860007137060165
            X Locks: 0.028899790719151497
            X Household Activity: 0.012798599898815155
            X Switches: 0.012735127471387386
            X Sensors: 0.012735127471387386
         Categories:
              /Computers & Electronics: 0.7900000214576721
         Tags: Computers & Electronics
```

## References
- [Pocket API Wrapper for Python](https://github.com/tapanpandita/pocket)
- [Pocket API Docs](http://getpocket.com/api/docs)
- [Google Cloud Natural Language Processing](https://cloud.google.com/natural-language/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [Complete list of content categories from Google Natural Language API](https://cloud.google.com/natural-language/docs/categories)

## Analytics
[![Analytics](https://ga-beacon.appspot.com/UA-59542024-4/pocket-tagger/)](https://github.com/igrigorik/ga-beacon)
