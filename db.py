from flask import Flask
from flask_pymongo import pymongo
from application import application
from config import mongoLogin


username = mongoLogin["username"]
password = mongoLogin["password"]
CONNECTION_STRING = f"mongodb+srv://{username}:{password}@algo.7da41.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('algo_db')
user_collection = pymongo.collection.Collection(db, 'users')
algorithm_collection = pymongo.collection.Collection(db, 'algorithms')
