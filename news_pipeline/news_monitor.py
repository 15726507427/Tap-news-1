import datetime
import hashlib
import redis
import os
import sys
import yaml

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient

stream = open('../config.yaml', 'r')
load = yaml.load(stream)
config = load['common']

config_cloudAMQP = config['cloudAMQP']

SCRAPE_NEWS_TASK_QUEUE_URL = config_cloudAMQP['SCRAPE_NEWS_TASK_QUEUE_URL']
SCRAPE_NEWS_TASK_QUEUE_NAME = config_cloudAMQP['SCRAPE_NEWS_TASK_QUEUE_NAME']

SLEEP_TIME_IN_SECONDS = config_cloudAMQP['MONITOR_SLEEP_TIME_IN_SECONDS']
NEWS_TIME_OUT_IN_SECONDS = config_cloudAMQP['NEWS_TIME_OUT_IN_DAYS'] * 3600 * 24

# redis-server at default port
REDIS_HOST = config['redis']['HOST']
REDIS_PORT = config['redis']['PORT']

# NEWS_SOURCES = []

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def run():
    while True:
        news_list = news_api_client.getNewsFromSource()     # Use default news sources in config file

        num_of_news = 0

        for news in news_list:
            news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()

            if redis_client.get(news_digest) is None:
                num_of_news += 1
                news['digest'] = news_digest

                if news['publishedAt'] is None:
                    news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

                redis_client.set(news_digest, True)
                redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

                cloudAMQP_client.sendMessage(news)

        print("Fetched %d news." % num_of_news)

        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    run()