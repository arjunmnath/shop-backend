import os

import qrcode
from pydantic import ValidationError 
from pymongo import MongoClient
import api.models as models


def normalize(i):
    i['_id'] = str(i['_id'])
    return i

class MultiDict(dict):
    def getlist(self, key):
        return self[key] if type(self[key]) == list else [self[key]]

    def __repr__(self):
        return type(self).__name__ + '(' + dict.__repr__(self) + ')'

class DBHandle:
    def __init__(self): 
        uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(uri)
        self.db = self.client.get_database("shopapp")
        self.Products = models.Products
        self.Customer = models.Customer
        self.Sales = models.Sales
    
    def add_document(self, item_data: dict, collection_name, model):
        try:
            item = model(**item_data)
            collection = self.db[collection_name]
            collection.insert_one(item.dict())
            return 
        except ValidationError as e:
            return

    def get_documents(self, collection_name):
        try:
            return [normalize(i) for i in list(self.db[collection_name].find())]
        except Exception as e:
            return

def qrgen(text):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(text)        
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img
