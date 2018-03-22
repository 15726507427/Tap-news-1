import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client as modeling_client

# modeling classes of all news in mongodb
if __name__ == "__main__":
    db = mongodb_client.get_db()
    cursor = db['news'].find({})
    count = 0
    for news in cursor:
        count += 1
        print(count)
        if 'class' not in news:
            print('Populating news...')
            description = news['description']
            if description is None:
                description = news['title']
            topic = modeling_client.classify(description)
            news['class'] = topic
            db['news'].replace_one({'digest': news['digest']}, news, upsert=True)