from flask import Flask, jsonify
import subprocess
import pymongo
import os
from dotenv import load_dotenv
from pathlib import Path
import random
import requests
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
load_dotenv()
app = Flask(__name__)

client = pymongo.MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('DB_NAME')]
collection = db[os.getenv('COLLECTION_NAME')]

@app.route('/run-script', methods=['GET'])
def run_script():
    
    subprocess.run(["python3", "scrape_twitter.py"])
    print("Script executed")
    last_record = collection.find().sort([('date_time', pymongo.DESCENDING)]).limit(1)
    print(last_record)
    return jsonify(last_record[0])

@app.route('/')
def index():
    return open('index.html').read()

if __name__ == "__main__":
    app.run(debug=True)
