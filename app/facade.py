# facade.py
from app.manager import RedisManager, MongoDBManager
from app.fetcher import UserDataFetcher
from app.processor import DataProcessor

class UserDataFacade:
    def __init__(self):
        self.redis_manager = RedisManager()
        self.mongo_manager = MongoDBManager()
        self.user_data_fetcher = UserDataFetcher()
        self.data_processor = DataProcessor()

    def fetch_process_store(self):
        user_data = self.user_data_fetcher.fetch_user_data()
        if user_data:
            print(f"Fetched new data: {user_data}")
            processed_data = self.data_processor.process_user_data(user_data)

            for user in processed_data:
                user_id = user['login']['uuid']
                redis_key = f'user:{user_id}'
                self.redis_manager.set_data(redis_key, user)

            self.mongo_manager.insert_data(processed_data)

            print("Data fetched, processed, and stored successfully.")
        else:
            print("No new data fetched today.")
        
