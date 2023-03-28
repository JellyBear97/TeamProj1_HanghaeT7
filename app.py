from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('mongodb+srv://raccoonboy0803:aydlalsk12@raccoonboy.9hdmenx.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
import certifi, datetime

from bson.objectid import ObjectId

@app.route('/')
def home():
    return render_template('index.html') 

#카테고리별 조회
@app.route("/posts/<category>", methods=["GET"])
def list_category(category):
    results = []
    all_movies = list(db.board.find({'category':category}))
    for movie in all_movies:
        movie['_id'] = str(movie['_id'])    ## object_id -> string으로 변환
        results.append(movie)
    return jsonify({'result':results})  

# 게시글 상세페이지로 이동
# @app.route("/detail/<p_id>", methods=["GET"])
# def view_posts(p_id):    
    
#     return render_template('detail.html',p_id=p_id)

@app.route("/posts/move/<p_id>", methods=["GET"])
def move_posts(p_id):
    return render_template("detail.html", p_id = p_id)

@app.route("/posts/detail/<p_id>", methods=["GET"])
def view_posts(p_id):
    findone = db.board.find_one({'_id': ObjectId(p_id)})
    doc = {
       'title' : findone['title'],
        'comment' : findone['comment'],
        'url' : findone['url'],
        'reg_date' : findone['reg_date'],
        'mod_date' : findone['mod_date'],
        'category' : findone['category'],
        'nickname' : findone['nickname'],
        'image':findone['image']   
         }     
    return jsonify({'result':doc}) 

# @app.route("/detail/get/<p_id>", methods=["GET"])
# def views_posts(p_id):   
#     findone = db.board.find_one({'_id':ObjectId(p_id)}) 
#     doc = {
#        'title' : findone['title'],
#         'comment' : findone['comment'],
#         'url' : findone['url'],
#         'reg_date' : findone['reg_date'],
#         'mod_date' : findone['mod_date'],
#         'category' : findone['category'],
#         'nickname' : findone['nickname'],
#         'image':findone['image']   
#          }         
#     return jsonify({'result':doc})     

   

#카테고리별 등록
@app.route("/posts/<category>", methods=["POST"] )
def insert_posts(category):
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    url_receive = request.form['url_give']
    # category_receive = request.form['category_give']
    category_receive = category
    nickname_receive = request.form['nickname_give']
    reg_date = datetime.datetime.utcnow()
    mod_date = datetime.datetime.utcnow()
    ## file_upload

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # ogtitle = soup.select_one('meta[property="og:title"]')['content'] 직접 적으면 필요X
    ogdesc = soup.select_one('meta[property="og:description"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']  

    doc = {
        'title' : title_receive,
        'comment' : comment_receive,
        'url' : url_receive,
        'reg_date' : reg_date,
        'mod_date' : mod_date,
        'category' : category_receive,
        'nickname' : nickname_receive,
        'image':ogimage #이미지 썸네일로 사용
    }

    db.board.insert_one(doc)

    return jsonify({'msg':'저장완료!'})         


#카테고리별 삭제
@app.route("/posts/<p_id>", methods=["DELETE"])
def delete_posts(p_id):        
    
    db.board.delete_one({'_id':ObjectId(p_id)})
  
    return jsonify({'msg':'삭제완료!'}) 



if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)