# main.py
import json
import os
import sys
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_path, '..'))
sys.path.append(project_root)

from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from app.facade import UserDataFacade
from app.manager import RedisManager
from pymongo import MongoClient
from app.config import Config

app = Flask(__name__)
redis_client = RedisManager().client
mongo_client = MongoClient(Config.MONGO_URI)
db = mongo_client[Config.MONGO_DB_NAME]
collection = db['user_data']
user_data_facade = UserDataFacade()

# Schedule the cron job every 3 1/2 hours
scheduler = BackgroundScheduler()
scheduler.add_job(user_data_facade.fetch_process_store, 'interval', minutes=1, timezone=None)
# scheduler.add_job(user_data_facade.fetch_process_store, 'interval', hours=3.5, timezone=None)
scheduler.start()

# Define API endpoints
@app.route('/api/user_data', methods=['GET'])
def get_user_data():
    all_keys = redis_client.keys('user:*')
    cached_data = [json.loads(redis_client.get(key)) for key in all_keys[:10]]
    response = dict()
    if not cached_data:
        mongo_data = list(collection.find().limit(10))
        response = {
            "data": mongo_data,
            "total_length": len(mongo_data)
        }
        
        return jsonify(response)
    response = {
        "data": cached_data,
        "total_length": len(cached_data)
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
