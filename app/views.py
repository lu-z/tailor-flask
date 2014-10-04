from app import app, shopstyle, item, user
import json, parser

QUERY_SIZE = 10

#########
# Views #
#########

@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!\n"

@app.route('/dresses')
def get_dress_batch():
  return get_batch('dresses')


###############
# Actual work #
###############

current_offset = 0
dresses = []
def get_batch(t):
  global current_offset
  global dresses
  print 'Offset:', current_offset

  if not dresses:
    dresses = shopstyle.get_batch(t, current_offset)
    current_offset += len(dresses)

  result, new_dresses = [], [];
  for i in range(0, len(dresses)):
    if len(result) >= QUERY_SIZE:
      break

    dress = dresses[i]
    try:
      brand = dress['brand']['name']
    except KeyError as k:
      new_dresses = dresses[i+1:]
      continue
    categories = [category['shortName'] for category in dress['categories']]
    colors = [color['name'] for color in dress['colors']]
    types, attributes = parser.parse(dress['name'], dress['description'])

    it = item.Item(brand, categories, types, attributes, colors)
    # if matches(user, item): #implement this
    result.append(it.toDict())
    new_dresses = dresses[i+1:]

  dresses = new_dresses
  if not dresses:
    return get_batch(t)

  return json.dumps(result) + '\n'
