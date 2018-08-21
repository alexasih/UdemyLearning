import uuid
import requests
from bs4 import BeautifulSoup
import re

from src.common.database import Database
import src.models.items.constants as ItemConstants

__author__ = 'alexasih'


class Item(object):
    def __init__(self, name, url, store, _id=None):
        self.name = name
        self.url = url
        self.store = store
        tag_name = store.tag_name
        query = store.query
        self.price = self.load_price(tag_name, query)
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self, tag_name, query):
        # Amazon: <span id="priceblock_ourprice" class="a-size-medium a-color-price">$3,099.00</span>
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(tag_name, query)
        string_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)")
        match = pattern.search(string_price)

        return match.group()

    def save_to_mongo(self):
        # Insert JSON representation
        Database.insert(ItemConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url
        }

    # post to mongo db

