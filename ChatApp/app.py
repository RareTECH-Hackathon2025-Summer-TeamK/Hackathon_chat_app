#モジュールのインポート
from flask import Flask, render_template, session, request, redirect, url_for, flash, abort
import uuid
import re
import os
import hashlib
from datetime import timedelta

from models import User, Channel, Message


EMAIL_PATTERN = r"^[\w.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+$"

app = Flask(__name__) 
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', uuid.uuid4().hex)

#セッションの有効期限を30日間と設定
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30) 

#ブラウザにCSSや画像などの静的ファイルをキャッシュさせる期間を約31日と設定
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 2678400

#トップページの表示
@app.route('/', methods=['GET'])
def index():
    return render_template("top.html")  

#サインアップページの表示
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template('auth/signup.html')

#サインアップ処理
@app.route('/signup', methods=['POST'])
def signup_process():
    user_name =request.form.get('user_name')
    email =request.form.get('email')
    password =request.form.get('password')
    password_confirmation =request.form.get('password-confirmation')

    if user_name == '' or password == '' or password_confirmation == '':
        flash('空のフォームがあります')
    elif password != password_confirmation:
        flash('2つのパスワードの値が違っています')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        user_id = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        registered_user = User.find_by_email(email)

        if registered_user != None:
            flash('既に登録されているようです')
        else:
            User.create(user_id, user_name, email, password)
            user_id = str(user_id)
            session['user_id'] = user_id
            session['email'] = email
            return redirect(url_for('channels_view'))
    return redirect(url_for('signup_view'))

#ログインページの表示
@app.route('/login', methods =['GET'])
def login_view():
    return render_template('auth/login.html')

#ログイン処理
@app.route('/login',methods =['POST'])
def login_process():
    email =request.form.get('email')
    password =request.form.get('password')

    if email =='' or password =='':
        flash('空のフォームがあります')
    else:
        user = User.find_by_email(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています')
            else:
                session['user_id'] = user["user_id"]
                session['email'] = user["email"]
                if user.get('is_admin'):
                    return redirect(url_for('edit_channels_view'))  
                else: 
                    return redirect(url_for('channels_view'))
    return redirect(url_for('login_view'))

#ログアウト方法
@app.route("/logout", methods =["GET"])
def logout():
    session.clear()
    return redirect(url_for("login_view"))

## チャンネル一覧ページの表示   
@app.route('/channels', methods =['GET'])
def channels_view(): 
    uid = session.get('user_id')
    if uid is None:
        return redirect(url_for('login_view'))
    
    email = session["email"]
    user = User.find_by_email(email)
    channels = Channel.get_all()
    return render_template('channels.html', channels=channels, user=user)


##チャンネル作成（管理者ユーザーのみ）  
@app.route('/admin/channels', methods ='POST')
def create_channel():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login_view'))
    
    channel_name = request.form.get('channelTitle')
    channel = Channel.find_by_name(channel_name)
    if channel == None:
        Channel.create(channel_name)
        return redirect(url_for('channels_view'))
    else:
        error = '既に同じ名前のチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)

##チャンネル編集（管理者ユーザーのみ）  
@app.route('/admin/channels/update/<cid>', methosa=['POST'])
def update_channel(cid):
    user_id = session.get('user_name')
    if user_id is None:
        return redirect(url_for('login_view'))
    
    channel_name = request.form.get('channelTitle')

    Channel.update(cid, channel_name,)
    return redirect(f'/channels/{cid}/messages')


## チャンネル編集ページの表示（管理者ユーザーのみ）  
@app.route('/admin/channels', methods=['GET'])
def edit_channels_view():
    uid = session.get('user_id')
    if uid is None:
        return redirect(url_for('login_view'))
    
    email = session["email"]
    user = User.find_by_email(email)
    
    if not user.get('is_admin'):
        return redirect(url_for('channels_view'))
    channels = Channel.get_all()
    return render_template('admin/channels/edit_channels.html', channels=channels, user=user)

## チャンネルの削除（管理者ユーザーのみ）  
@app.route('/admin/channels/<cid>', methods=['POST'])
def delete_channel(cid):
    user_id = session.get('user_id')
    channel = Channel.find_by_cid(cid)
    
    if channel and channel['user_id'] == user_id:
        channel.delete(channel)
        
    return redirect(url_for('edit_channels_view', cid=cid)) 

## チャンネル個別ページの表示
@app.route('/channels/<cid>/messages', methods=['GET'])
def messages(cid):
    uid = session.get('user_id')
    if uid is None:
        return redirect(url_for('login_view'))
    channel = Channel.find_by_cid(cid)
    if channel is None:
        abort(404) # チャンネルが存在しない場合は404エラー
    messages = Message.get_all(cid)
    return render_template('messages.html', uid=uid, channel=channel, messages=messages)

# メッセージの投稿
@app.route('/channels/<cid>/messages', methods=['POST'])
def create_message(cid):
    user_id = session.get('user_id')
    message = request.form.get('create_message')
    Message.create(user_id, cid, message)
    return redirect(url_for('messages', cid=cid))

# メッセージの削除
@app.route('/channels/<cid>/messages/<int:message_id>', methods=['POST'])
def delete_message(cid, message_id):
    user_id = session.get('user_id')
    message = Message.find_by_id(message_id)
    
    if message and message['user_id'] == user_id:
        Message.delete(message_id)
        
    return redirect(url_for('messages', cid=cid)) 

# メッセージの編集
@app.route('/channels/<cid>/messages/<int:message_id>/edit', methods=['POST'])
def edit_message(cid, message_id):
    user_id = session.get('user_id')
    message = Message.find_by_id(message_id)
    new_content = request.form.get('edit_message')

    if message and message['user_id'] == user_id:
        Message.update(message_id, new_content)

    return redirect(url_for('messages', cid=cid)) 

# 404エラー
@app.errorhandler(404)
def page_notfound(error):
    return render_template('error/404.html'),404

# 500エラー
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html'),500

if __name__ =='__main__':
    app.run(host="0.0.0.0", debug=True,) 