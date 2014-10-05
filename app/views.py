from app import app, classes, shopstyle
import core, json

@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!\n"

@app.route('/dresses')
def get_dress_batch():
  return core.get_batch('dresses')

@app.route('/update', methods=['POST'])
def update_prefs():
  item = json.loads(request.form['item'])
  weight = json.loads(request.form['weight'])
  core.update_prefs(item, weight)

@app.route('/close')
def update_db():
  core.db_post_user()
