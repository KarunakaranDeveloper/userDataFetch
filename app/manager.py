# manager.py
from pymongo import MongoClient
import json
import redis
from app.config import Config

class RedisManager:
    def __init__(self):
        self.client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)

    def set_data(self, key, value):
        self.client.set(key, json.dumps(value))

class MongoDBManager:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB_NAME]
        self.collection = self.db['user_data']

    def insert_data(self, data):
        self.collection.insert_many(data)
