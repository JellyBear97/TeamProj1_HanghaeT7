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

# 카테고리별 조회
@app.route("/posts/<category>", methods=["GET"])
def list_category(category):
    results = []
    all_posts = list(db.posts.find({'category':category}))
    for post in all_posts:
        post['_id'] = str(post['_id'])    ## object_id -> string으로 변환
        results.append(post)
    return jsonify({'result':results})  

# 게시글 상세조회 이동
@app.route("/posts/move/<p_id>", methods=["GET"])
def move_posts(p_id):
    return render_template("detail.html", p_id = p_id)

# 게시글 상세조회 가져오기
@app.route("/posts/detail/<p_id>", methods=["GET"])
def view_posts(p_id):
    findone = db.posts.find_one({'_id': ObjectId(p_id)})
    doc = {
       'title' : findone['title'],
        'comment' : findone['comment'],
        'reg_date' : findone['reg_date'],
        'mod_date' : findone['mod_date'],
        'category' : findone['category'],
        'user_id' : findone['user_id'],
        'image':findone['image']   
         }     
    return jsonify({'result':doc}) 

# 게시글 작성
@app.route("/posts/<category>", methods=["POST"] )
def insert_posts(category):
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    url_receive = request.form['url_give']
    #category_receive = request.form['category_give']
    category_receive = category
    name_receive = request.form['nickname_give']
    reg_date = datetime.datetime.utcnow()
    mod_date = datetime.datetime.utcnow()
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    
    if(category_receive == "book"):
         # ogtitle = soup.select_one('meta[property="og:title"]')['content'] 직접 적으면 필요X
        ogdesc = soup.select_one('meta[property="og:description"]')['content']
        ogimage = soup.select_one('meta[property="og:image"]')['content']  
    elif(category_receive == "music"):
        title_receive = soup.select_one('#body-content > div.search_song > div.search_result_detail > div > table > tbody > tr > td.info > a.title.ellipsis')['title'].strip()
        music_artist = soup.select_one('#body-content > div.search_song > div.search_result_detail > div > table > tbody > tr > td.info > a.artist.ellipsis').text.strip()
        ogimage = soup.select_one('#body-content > div.search_song > div.search_result_detail > div > table > tbody > tr > td:nth-child(3) > a > img')['src']
    else:
        ogimage = url_receive

    doc = {
        'title' : title_receive,
        'comment' : comment_receive,
        'reg_date' : reg_date,
        'mod_date' : mod_date,
        'category' : category_receive,
        'user_id' : name_receive,
        'image':ogimage, #이미지 썸네일로 사용,
        'artist':music_artist
    }

    db.posts.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

# 게시글 수정
@app.route("/posts/<category>/<p_id>", methods=["PUT"] )
def modify_posts(p_id):
    return jsonify({'msg':'수정완료!'})

# 게시글 삭제
@app.route("/posts/<p_id>", methods=["DELETE"])
def delete_posts(p_id):        
    db.posts.delete_one({'_id':ObjectId(p_id)})
    return jsonify({'msg':'삭제완료!'}) 

# 게시글에 해당하는 댓글 목록 조회
@app.route("/posts/<p_id>/comments", methods=["GET"])
def list_comments(p_id):
    results = []
    all_comments = list(db.comments.find({'p_id':p_id}))
    for comment in all_comments:
        comment['_id'] = str(comment['_id'])    ## object_id -> string으로 변환
        results.append(comment)
    return jsonify({'result':results}) 

# 댓글 작성
@app.route("/posts/<p_id>/comments", methods=["POST"])
def insert_comments(p_id):
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    reg_date = datetime.datetime.utcnow()
    mod_date = datetime.datetime.utcnow()

    doc = {
        'p_id' : p_id,
        'user_id' : name_receive,
        'comment' : comment_receive,
        'reg_date' : reg_date,
        'mod_date' : mod_date
    }
    db.comments.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

# 댓글 수정
@app.route("/posts/comments/<r_id>", methods=["PUT"])
def modify_comments(r_id):
    return jsonify({'msg':'수정완료!'})

# 댓글 삭제
@app.route("/posts/comments/<r_id>", methods=["DELETE"])
def delete_comments(r_id):
    db.comments.delete_one({'_id':ObjectId(r_id)})
    return jsonify({'msg':'삭제완료!'}) 

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)