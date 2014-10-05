from app import shopstyle, classes
from util import SafeDict
import httplib, json, parser, threading

QUERY_SIZE = 10
REQUEST_THRESHOLD = 20
USER_ID = 'i7AfKxW9wG'

current_offset = 0
dresses = []

user_prefs = SafeDict()
initiated = False

def get_batch(t):
  global current_offset, dresses, initiated

  if not initiated:
    db_get_user(USER_ID)
    initiated = True
  if not dresses:
    update_list(t)

  if len(dresses) < REQUEST_THRESHOLD:
    update_thread = threading.Thread(target=update_list, args=[t])
    update_thread.start()

  result, new_dresses = [], [];
  for i in range(0, len(dresses)):
    if len(result) >= QUERY_SIZE:
      break

    dress = dresses[i]
    name = dress['name']
    description = de_htmlize(dress['description'])
    price = dress['priceLabel']
    try:
      brand = dress['brand']['name']
    except KeyError as k:
      new_dresses = dresses[i+1:]
      continue
    categories = [category['shortName'] for category in dress['categories']]
    colors = set()
    try:
      color_list = dress['colors'][0]['canonicalColors']
      for color in color_list:
        colors.add(color['name'])
    except IndexError:
      continue
    types, attributes = parser.parse(dress['name'], dress['description'])
    try:
      imgurl = dress['colors'][0]['image']['sizes']['Best']['url']
    except KeyError:
      imgurl = dress['image']['sizes']['Best']['url']      

    it = classes.Item(name, description, brand, categories, types, attributes, colors, imgurl, price)
    # if matches(user, item): # TODO
    result.append(it.toDict())
    new_dresses = dresses[i+1:]

  dresses = new_dresses
  if not dresses:
    return get_batch(t)

  return json.dumps(result)

def update_list(t):
  global current_offset, dresses
  old_size = len(dresses)
  dresses += shopstyle.get_batch(t, current_offset)
  current_offset += len(dresses) - old_size

def update_prefs(item, weight): # TODO fix weights
  for category in item['categories']:
    user_prefs[category] += float(weight) / len(item['categories'])
  for t in item['types']:
    user_prefs[t] += float(weight) / len(item['types'])
  for attribute in item['attributes']:
    user_prefs[attribute] += float(weight) / len(item['attributes'])
  for color in item['colors']:
    user_prefs[color] += float(weight) / len(item['colors'])

def de_htmlize(s):
  started = False
  new_s = []
  for c in s:
    if c == '<':
      started = True
    if not started:
      new_s.append(c)
    if c == '>':
      started = False
  return ''.join(new_s).strip()

def db_get_user(uid):
  global user_prefs

  connection = httplib.HTTPSConnection('api.parse.com', 443)
  connection.connect()
  connection.request('GET', '/1/classes/Dresses/' + uid, '', {
         "X-Parse-Application-Id": "PKrmNmjPokcQfoDsqyAWXfxjoHyUsPxFRFd6Q9u3",
         "X-Parse-REST-API-Key": "6UQ7REq6nFC2WLNX7sIgM90Qm1jcLZJOTRV0XLLk"
       })
  result = json.loads(connection.getresponse().read())
  del result['objectId']
  try:
    del result['uid']
  except KeyError:
    print "No uid!"
  del result['createdAt']
  del result['updatedAt']  
  user_prefs = SafeDict(result)

def db_post_user(uid=USER_ID):
  connection = httplib.HTTPSConnection('api.parse.com', 443)
  connection.connect()
  connection.request('PUT', '/1/classes/Dresses/' + uid, json.dumps(user_prefs), {
         "X-Parse-Application-Id": "PKrmNmjPokcQfoDsqyAWXfxjoHyUsPxFRFd6Q9u3",
         "X-Parse-REST-API-Key": "6UQ7REq6nFC2WLNX7sIgM90Qm1jcLZJOTRV0XLLk",
         "Content-Type": "application/json"
       })
  result = json.loads(connection.getresponse().read())
