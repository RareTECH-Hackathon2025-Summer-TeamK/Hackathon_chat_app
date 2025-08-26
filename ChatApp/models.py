from flask import abort
import pymysql
from util.DB import DB
import uuid

db_pool =DB.init_db_pool()

class User:
    @classmethod
    def create(cls, user_id, user_name, email, password):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (user_id, user_name, email, password) VALUES (%s, %s, %s, %s);"
                cur.execute(sql, (user_id, user_name, email, password))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    # クラスメソッドとして定義し、メールアドレスでユーザーを検索する
    @classmethod
    def find_by_email(cls, email):
        # データベース接続プールからコネクションを取得
        conn = db_pool.get_conn()
        try:
            # DBコネクションからカーソル（SQL実行用オブジェクト）を取得
            # with構文により、処理終了後にカーソルが自動的にクローズされる
            with conn.cursor() as cur:
                # 検索用SQL文を定義（メールアドレスを条件に users テーブルから取得）
                sql = "SELECT * FROM users WHERE email=%s;"
                # execute でSQL文を実行し、email の値を安全にバインド（SQLインジェクション防止）
                cur.execute(sql, (email,))
                # 最初の1件の行を取得（該当がなければ None）
                user = cur.fetchone()
            # 検索結果を呼び出し元に返す
            return user
        # PyMySQLで発生したエラーを捕捉
        except pymysql.Error as e:
            # エラー内容を出力（ログ代わり）
            print(f'エラーが発生しています：{e}')
            # Flask の abort を使い HTTP 500 エラー応答を返す
            abort(500)
        # 成功・失敗にかかわらず必ず実行される処理
        finally:
            # 借りたコネクションを接続プールに返却（再利用可能にする）
            db_pool.release(conn)
            
# チャンネルクラス
class Channel:
    @classmethod
    def find_by_name(cls, channel_name):
        conn =db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM channels WHERE channel_name =%s LIMIT 1;"
                cur.execute(sql, (channel_name,))
                return cur.fetchone()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_cid(cls, cid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM channels WHERE channel_id=%s;"
                cur.execute(sql, (cid,))
                channel = cur.fetchone()
                return channel
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def create(cls, channel_name):
        channel_id = uuid.uuid4()
        conn =db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO channels (channel_id, channel_name ) VALUES(%s, %s);"
                cur.execute(sql, (channel_id, channel_name))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_all(cls):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM channels;"
                cur.execute(sql)
                # 変数channelsにデータベースのデータをリスト型で保管している
                # cur.fetchallはリスト（list）の形式で返すメソッド
                channels = cur.fetchall()
                return channels
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls,cid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM channels WHERE channel_id=%s;"
                cur.execute(sql, (cid,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, cid, channel_name):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE channels SET channel_name=%s, updated_at=NOW() WHERE channel_id=%s;"
                cur.execute(sql, (channel_name, cid))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

# メッセージクラス
class Message:
    
    @classmethod
    def create(cls, uid, cid, message):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO messages(user_id, channel_id, message_content) VALUES(%s, %s, %s)"
                cur.execute(sql, (uid, cid, message,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_all(cls, cid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                    SELECT message_id, u.user_id, user_name, message_content, m.created_at
                    FROM messages AS m 
                    INNER JOIN users AS u ON m.user_id = u.user_id
                    WHERE channel_id = %s AND m.created_at > NOW() - INTERVAL 10 MINUTE
                    ORDER BY message_id ASC;
                """
                cur.execute(sql, (cid,))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    @classmethod
    def find_by_id(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM messages WHERE message_id=%s;"
                cur.execute(sql, (message_id,))
                message = cur.fetchone()
                return message
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, message_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM messages WHERE message_id=%s;"
                cur.execute(sql, (message_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def update(cls, message_id, message_content):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE messages SET message_content=%s WHERE message_id=%s;"
                cur.execute(sql, (message_content, message_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)