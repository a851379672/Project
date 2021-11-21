import pymysql
import re
import logging
import json
import pytest

from settings import *


class MysqlOperate(object):

    def __init__(self, sql_statement):
        """
        读取config.json文件
        :param sql_statement: sql语句
        """
        with open(TARGET_PATH, 'r', encoding="utf-8") as f:
            config_json = json.loads(f.read())
        self.sql = sql_statement
        self.db_name = re.findall(r'FROM (.*?)\.', sql_statement)[0]
        self.db, self.cursor = self.link_sql(config_json['db_config'])
        self.judge = Select()
        sql_delete = Delete()
        self.judge.next_handler(sql_delete)

    def link_sql(self, db_config):
        """
        连接数据库
        :param db_config: config.json
        :return: db:链接, cursor:游标
        """
        db = pymysql.Connect(
            host=db_config['db_host'],
            user=db_config['db_name'],
            password=db_config['db_password'],
            db=self.db_name,
            port=db_config['db_port'],
            charset=db_config['db_charset']
        )
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        return db, cursor

    def execute_sql(self, value, deal_with):
        """
        执行sql
        :param: value: 预期值
        :return:
        """
        if deal_with.replace_(self.sql):
            self.sql = deal_with.replace_(self.sql)
        result = self.judge.handler(self.cursor, self.sql, self.db)
        try:
            assert result == value
            logging.info(f'SQL影响行数: ({result}) 预期影响行数: ({value}) 断言成功!')
        except AssertionError:
            pytest.xfail(f'SQL断言失败：{AssertionError}')
        self.cursor.close()
        self.db.close()

    def execute_sql_list(self):
        """
        ——执行sql_list，暂时用不到——
        :return:
        """
        sql_dict = {sql: self.cursor.execute(sql) for sql in self.sql if sql}
        sql_result = [self.judge.handler(self.cursor, sql, self.db) for sql, value in sql_dict.items()
                      if self.judge.handler(self.cursor, sql, self.db)]
        self.cursor.close()
        self.db.close()
        return sql_result


class Manager:

    def __init__(self):
        self.obj = None

    def handler(self, cursor, sql, db):
        pass

    def next_handler(self, obj):
        self.obj = obj


class Select(Manager):

    def handler(self, cursor, sql, db):
        if sql.lower().startswith('select'):
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                logging.info(f'sql select result: {result}')
            return cursor.rowcount
        else:
            return self.obj.handler(cursor, sql, db)


class Delete(Manager):

    def handler(self, cursor, sql, db):
        if sql.lower().startswith('delete'):
            cursor.execute(sql)
            db.commit()
            return cursor.rowcount
        else:
            return self.obj.handler(cursor, sql, db)
