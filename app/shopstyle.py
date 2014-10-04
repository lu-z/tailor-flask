import json, requests

API_KEY = 'uid5124-25733182-80'
URL_PREFIX = 'http://api.shopstyle.com/api/v2'
PRODUCTS = '/products'

current_offset = 0

def get_batch(key, offset=current_offset):
  global current_offset
  url = URL_PREFIX + PRODUCTS
  url += '?' + 'pid=' + API_KEY
  url += '&' + 'fts=' + key
  url += '&' + 'offset=' + str(offset)
  url += '&' + 'limit=' + '100'
  r = requests.get(url)
  current_offset += 100
  return json.loads(r.content)['products']