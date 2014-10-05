from app import app, classes, shopstyle
from flask import request
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
  weight = json.loads(request.form['weight'])['weight']
  core.update_prefs(item, weight)
  return 'Success\n'

@app.route('/close')
def update_db():
  core.db_post_user()

@app.route('/stats')
def get_stats():
  return json.dumps(core.get_stats())