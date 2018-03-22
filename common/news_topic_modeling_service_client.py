import jsonrpclib

# modeling service listen on 6060

URL = "http://localhost:6060"
client = jsonrpclib.ServerProxy(URL)

def classify(text):
    topic = client.classify(text)
    print("Topic: %s" % str(topic))
    return topic