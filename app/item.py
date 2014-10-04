class Item:

    def __init__(self, brand, categories, types, attributes, colors):
        self.brand = brand
        self.categories = categories
        self.types = types
        self.attributes = attributes
        self.colors = colors

    def toDict(self):
        d = {'brand': self.brand,
             'categories': self.categories,
             'types': self.types,
             'attributes': self.attributes,
             'color': self.colors}
        return d
