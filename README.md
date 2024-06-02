# Flask Twitter Trends Scraper

This application scrapes trending topics from Twitter using Selenium and saves the data to MongoDB. Each request uses a different proxy IP address from ProxyMesh.

## Prerequisites

- Python 3.6+
- MongoDB
- Chrome browser
- ChromeDriver

## Installation

### Step 1: Clone the Repository

Clone this repository to your local machine:

```bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

pip install -r requirements.txt

```

### Step 2: Set Up Environment Variables

Create a .env file in the project root directory and add your environment variables:

MONGO_URI=mongodb://localhost:27017/
TWITTER_USERNAME=your_twitter_username
TWITTER_PASSWORD=your_twitter_password
PROXY_USER=your_proxymesh_username
PROXY_PASS=your_proxymesh_password

Replace the placeholders with your actual values.

Running the Application

Step 1: Start MongoDB
Make sure your MongoDB server is running.

Step 2: Run the Flask Application
Run the Flask application:

```bash

export FLASK_APP=app.py
export FLASK_ENV=development
flask run

```

## Step 3: Access the Application

Open your web browser and navigate to http://127.0.0.1:5000 to access the application.

### Usage

Click the button on the web page to start the script that scrapes the trending topics from Twitter and displays them.

### Troubleshooting

Proxy Connection Failed: Ensure your ProxyMesh credentials are correct and you have an active subscription.
Environment Variables Not Updated: If changes to the .env file are not reflected, restart the Flask application.