# Queue helper: clear all messages in scrape and dedupe queues. Test purpose only

import os
import sys
import yaml

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

stream = open('../config.yaml', 'r')
load = yaml.load(stream)
config = load['common']['cloudAMQP']

SCRAPE_NEWS_TASK_QUEUE_URL = config['SCRAPE_NEWS_TASK_QUEUE_URL']
SCRAPE_NEWS_TASK_QUEUE_NAME = config['SCRAPE_NEWS_TASK_QUEUE_NAME']

DEDUPE_NEWS_TASK_QUEUE_URL = config['DEDUPE_NEWS_TASK_QUEUE_URL']
DEDUPE_NEWS_TASK_QUEUE_NAME = config['DEDUPE_NEWS_TASK_QUEUE_NAME']

def clearQueue(queue_url, queue_name):
    scrape_news_queue_client = CloudAMQPClient(queue_url, queue_name)

    num_of_messages = 0

    while True:
        if scrape_news_queue_client is not None:
            msg = scrape_news_queue_client.getMessage()
            if msg is None:
                print("Cleared %d messages." % num_of_messages)
                return
            num_of_messages += 1


if __name__ == "__main__":
    clearQueue(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
    clearQueue(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
