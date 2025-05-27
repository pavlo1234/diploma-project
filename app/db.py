from pymongo import MongoClient
import os

client = MongoClient(os.environ['MONGODB_URL'])

db = client[os.environ['MONGODB_DATABASE']]
