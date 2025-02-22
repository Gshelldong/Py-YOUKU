import pymysql
from .db_pool import POOL

class Mysql:
    def __init__(self):
        # 建立连接
        self.conn = POOL.connection()

        # 获取游标
        self.cursor = self.conn.cursor(
            pymysql.cursors.DictCursor
        )

    # 关闭游标\连接方法
    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def my_select(self, sql ,args = None):
        self.cursor.execute(sql, args)
        res = self.cursor.fetchall()
        return res

    def my_execute(self, sql, args):
        try:
            self.cursor.execute(sql, args)
        except Exception as e:
            print(e)
