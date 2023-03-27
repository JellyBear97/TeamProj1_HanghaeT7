from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('여기에 URL 입력')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')    

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)