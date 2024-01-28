User Data Fetch and Store
Overview
This project is a backend system that fetches user data from the Random User Generator API, processes and stores the data in Redis for caching, and finally stores the processed data in MongoDB. The application includes a cron job that runs every 3 1/2 hours to handle the entire process.

Architecture
The project is structured into several modules:
    config.py: Configuration file containing environment-specific settings.
    fetcher.py: Module responsible for fetching user data from the Random User Generator API.
    processor.py: Module responsible for processing and storing user data in Redis and MongoDB.
    main.py: Flask application defining endpoints and initiating the cron job.


Technologies Used
    Flask: Used for building the web application.
    Redis: Used for caching user data.
    MongoDB: Used for storing processed user data.
    APScheduler: Used for scheduling the cron job.
    Requests: Used for making HTTP requests to the Random User Generator API.


Running the Application
Clone the Repository:

    git clone https://github.com/KarunakaranDeveloper/userDataFetch.git
    cd userDataFetch

Set Up Virtual Environment:

    python -m venv venv
    source venv/bin/activate  # On Unix/Mac, or use .\venv\Scripts\activate on Windows

Install Dependencies:

    pip install -r requirements.txt

Start Redis Server:
    Ensure Redis is installed and running on the default port (6379).

Start MongoDB Server:
    Ensure MongoDB is installed and running on the default port (27017).

Run the Application:

    cd app
    python main.py

Test the Application:
    Use a tool like curl, Postman, or httpie to send a GET request to http://localhost:5000/api/user_data.

Run Unit Tests:

    python -m unittest discover tests
    
Cron Job Configuration
    The cron job is configured using the APScheduler library in the main.py file. It runs every 3 1/2 hours and triggers the data fetching and processing.

Author
Karunakaran