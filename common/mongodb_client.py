from pymongo import MongoClient

import yaml

stream = open("../config.yaml", "r")
load = yaml.load(stream)
config = load['common']

MONGO_DB_HOST = config['mongodb']['HOST']
MONGO_DB_PORT = config['mongodb']['PORT']
DB_NAME = config['mongodb']['DB_NAME']

client = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))

def get_db(db=DB_NAME):
    db = client[db]
    return db