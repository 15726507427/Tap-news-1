import os
import sys
import json
import pickle
import redis

from bson.json_util import dumps
from datetime import date, datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient
import recommendation_service_client

NEWS_TABLE_NAME = 'news' # table name

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_LIST_BATCH_SIZE = 10 		# number of news in single page
NEWS_LIMIT = 200 		    	# maximum number of news of one fetch from mongoDB
USER_NEWS_TIME_OUT_IN_SECONDS = 60 # timeout for user's pagination info in redis

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)

CLICK_LOG_TASK_QUEUE_URL = 'amqp://uhkguhqy:SFT8Vf9Ln3s7cfs8_ZwErFww8UB3V5RJ@otter.rmq.cloudamqp.com/uhkguhqy'
CLICK_LOG_TASK_QUEUE_NAME = 'news-click-log'

cloudAMQP_client = CloudAMQPClient(CLICK_LOG_TASK_QUEUE_URL, CLICK_LOG_TASK_QUEUE_NAME)

def getOneNews():
    db = mongodb_client.get_db()
    news = db[NEWS_TABLE_NAME].find_one()
    return news

def getNewsSummariesForUser(user_id, page_num):

    page_num = int(page_num)
    # news range to be fetched for the page number
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    # the final list of news to be returned

    sliced_news = []
    db = mongodb_client.get_db()

    if redis_client.get(user_id) is not None:
        # user id already cached in redis, get next paginating data and fetch news
        news_digests = pickle.loads(redis_client.get(user_id))
        # both parameters are inclusive
        sliced_news_digest = news_digests[begin_index:end_index]
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': {'$in': sliced_news_digest}}))
    else:
        # no cached data
        # retrieve news and store their digests list in redis with user id as key
        # retrieve news and sort by publish time in reverse order (latest first)
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digest = [x['digest'] for x in total_news] # lambda function in python

        redis_client.set(user_id, pickle.dumps(total_news_digest))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)
        sliced_news = total_news[begin_index:end_index]

    # Get user preference
    preference = recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None

    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    print('top preference is %s' % topPreference)
    for news in sliced_news:
        # Remove text field to save bandwidth
        del news['text']
        # print(news['publishedAt'])
        if news['publishedAt'].date == date.today():
            # Add time tag to be displayed on page
            news['time'] = 'today'
        if news['class'] == topPreference:
            news['reason'] = topPreference

    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    message = {
        'userId': user_id,
        'newsId': news_id,
        'timestamp': str(datetime.utcnow())
    }

    # Send log task to click log processor through msg queue
    cloudAMQP_client.sendMessage(message)