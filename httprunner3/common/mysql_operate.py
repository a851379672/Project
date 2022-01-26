import pymysql
import re
import logging
import json
import pytest

from settings import *


class MysqlOperate:

    def __init__(self, extract_key, sql_statement):
        """
        读取config.json
        :param extract_key: extract_key
        :param sql_statement: sql
        """
        with open(TARGET_PATH, 'r', encoding="utf-8") as f:
            config_json = json.loads(f.read())
        self.sql = sql_statement
        self.key = extract_key
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
        :param: deal_with
        :return:
        """
        if deal_with.replace_(self.sql):
            self.sql = deal_with.replace_(self.sql)
        result = self.judge.handler(self.cursor, self.sql, self.db)
        try:
            assert value == result['count']
            logging.info(f'SQL影响行数: {result["count"]} 预期影响行数: {value} 断言成功!')
            deal_with.extract_(f'{self.key}_count', result['count'], None, deal_with)
            if result.get('value'):
                deal_with.extract_(f'{self.key}_value', result['value'], None, deal_with)
        except AssertionError:
            pytest.xfail(f'SQL断言失败: {AssertionError}')
        self.cursor.close()
        self.db.close()


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
                key = re.findall('select (.*?) from', sql.lower())[0]
                cursor_value = result.get(key)
                logging.info(f'SQL查询结果: {cursor_value}')
                return {'count': cursor.rowcount, 'value': cursor_value}
        else:
            return self.obj.handler(cursor, sql, db)


class Delete(Manager):

    def handler(self, cursor, sql, db):
        if sql.lower().startswith('delete'):
            cursor.execute(sql)
            db.commit()
            return {'count': cursor.rowcount}
        else:
            return self.obj.handler(cursor, sql, db)
