# Queue helper: clear all messages in scrape and dedupe queues. Test purpose only

import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

SCRAPE_NEWS_TASK_QUEUE_URL = 'amqp://nifchscl:vSSrLMljckfH22yVWZu3oAMHyAoLcuM-@otter.rmq.cloudamqp.com/nifchscl'
SCRAPE_NEWS_TASK_QUEUE_NAME = 'tap-news-monitor'

DEDUPE_NEWS_TASK_QUEUE_URL = 'amqp://mctuftbf:9PdbLbIsbJ1bRXpwWiF-s2tYmvLnf14l@mosquito.rmq.cloudamqp.com/mctuftbf'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'tap-news-deduper'

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
