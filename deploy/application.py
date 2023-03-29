from flask import Flask, render_template, request, jsonify
application = app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi, datetime

from bson.objectid import ObjectId

ca = certifi.where()

client = MongoClient('mongodb://spart:test@ac-ywf5hos-shard-00-00.vcctwzu.mongodb.net:27017,ac-ywf5hos-shard-00-01.vcctwzu.mongodb.net:27017,ac-ywf5hos-shard-00-02.vcctwzu.mongodb.net:27017/?ssl=true&replicaSet=atlas-1f9jmh-shard-0&authSource=admin&retryWrites=true&w=majority',tlsCAFile=ca)
db = client.diary

# 메인페이지
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()