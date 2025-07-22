from flask import Flask, render_template

# インスタンス生成
app = Flask(__name__)

# ルーティング

## TOPページ
@app.route('/')
def index():
    return render_template('top.html')


# 実行
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True) # debug=True は、デバッグモードを有効