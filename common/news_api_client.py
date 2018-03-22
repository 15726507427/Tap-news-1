import requests

from json import loads

NEWS_API_ENDPOINTS = 'https://newsapi.org/v1/'
NEWS_API_KEYS = 'fd313653d3cc4f9e87cf24ba5afa7150'

ARTICLES_API = 'articles'

CNN = 'cnn'

DEFAULT_SOURCES = [CNN]
SORT_BY_TOP = 'top'

def _buildUrl(endpoint=NEWS_API_ENDPOINTS, apiName=ARTICLES_API):
    return endpoint + apiName

def getNewsFromSource(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = []
    for source in sources:
        payload = {
            'apiKey': NEWS_API_KEYS,
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