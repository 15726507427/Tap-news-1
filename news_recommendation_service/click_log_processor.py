# -*- coding: utf-8 -*-

"""
Time decay model:

If selected:
p = (1-α)p + α

If not:
p = (1-α)p

Where p is the selection probability, and α is the degree of weight decrease.
The result of this is that the nth most recent selection will have a weight of
(1-α)^n. Using a coefficient value of 0.05 as an example, the 10th most recent
selection would only have half the weight of the most recent. Increasing epsilon
would bias towards more recent results more.
"""

import news_classes
import os
import sys
import yaml

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

stream = open('../config.yaml', 'r')
load = yaml.load(stream)
config = load['common']

NUM_OF_CLASSES = len(news_classes.classes)
INITIAL_P = 1.0 / NUM_OF_CLASSES
# print("num of classes: %d, initial possibility: %f." % (NUM_OF_CLASSES, INITIAL_P))
ALPHA = config['news_recommendation_server']['ALPHA']

SLEEP_TIME_IN_SECONDS = config['cloudAMQP']['CLICK_LOG_SLEEP_TIME_IN_SECONDS']

CLICK_LOG_TASK_QUEUE_URL = config['cloudAMQP']['CLICK_LOG_TASK_QUEUE_URL']
CLICK_LOG_TASK_QUEUE_NAME = config['cloudAMQP']['CLICK_LOG_TASK_QUEUE_NAME']

PREFERENCE_MODEL_TABLE_NAME = config['mongodb']['PREFERENCE_MODEL_TABLE_NAME']
NEWS_TABLE_NAME = config['mongodb']['NEWS_TABLE_NAME']

cloudAMQP_client = CloudAMQPClient(CLICK_LOG_TASK_QUEUE_URL, CLICK_LOG_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return

    if ('userId' not in msg
        or 'newsId' not in msg
        or 'timestamp' not in msg):
        return

    userId = msg['userId']
    newsId = msg['newsId']

    # Update user's preference model
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': userId})

    # If model not exists, create a new one
    if model is None:
        print("Creating preference model for new user: %s" % userId)
        news_model = {'userId': userId}
        preference = {}
        for i in news_classes.classes:
            preference[i] = float(INITIAL_P)
        news_model['preference'] = preference
        model = news_model

    print("Update preference model for user: %s" % userId)

    # Update model using time decay model
    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if (news is None
        or 'class' not in news
        or news['class'] not in news_classes.classes):
        print("Skip processing...")
        return

    # Update the clicked class
    clicked_class = news['class']
    old_p = model['preference'][clicked_class]
    model['preference'][clicked_class] = float((1 - ALPHA) * old_p + ALPHA)

    # Update other non-clicked classes
    for i, prob in model['preference'].items():
        if not i == clicked_class:
            old_p = model['preference'][i]
            model['preference'][i] = float((1 - ALPHA) * old_p)

    print(model)

    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)


def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass

            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == '__main__':
    run()