from flask import abort
import pymysql
from util.DB import DB

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

    
