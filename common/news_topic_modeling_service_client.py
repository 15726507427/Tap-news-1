import jsonrpclib
import yaml

stream = open('../config.yaml', 'r')
load = yaml.load(stream)
config = load['common']

# modeling service listen on 6060
URL = config['news_topic_modeling_server']['URL']
client = jsonrpclib.ServerProxy(URL)

def classify(text):
    topic = client.classify(text)
    print("Topic: %s" % str(topic))
    return topic