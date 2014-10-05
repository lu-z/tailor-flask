class User:
  def __init__(self, uid, prefs):
    self.uid = uid
    self.prefs = prefs

  def update(self, new_data):
    self.prefs = new_data

class Item:
    def __init__(self, name, description, brand, categories, types, attributes, colors, imgurl, price):
        self.name = name
        self.description = description
        self.brand = brand
        self.categories = categories
        self.types = types
        self.attributes = attributes
        self.colors = colors
        self.imgurl = imgurl
        self.price = price

    def toDict(self):
        d = {'name': self.name,
             'description': self.description,
             'brand': self.brand,
             'categories': self.categories,
             'types': list(self.types),
             'attributes': list(self.attributes),
             'colors': list(self.colors),
             'img': self.imgurl,
             'price': self.price}
        return d
