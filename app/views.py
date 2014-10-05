from app import app, shopstyle, classes
import core

@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!\n"

@app.route('/dresses')
def get_dress_batch():
  return core.get_batch('dresses')
