class Item:

    def __init__(self, brand, categories, color):
        self.brand = brand
        self.categories = categories
        self.color = color

    def toDict(self):
        d = {'brand': self.brand,
             'categories': self.categories,
             'color': self.color}
        return d
        