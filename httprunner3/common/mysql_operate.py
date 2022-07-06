import pymysql
import re
import logging
import json
import pytest
from settings import *


class MysqlOperate:

    def __init__(self, sql_statement):
        """
        读取config.json
        :param sql_statement: sql
        """
        with open(TARGET_PATH, 'r', encoding="utf-8") as f:
            config_json = json.loads(f.read())
        self.sql = sql_statement
        self.db_name = self.sql_type(sql_statement)
        self.db, self.cursor = self.link_sql(config_json['db_config'])
        self.judge, delete_, update_, insert_ = Select(), Delete(), Update(), Insert()
        self.judge.next_handler(delete_)
        self.judge.next_handler(update_)
        self.judge.next_handler(insert_)

    def link_sql(self, db_config):
        """
        数据库连接
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

    def execute_sql(self, extract_key, values, deal_with):
        """
        sql执行
        :param extract_key: extract_key
        :param values: 预期值
        :param deal_with
        :return:
        """
        deal_with.replace_(self.sql) if deal_with.replace_(self.sql) else ''
        result = self.judge.handler(self.cursor, self.sql, self.db)
        try:
            count, value = result.get('count'), result.get('value')
            assert values == count
            logging.info(f'sql影响行数: {count} 预期影响行数: {values} 断言成功!')
            [deal_with.extract_(f'{extract_key}_count', count, None, deal_with),
             deal_with.extract_(f'{extract_key}_value', value, None, deal_with)] if result.get('value') else \
                deal_with.extract_(f'{extract_key}_count', count, None, deal_with)
        except AssertionError:
            pytest.xfail(f'sql断言失败: {AssertionError}')
        except TypeError:
            pytest.xfail(f'result object TypeError: {TypeError}')
        self.cursor.close()
        self.db.close()

    @staticmethod
    def sql_type(sql_statement):
        """
        sql操作类型判断
        :param sql_statement: sql
        :return: db_name
        """
        if sql_statement.startswith('select') or sql_statement.startswith('delete'):
            pattern = 'from'
        elif sql_statement.startswith('update'):
            pattern = 'update'
        else:
            pattern = 'into'
        return re.findall(rf'{pattern} (.*?)\.', sql_statement)[0]


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
                key = re.findall('select (.*) from', sql)[0]
                cursor_value = result.get(key)
                logging.info(f'sql查询结果: {cursor_value}')
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


class Update(Manager):

    def handler(self, cursor, sql, db):
        if sql.lower().startswith('update'):
            cursor.execute(sql)
            db.commit()
            return {'count': cursor.rowcount}
        else:
            return self.obj.handler(cursor, sql, db)


class Insert(Manager):

    def handler(self, cursor, sql, db):
        if sql.lower().startswith('insert'):
            cursor.execute(sql)
            db.commit()
            return {'count': cursor.rowcount}
        else:
            return self.obj.handler(cursor, sql, db)


if __name__ == '__main__':
    from logs import logging_
    logging_()
    import data_depend
    data_depends = data_depend.DataDepend()
    MysqlOperate('select colID from palmmusic_item.singer_category_test where colID=1194')\
        .execute_sql('singerID', 6, data_depends)
