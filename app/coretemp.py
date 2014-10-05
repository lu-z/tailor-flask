from app import shopstyle, classes
import json, parser, threading

QUERY_SIZE = 10
REQUEST_THRESHOLD = 20

current_offset = 0
dresses_json = []
dresses = []

def get_batch(t):
  global current_offset, dresses

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

    it = classes.Item(name, brand, categories, types, attributes, colors, imgurl)
    # if matches(user, item): #implement this
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

