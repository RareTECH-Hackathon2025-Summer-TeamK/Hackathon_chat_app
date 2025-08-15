#モジュールのインポート
from flask import Flask, render_template, session, request, redirect, url_for, flash
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import timedelta


#Webアプリ作成
app = Flask(__name__) 
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

#セッション関連
#有効期限を30日間と設定
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30) 

#トップページ
@app.route("/", methods=['GET'])
def index():
    if "user_id"  in session:
        return redirect(url_for("channels_view"))
    else:
        return render_template("top.html")  

#サインアップ
@app.route("/signup", methods=['GET','POST'])
def signup_view():
    if request.method == 'GET':
        return render_template("auth/signup.html")
    
    user_id = str(uuid.uuid4())
    user_name =request.form.get('user_name')
    email =request.form.get('email')
    password =request.form.get('password')
    password_confirmation =request.form.get('password-confermation')
    ##パスワードをハッシュ化
    password_hash = generate_password_hash(password)

    ##未入力チェック
    if not user_name or not email or not password:
        flash("未入力の項目があります")
    elif password != password_confirmation:
        return redirect(url_for("signup_view"))

    session["user_id"] = user_id
    session.permanent = True 
    return redirect(url_for("channels_view"))

#ログイン
@app.route("/login", methods =["GET", "POST"])
def login_view():
    if request.method == "GET":
        return render_template("auth/login.html")
    
    email =request.form.get('email')
    password =request.form.get('password')

   ##未入力チェック
    if not email or not password:
        flash("メールアドレスとパスワードを入力してください")
        return redirect(url_for("login_view"))

    ##DBからレコード取得
    user = User.find_by_email(email)

    ##ユーザーが存在しないorパス不一致
    if not user or not check_password_hash(user["password_hash"], password):
        flash("メールアドレスまたはパスワードが違います")
        return redirect(url_for("login_view"))

    user_id = session["user_id"] 
    session.permanent = True 
    return redirect(url_for("channels_view"))

#ログアウト
@app.route("/logout", methods =["GET"])
def logout():
    session.clear()
    return redirect(url_for("login_view"))


if __name__ =='__main__':
    app.run(host="0.0.0.0", debug=True,) 