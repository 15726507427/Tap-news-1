import operator
import os
import sys
import yaml

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

stream = open('../config.yaml', 'r')
load = yaml.load(stream)
config = load['common']

# news recommendation server hosted on port 5050
SERVER_HOST = config['news_recommendation_server']['SERVER_HOST']
SERVER_PORT = config['news_recommendation_server']['SERVER_PORT']

PREFERENCE_MODEL_TABLE_NAME = config['mongodb']['PREFERENCE_MODEL_TABLE_NAME']

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def getPreferenceForUser(user_id):
    """ Get user's preference in an ordered class list """
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': user_id})

    if model is None:
        return []

    sorted_tuples = sorted(list(model['preference'].items()), key=operator.itemgetter(1), reverse=True)
    sorted_list = [x[0] for x in sorted_tuples]
    sorted_value_list = [x[1] for x in sorted_tuples]

    if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
        return []

    return sorted_list

# Treading HTTP server

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(getPreferenceForUser, 'getPreferenceForUser')

print("Starting HTTP Server on %s:%d" % (SERVER_HOST, SERVER_PORT))

RPC_SERVER.serve_forever()