from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.il2ibyq.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/music", methods=["POST"])
def music_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    name_receive = request.form['name_give']
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    music_title = soup.select_one('#body-content > div.search_song > div.search_result_detail > div > table > tbody > tr > td.info > a.title.ellipsis')['title'].strip()
    music_artist = soup.select_one('#body-content > div.search_song > div.search_result_detail > div > table > tbody > tr > td.info > a.artist.ellipsis').text.strip()
    music_image = soup.select_one('#body-content > div.search_song > div.search_result_detail > div > table > tbody > tr > td:nth-child(3) > a > img')['src']

    doc = {
        'title':music_title,
        'artist':music_artist,
        'image':music_image,
        'comment':comment_receive,
        'name':name_receive
    }
    db.music.insert_one(doc)

    return jsonify({'msg':'취향 공유 완료!'})

@app.route("/music", methods=["GET"])
def music_get():
    all_musics = list(db.music.find({},{'_id':False}))
    return jsonify({'result':all_musics})

@app.route('/detail')
def detail():
    return render_template("detail.html")

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

