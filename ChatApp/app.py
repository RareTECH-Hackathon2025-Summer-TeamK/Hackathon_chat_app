from flask import Flask, render_template,flash, request, session,redirect,url_for
from datetime import datetime
import hashlib 
import uuid
import os

from models import User, Channel, Message


# インスタンス生成
app = Flask(__name__)
app.secret_key = os.getenv('SEACRET_KEY',uuid.uuid4().hex)

# ルーティング

## TOPページ
@app.route('/', methods = ['GET'])
def index():
    uid =session.get('uid')
    if uid is None:
        return render_template('top.html')
    return redirect(url_for('channel_view'))

## サインアップページ
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template('auth/signup.html')

## サインアップ処理
@app.route('/signup', methods=['POST'])
def signup_process():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')
    passwordConfirmation = request.form.get('password-confirmation')
    
    if user_name == '' or email == '' or password == '' or passwordConfirmation == '':
        flash('空のフォームがあるようです')
    elif password != passwordConfirmation:
        flash('パスワードが一致しません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        registered_user = User.find_by_email(email)
        
        if registered_user != None:
            flash('既に登録されているようです')
        else:
            User.create(uid, user_name, email, password )
            UserId = int(uid)
            session['uid'] = UserId
            return redirect(url_for('channels_view'))            
    return redirect(url_for('signup_view'))

## ログインページの表示
@app.route('/login', methods=['GET'])
def login_view(): 
    return render_template('auth/login.html')

## ログイン処理
@app.route('/login', methods=['POST'])
def login_process(): 
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email =='' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = User.find_by_emial(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています！')
            else:
                session['uid'] = user["uid"]
                return redirect(url_for('channels_view'))
    return redirect(url_for('login_view'))

## ログアウト処理  
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_view'))


## チャンネル一覧ページの表示   
@app.route('/channels', methods =['GET'])
def channels_view(): 
    uid = session.get('uid') #ユーザーの入力したuidがあるか確認
    if uid is None:
        return redirect(url_for('login_view'))
    else:
        channels = Channel.get_all() #DBから情報を取得する
        channels.reverse() #新しい順に並べる
        return render_template('channels.html', channels = channels, uid = uid)
    
##チャンネル作成（管理者）
@app.route('/admin/channels/create',  methods =['POST'])
def create_channel():
    user = User.find(uid) 
    uid = session.get('uid')
    if uid is None or not user or not user.is_admin:
     #未ログイン、存在しないユーザー、管理者以外はログイン画面へ戻る
        return redirect(url_for('login_view'))

    
    channel_name = request.form.get('channel_name')
    Channel.create(uid, channel_name)
    
    return redirect(url_for('admin_channels_view'))
    
    
##チャンネル更新（管理者）
@app.route('/admin/channels/update/<cid>', methods=['POST'])
def update_channel(cid):
    uid = session.get('uid')
    user = User.find(uid)
    if not user or not user.is_admin:
     return redirect(url_for('login_view'))
    
    channel_name = request.form.get('channel_name')
    Channel.update(uid, channel_name, cid)
    return redirect(f'/channels/{cid}/messages')

##チャンネル削除（管理者）
@app.route('/admin/channels/delete/<cid>', methods=['POST'])
def delete_channel(cid):
    uid = session.get('uid')
    user = User.find(uid)
    if not user or not user.is_admin:
     return redirect(url_for('login_view'))
    
    Channel.delete(cid)
    return redirect(url_for('channels_view'))
   
      
##チャンネル詳細ページの表示
@app.route('/channels/<cid>/messages', methods=['GET'])
def detail(cid):
    #if文が入る
    return render_template('messages.html')
     
    
##メッセージの投稿
@app.route('/channels/<cid>/messages', methods=['POST'])
def create_message(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    
    message = request.form.get('message')
    
    if message: #messageが空なら投稿処理をスキップ
        Message.create(uid,cid,message) #uid,cid,messageを記録
    return redirect(f'/channels/{cid}/messages')

##メッセージの削除
@app.route('/channels/<cid>/messages/<messages_id>', methods=['POST'])
def delete_message(cid, message_id):
    user = User.find(session.get('uid'))
    if not user or not user.is_admin:
        return redirect(url_for('login_view'))
    Message.delete(message_id)
    return redirect(f'/channels/{cid}/messages')
##404エラー
app.errorhandler(404)
def page_notfound(error):
    return render_template('error/404.html'),404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html'),500

# 実行
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True) # debug=True は、デバッグモードを有効