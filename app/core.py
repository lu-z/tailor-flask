from app import shopstyle, classes
from util import SafeDict
import httplib, json, operator, parser, threading

QUERY_SIZE = 10
REQUEST_THRESHOLD = 20
USER_ID = 'i7AfKxW9wG'

MAGIC_THRESHOLD = 0
CATEGORY_WEIGHT = 4
TYPE_WEIGHT = 3
ATTRIBUTE_WEIGHT = 2
COLOR_WEIGHT = 1

current_offset = 0
dresses = []

user_prefs = SafeDict()
user_brands = SafeDict()
user_styles = SafeDict()
mean_price = 0
yes_count = 0

initialized = False
iterations = 0

def get_batch(t):
  global current_offset, dresses, initialized, iterations

  print "get_batch ITERATIONS1:", iterations
  iterations += 1
  print "get_batch ITERATIONS2:", iterations

  if not initialized:
    db_get_user(USER_ID)
    initialized = True
  if not dresses:
    update_list(t)

  print "PRE UPDATE"
  print user_prefs
  update_pref_weights()
  print "POST UPDATE"
  print user_prefs

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
    if matches(user_prefs, it):
      result.append(it.toDict())
    new_dresses = dresses[i+1:]

  dresses = new_dresses
  if not dresses:
    return get_batch(t)

  return json.dumps(result)

def matches(prefs, item):
  catotal = 0
  for category in item.categories:
    catotal +=  float(prefs[category]) / len(item.categories)
  catotal *= CATEGORY_WEIGHT
  print "CATEGORY TOTAL = ", catotal

  ttotal = 0
  for t in item.types:
    ttotal +=  float(prefs[t]) / len(item.types)
  ttotal *= TYPE_WEIGHT
  print "TYPES TOTAL = ", catotal

  atotal = 0
  for attribute in item.attributes:
    atotal +=  float(prefs[attribute]) / len(item.attributes)
  atotal *= ATTRIBUTE_WEIGHT
  print "ATTRIBUTES TOTAL = ", catotal

  cototal = 0
  for color in item.colors:
    cototal +=  float(prefs[color]) / len(item.colors)
  cototal *= COLOR_WEIGHT
  print "COLORS TOTAL = ", catotal

  total = catotal + ttotal + atotal + cototal
  print "TOTAL = ", total
  if total < MAGIC_THRESHOLD:
    print item.imgurl
  return total >= MAGIC_THRESHOLD

def update_list(t):
  global current_offset, dresses
  old_size = len(dresses)
  dresses += shopstyle.get_batch(t, current_offset)
  current_offset += len(dresses) - old_size

def update_prefs(item, weight):
  global iterations, user_brands, mean_price, yes_count
  print "ITERATIONS is", iterations

  for category in item['categories']:
    user_prefs[category] += (float(weight) / len(item['categories'])) / iterations
  for t in item['types']:
    user_prefs[t] += (float(weight) / len(item['types'])) / iterations
    user_styles[t] += (float(weight) / len(item['types'])) / iterations
  for attribute in item['attributes']:
    user_prefs[attribute] += (float(weight) / len(item['attributes'])) / iterations
  for color in item['colors']:
    user_prefs[color] += (float(weight) / len(item['colors'])) / iterations

  user_brands[item['brand']] += weight
  if weight == 1:
    mean_price *= yes_count
    yes_count += 1
    price = item['price'][1:]
    price = str(price).translate(None, ',')
    mean_price += float(price)
    mean_price = float(mean_price) / yes_count

def update_pref_weights():
  global iterations, user_prefs
  for key in user_prefs.keys():
    user_prefs[key] *= 1 - float(1) / iterations
  for key in user_styles.keys():
    user_styles[key] *= 1 - float(1) / iterations

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

def get_stats():
  sorted_brands = sorted(user_brands.items(), key=operator.itemgetter(1))
  sorted_brands.reverse()
  sorted_styles = sorted(user_styles.items(), key=operator.itemgetter(1))
  sorted_styles.reverse()

  if len(sorted_brands) >= 3:
    top_brands = sorted_brands[0:3]
  else:
    top_brands = sorted_brands
  if len(sorted_styles) >= 3:
    top_styles = sorted_styles[0:3]
  else:
    top_styles = sorted_styles

  d = {'mean_price': mean_price,
       'top_brands': [x[0] for x in top_brands],
       'top_styles': [y[0] for y in top_styles]}
  return d

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
  global initialized

  connection = httplib.HTTPSConnection('api.parse.com', 443)
  connection.connect()
  connection.request('PUT', '/1/classes/Dresses/' + uid, json.dumps(user_prefs), {
         "X-Parse-Application-Id": "PKrmNmjPokcQfoDsqyAWXfxjoHyUsPxFRFd6Q9u3",
         "X-Parse-REST-API-Key": "6UQ7REq6nFC2WLNX7sIgM90Qm1jcLZJOTRV0XLLk",
         "Content-Type": "application/json"
       })
  result = json.loads(connection.getresponse().read())
  initialized = False
