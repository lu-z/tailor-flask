from app import app, shopstyle, item, user
import json

QUERY_SIZE = 10

@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!\n"

@app.route('/dresses')
def get_dress_batch():
  return get_batch('dress')



dresses = []
def get_batch(t):
  global dresses
  if not dresses:
    dresses = shopstyle.get_batch(t)

  result = [];
  for i in range(0, len(dresses)):
    if len(result) >= QUERY_SIZE:
      dresses = new_dresses
      break

    dress = dresses[i]
    try:
      brand = dress['brand']['name']
    except KeyError as k:
      continue
    categories = [category['shortName'] for category in dress['categories']]
    colors = [color['name'] for color in dress['colors']]

    it = item.Item(brand, categories, colors)
    #add attributes
    # if matches(user, item): #implement this
    result.append(it.toDict()) #implement this too
    new_dresses = dresses[i+1:]

  return json.dumps(result) + '\n'
