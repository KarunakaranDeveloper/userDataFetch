# test_app.py

import json
import unittest
from unittest.mock import patch
from app.fetcher import UserDataFetcher
from app.manager import RedisManager, MongoDBManager
from app.processor import DataProcessor
from app.facade import UserDataFacade
from unittest.mock import patch

class TestUserDataFetcher(unittest.TestCase):
    def test_fetch_user_data(self):
        # Initialize UserDataFetcher
        user_data_fetcher = UserDataFetcher()

        # Mock the requests.get method to avoid making actual HTTP requests
        with patch('requests.get') as mock_get:
            # Set the return value for the mocked method
            mock_get.return_value.json.return_value = {'results': [{'login': {'uuid': '123'}}]}

            # Call the fetch_user_data method
            new_data = user_data_fetcher.fetch_user_data()

            # Print information for debugging
            print("Mocked response:", mock_get.return_value.json.return_value)
            print("New data:", new_data)

            # Check if new_data is not None
            self.assertIsNotNone(new_data)


class TestRedisManager(unittest.TestCase):
    def test_set_data(self):
        # Initialize RedisManager
        redis_manager = RedisManager()

        # Test setting data
        key = 'test_key'
        value = {'test': 'data'}
        redis_manager.set_data(key, value)

        # Retrieve and check the stored data
        retrieved_value = redis_manager.client.get(key)
        self.assertIsNotNone(retrieved_value)
        self.assertEqual(json.loads(retrieved_value), value)

import uuid

class TestMongoDBManager(unittest.TestCase):
    def assertDictSubset(self, expected, actual):
        # Check if the expected dictionary is a subset of the actual dictionary
        for key, value in expected.items():
            self.assertIn(key, actual, f"Key '{key}' not found in the actual dictionary")
            if isinstance(value, dict):
                self.assertDictSubset(value, actual[key])
            elif key == 'uuid':
                # Convert expected 'uuid' value to UUID string for comparison
                self.assertEqual(uuid.UUID(value), uuid.UUID(actual[key]), f"Value mismatch for key '{key}'")
            else:
                self.assertEqual(value, actual[key], f"Value mismatch for key '{key}'")

    def test_insert_data(self):
        # Initialize MongoDBManager
        mongo_manager = MongoDBManager()

        # Test inserting data
        data = [{'login': {'uuid': '123'}}]
        mongo_manager.insert_data(data)

        # Retrieve and check the inserted data
        retrieved_data = list(mongo_manager.collection.find({}, {'_id': 0}))

        # Compare the lists element by element
        for expected, actual in zip(data, retrieved_data):
            # Ignore the '_id' field in the retrieved document
            actual.pop('_id', None)
            # Check if the expected dictionary is a subset of the actual dictionary
           


class TestDataProcessor(unittest.TestCase):
    def test_process_user_data(self):
        # Initialize DataProcessor
        data_processor = DataProcessor()

        # Test processing user data (add more tests based on the actual processing logic)
        user_data = [{'login': {'uuid': '123'}}]
        processed_data = data_processor.process_user_data(user_data)

        # For simplicity, just checking if the processed data is the same as input data
        self.assertEqual(processed_data, user_data)

class TestUserDataFacade(unittest.TestCase):
    @patch.object(UserDataFetcher, 'fetch_user_data', return_value=[{'login': {'uuid': '123'}}])
    @patch.object(DataProcessor, 'process_user_data', return_value=[{'login': {'uuid': '123'}}])
    def test_fetch_process_store(self, mock_fetch_user_data, mock_process_user_data):
        # Initialize UserDataFacade
        user_data_facade = UserDataFacade()

        # Test fetching, processing, and storing data
        user_data_facade.fetch_process_store()

        # Check if the fetch_user_data and process_user_data methods were called
        mock_fetch_user_data.assert_called_once()
        mock_process_user_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()
