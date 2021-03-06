import json, requests

API_KEY = 'uid5124-25733182-80'
URL_PREFIX = 'http://api.shopstyle.com/api/v2'
PRODUCTS = '/products'

def get_batch(key, offset):
  url = URL_PREFIX + PRODUCTS
  url += '?' + 'pid=' + API_KEY
  url += '&' + 'fts=' + key + ' under $250'
  url += '&' + 'offset=' + str(offset)
  url += '&' + 'limit=' + '100'
  print 'Url is', url
  r = requests.get(url)
  return json.loads(r.content)['products']
