#!/usr/bin/env python
# coding=UTF-8
import pymysql
import pymysql.cursors
from DBUtils.PooledDB import PooledDB


ip = "127.0.0.1"
user_name = "root"
password = "abcd1234"
db_name = "test"


pool = PooledDB(pymysql, 2, 10, 10, 50,
                **{'host': ip, 'port': 3306, 'user': user_name, 'passwd': password,
                   'db': db_name, 'charset': 'utf8', 'cursorclass': pymysql.cursors.DictCursor})


class BaseDB(object):
    def __init__(self, conn=None, slave=False, bid=''):
        if conn:
            self.conn = conn
        else:
            self.conn = pool.connection()
        self.cur = self.conn.cursor()
        self.res = True

    def __del__(self):
        self.finish()

    def execute(self, sql, param=None):
        try:
            if 'select' not in sql.lower()[:7]:
                # logging.info(sql)
                pass
            else:
                pass
                # logging.info(sql)
                # logging.debug(sql)
            if not param:
                return self.cur.execute(sql)
            else:
                return self.cur.execute(sql, param)
        except:
            self.res = False
            return 0

    def get(self, sql, param=None):
        self.execute(sql, param)
        return self.cur.fetchone()

    def query(self, sql, param=None):
        self.execute(sql, param)
        return self.cur.fetchall()

    def update(self, table_name, set_data, where_data={}, limit=None):
        set_col_list = []
        for k, v in set_data.items():
            set_col_list.append("%s='%s'" % (k, v))
        set_sql = ",".join(set_col_list)
        where_data_list = []
        for k, v in where_data.items():
            where_data_list.append("%s='%s'" % (k, v))
        where_sql = "and ".join(where_data_list)
        sql = "update %s set %s" % (table_name, set_sql)
        if where_sql:
            sql += " where %s" % where_sql
        if limit:
            sql += " limit %s" % limit
        return self.execute(sql)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def finish(self):
        if self.res:
            self.conn.commit()
        else:
            self.conn.rollback()
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()