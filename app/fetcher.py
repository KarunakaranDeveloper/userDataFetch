# fetcher.py
import requests
import json
import logging
from datetime import datetime

class UserDataFetcher:
    def __init__(self, data_file_path='last_fetch_timestamp.txt'):
        self.data_file_path = data_file_path
        logging.basicConfig(filename='user_data_fetcher.log', level=logging.INFO)
        # Add a StreamHandler to print log messages to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logging.getLogger('').addHandler(console_handler)

    def fetch_user_data(self):
        # Record the start time
        start_time = datetime.now()

        # Load the last fetch timestamp from the file
        last_fetch_timestamp = self._load_last_fetch_timestamp()

        # Check if it's a new day
        if not self._is_same_day(last_fetch_timestamp, datetime.now()):
            # Fetch new data
            response = requests.get('https://randomuser.me/api/?results=10')
            new_data = response.json()['results']

            # Update the last fetch timestamp in the file
            self._update_last_fetch_timestamp()

            # Record the end time
            end_time = datetime.now()

            # Log the details
            self._log_request_details(response.url, response.request.method, response.json(), start_time, end_time)

            return new_data

        # If it's the same day, return None or some indicator that no new data is fetched
        return None

    def _load_last_fetch_timestamp(self):
        try:
            with open(self.data_file_path, 'r') as file:
                timestamp_str = file.read()
                return datetime.fromisoformat(timestamp_str)
        except FileNotFoundError:
            # If the file doesn't exist, return a timestamp far in the past
            return datetime.fromisoformat('2000-01-01T00:00:00')

    def _update_last_fetch_timestamp(self):
        timestamp_str = datetime.now().isoformat()
        with open(self.data_file_path, 'w') as file:
            file.write(timestamp_str)

    def _is_same_day(self, date1, date2):
        return date1.date() == date2.date()

    def _log_request_details(self, url, method, response_json, start_time, end_time):
        total_response_time = (end_time - start_time).total_seconds()
        log_message = (
            f"Request Time: {start_time}, "
            f"URL: {url}, "
            f"HTTP Method: {method}, "
            f"Response JSON: {json.dumps(response_json)}, "
            f"Total Response Time: {total_response_time} seconds"
        )
        logging.info(log_message)


