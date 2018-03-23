import requests
import yaml

from json import loads

stream = open("../config.yaml", "r")
load = yaml.load(stream)
config = load['common']['news_api']

NEWS_API_ENDPOINTS = config['NEWS_API_ENDPOINTS']
NEWS_API_KEY = config['NEWS_API_KEY']

ARTICLES_API = config['ARTICLES_API']


DEFAULT_SOURCES = config['DEFAULT_SOURCES']
SORT_BY_TOP = config['SORT_BY_TOP']

def _buildUrl(endpoint=NEWS_API_ENDPOINTS, apiName=ARTICLES_API):
    return endpoint + apiName

def getNewsFromSource(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = []
    for source in sources:
        payload = {
            'apiKey': NEWS_API_KEY,
            'source': source,
            'sortBy': sortBy
        }

        response = requests.get(_buildUrl(), params=payload)
        res_json = loads(response.content.decode('utf-8'))

        print(res_json)
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])

    return articles