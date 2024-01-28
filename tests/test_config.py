# test_config.py

import unittest
from app.config import Config

class TestConfig(unittest.TestCase):
    def test_redis_config(self):
        self.assertEqual(Config.REDIS_HOST, 'localhost')
        self.assertEqual(Config.REDIS_PORT, 6379)

    def test_mongo_config(self):
        self.assertEqual(Config.MONGO_URI, 'mongodb://localhost:27017/')
        self.assertEqual(Config.MONGO_DB_NAME, 'user_data_db')

if __name__ == '__main__':
    unittest.main()
