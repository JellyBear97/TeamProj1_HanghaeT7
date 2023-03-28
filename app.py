from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi, datetime

from bson.objectid import ObjectId

ca = certifi.where()

client = MongoClient('mongodb://spart:test@ac-ywf5hos-shard-00-00.vcctwzu.mongodb.net:27017,ac-ywf5hos-shard-00-01.vcctwzu.mongodb.net:27017,ac-ywf5hos-shard-00-02.vcctwzu.mongodb.net:27017/?ssl=true&replicaSet=atlas-1f9jmh-shard-0&authSource=admin&retryWrites=true&w=majority',tlsCAFile=ca)
db = client.diary

# 메인 페이지
@app.route('/')
def home():
    return render_template('index.html')

# 게시판 조회
@app.route("/posts", methods=["GET"])
def list_posts():
    return render_template('')

# 카테고리별 조회
@app.route("/posts/<category>", methods=["GET"])
def list_category():
    results = []
    all_movies = list(db.movies.find({}))
    for movie in all_movies:
        movie['_id'] = str(movie['_id'])    ## object_id -> string으로 변환
        results.append(movie)
    return jsonify({'result':results})

# 게시글 상세조회
@app.route("/posts/<category>/<p_id>", methods=["GET"])
def view_posts():
    # p_id 값 가져오기
    p_id_receive = request.args.get('p_id')
    return jsonify({'result':'success', 'msg': '이 요청은 GET!'})

# 게시글 작성
@app.route("/posts/<category>", methods=["POST"] )
def insert_posts():
    title_receive = request.form['title_give']
    desc_receive = request.form['desc_give']
    url_receive = request.form['url_give']
    category_receive = request.form['category_give']
    nickname_receive = request.form['nickname_give']
    reg_date = datetime.datetime.utcnow()
    mod_date = datetime.datetime.utcnow()
    ## file_upload

    doc = {
        'title' : title_receive,
        'desc' : desc_receive,
        'url' : url_receive,
        'reg_date' : reg_date,
        'mod_date' : mod_date,
        'category' : category_receive,
        'nickname' : nickname_receive
    }

    db.movies.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

# 게시글 수정
@app.route("/posts/<category>/<p_id>", methods=["PUT"] )
def modify_posts():
    return ""

# 게시글 삭제
@app.route("/posts/<category>/<p_id>", methods=["DELETE"] )
def delete_posts():
    return ""

# 게시글에 해당하는 댓글 목록 조회
@app.route("/posts/<category>/<p_id>/comments", methods=["GET"])
def list_comments():
    return ""

# 댓글 작성
@app.route("/posts/<category>/<p_id>/comments", methods=["POST"])
def insert_comments():
    return ""

# 댓글 삭제
@app.route("/posts/<category>/<p_id>/comments/<r_id>", methods=["DELETE"])
def delete_comments():
    return ""

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)