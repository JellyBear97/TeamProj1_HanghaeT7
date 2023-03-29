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
# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib

# 메인 페이지
@app.route('/')
def home():
    return render_template('index.html')

# 카테고리별 조회
@app.route("/posts/data/<category>", methods=["GET"])
def get_Data(category):
    results = []
    all_posts = list(db.posts.find({'category':category}))
    for post in all_posts:
        post['_id'] = str(post['_id'])    ## object_id -> string으로 변환
        results.append(post)
    return jsonify({'result':results})  

# 영화 목록 이동
@app.route('/posts/movie')
def list_movie():
    return render_template('main.html', category = 'movie')

# 음악 목록 이동
@app.route('/posts/music')
def list_music():
    return render_template('main.html', category = 'music')

# 애니 목록 이동
@app.route('/posts/ani')
def list_ani():
    return render_template('main.html', category = 'ani')

# 운동 목록 이동
@app.route('/posts/health')
def list_health():
    return render_template('main.html', category = 'health')

# 책 목록 이동
@app.route('/posts/book')
def list_book():
    return render_template('main.html', category = 'book')

# 게시글 상세조회 이동
@app.route("/posts/move/<category>/<p_id>", methods=["GET"])
def move_posts(category, p_id):
    return render_template("detail.html", p_id = p_id, category = category)

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
        'image':findone['image'],
        'like':findone['like']  
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
    mod_date = ''
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    music_artist = ''
    
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
        'artist':music_artist,
        'like':0
    }

    db.posts.insert_one(doc)

    return jsonify({'msg':'등록완료!'})

# 게시글 수정
@app.route("/posts/<p_id>", methods=["PUT"] )
def modify_posts(p_id):

    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    url_receive = request.form['url_give']
    category_receive = request.form['category_give']
    name_receive = request.form['nickname_give']
    mod_date = datetime.datetime.utcnow()

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    music_artist = ''

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

    db.posts.update_one({'_id':ObjectId(p_id)},
                        {'$set':{'title': title_receive,
                                 'comment':comment_receive,
                                 'mod_date':mod_date,
                                 'category':category_receive,
                                 'user_id':name_receive,
                                 'image':ogimage,
                                 'artist':music_artist
                        }})
    return jsonify({'msg':'수정완료!'})

# 게시글 삭제
@app.route("/posts/<p_id>", methods=["DELETE"])
def delete_posts(p_id):        
    db.posts.delete_one({'_id':ObjectId(p_id)})
    return jsonify({'msg':'삭제완료!'}) 

# 게시글 좋아요
@app.route("/posts/like/<p_id>", methods=["PUT"])
def like_posts(p_id):   
    like_receive = request.form['like_give']

    db.posts.update_one({'_id':ObjectId(p_id)},
                        {'$set':{'like': like_receive}})
    return jsonify({'msg':'좋아요 완료!'}) 

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
    mod_date = ''

    doc = {
        'p_id' : p_id,
        'user_id' : name_receive,
        'comment' : comment_receive,
        'reg_date' : reg_date,
        'mod_date' : mod_date
    }
    db.comments.insert_one(doc)

    return jsonify({'msg':'등록완료!'})

# 댓글 수정
@app.route("/posts/comments/<r_id>", methods=["PUT"])
def modify_comments(r_id):
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    mod_date = datetime.datetime.utcnow()


    db.comments.update_one({'_id':ObjectId(r_id)},
                        {'$set':{
                                 'user_id':name_receive,
                                 'comment':comment_receive,
                                 'mod_date': mod_date
                        }})
    return jsonify({'msg':'수정완료!'})

# 댓글 삭제
@app.route("/posts/comments/<r_id>", methods=["DELETE"])
def delete_comments(r_id):
    db.comments.delete_one({'_id':ObjectId(r_id)})
    return jsonify({'msg':'삭제완료!'}) 

# 회원가입 API
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success'})

# 로그인 API
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)