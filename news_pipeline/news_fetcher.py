import os
import sys
import yaml

from newspaper import Article

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

stream = open('../config.yaml', 'r')
load = yaml.load(stream)
config = load['common']['cloudAMQP']

SCRAPE_NEWS_TASK_QUEUE_URL = config['SCRAPE_NEWS_TASK_QUEUE_URL']
SCRAPE_NEWS_TASK_QUEUE_NAME = config['SCRAPE_NEWS_TASK_QUEUE_NAME']

DEDUPE_NEWS_TASK_QUEUE_URL = config['DEDUPE_NEWS_TASK_QUEUE_URL']
DEDUPE_NEWS_TASK_QUEUE_NAME = config['DEDUPE_NEWS_TASK_QUEUE_NAME']

SLEEP_TIME_IN_SECONDS = config['FETCHER_SLEEP_TIME_IN_SECONDS']

scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print("message is broken")
        return

    task = msg
    text = None

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text
    dedupe_news_queue_client.sendMessage(task)

while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:

            try:
                handle_message(msg)
            except Exception as e:
                print(e)
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)