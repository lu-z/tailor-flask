class User:

  def __init__(self, uid, prefs):
    self.uid = uid
    self.prefs = prefs

  def update(self, new_data):
    self.prefs = new_data