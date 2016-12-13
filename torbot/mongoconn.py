#mongoconn.py

from pymongo import MongoClient
from pymongo.database import Database
from bson.objectid import ObjectId
# {'_id': ObjectId(_id)}

client = MongoClient()
db = client.torbot

class MongoConnection(object):
    mongoconn = None

    def __init__(self, db=None, collection=None, endpoint=None):
        self.mongodb = db
        self.mongocollection = collection
        self.mongoendpoint = endpoint
        MongoConnection.mongoconn = self.__mongo_connect()
    
    def __mongo_connect(self):
        if self.mongoendpoint is not None: 
            return MongoClient(host=self.mongoendpoint, port=27017, document_class=dict, tz_aware=False, connect=True)[self.mongodb][self.mongocollection]
        else: 
            return MongoClient(host='localhost', port=27017, document_class=dict, tz_aware=False, connect=True)[self.mongodb][self.mongocollection]