__author__ = 'alexasih'


class Item(object):
    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url

    def __repr(self):
        return "<Item {} with URL {}>".format(self.name, self.url)