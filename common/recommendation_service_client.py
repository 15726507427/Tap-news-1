import jsonrpclib
import yaml

stream = open('../config.yaml', 'r')
load = yaml.load(stream)
config = load['common']

# news recommendation server hosted on port 5050
URL = config['news_recommendation_server']['URL']

client = jsonrpclib.ServerProxy(URL)

def getPreferenceForUser(userId):
    preference = client.getPreferenceForUser(userId)
    print("Preference list: %s" % str(preference))
    return preference