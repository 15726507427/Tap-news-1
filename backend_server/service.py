import json
import operations
import yaml

from bson.json_util import dumps
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

stream = open("../config.yaml", "r")
load = yaml.load(stream)
config = load['common']

# Backend RPC Server hosted on port 4040
SERVER_HOST = config['backend_server']['HOST']
SERVER_PORT = config['backend_server']['PORT']

def add(num1, num2):
    print("add is called with %d and %d" % (num1, num2))
    return num1 + num2

def get_one_news():
    print("getOneNews is called...")
    news = operations.getOneNews()
    return json.loads(dumps(news))

def get_news_summaries_for_user(user_id, page_num):
    """ get news summaries for a user """
    print("get_news_summaries_for_user is called with %s and %s" % (user_id, page_num))
    return operations.getNewsSummariesForUser(user_id, page_num)

def log_news_click_for_user(user_id, news_id):
    """ send click news log from a user """
    print("log_news_click_for_user is called with %s and %s" % (user_id, news_id))
    operations.logNewsClickForUser(user_id, news_id)

server = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
server.register_function(add, 'add')
server.register_function(get_one_news, 'getOneNews')
server.register_function(get_news_summaries_for_user, 'getNewsSummariesForUser')
server.register_function(log_news_click_for_user, 'logNewsClickForUser')

print("Starting RPC server on %s:%d" % (SERVER_HOST, SERVER_PORT))
server.serve_forever()