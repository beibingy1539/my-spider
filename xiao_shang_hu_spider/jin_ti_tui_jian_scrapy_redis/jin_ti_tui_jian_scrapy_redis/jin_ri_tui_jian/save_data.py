# coding=utf-8
# ------------------------ 存入 mysql ---------------------------
import json
import redis
import MySQLdb

def save_mysql():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='192.168.199.108', port = 6379, db = 0)
    # 指定mysql数据库
    mysqlcli = MySQLdb.connect(host='127.0.0.1', user='power', passwd='xxxxxxx', db = 'ly', port=3306, use_unicode=True)

    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["jrtj:items"])
        item = json.loads(data)

        try:
            # 读取redis中数据， 保存到 mysql 中
            # 使用cursor()方法获取操作游标
            cur = mysqlcli.cursor()
            # 使用execute方法执行SQL INSERT语句
            cur.execute("INSERT INTO beijing_18_25 (username, crawled, age, spider, header_url, source, pic_urls, monologue, source_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )", [item['username'], item['crawled'], item['age'], item['spider'], item['header_url'], item['source'], item['pic_urls'], item['monologue'], item['source_url']])
            # 提交sql事务
            mysqlcli.commit()
            #关闭本次操作
            cur.close()
            print "inserted %s" % item['source_url']
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# --------------------- 存入 mongodb ------------------------------------------------------------

import json
import redis
import pymongo

def save_mongodb():

    # 指定Redis数据库信息
    rediscli = redis.StrictRedis(host='192.168.199.108', port=6379, db=0)
    # 指定MongoDB数据库信息
    mongocli = pymongo.MongoClient(host='localhost', port=27017)

    # 创建数据库名
    db = mongocli['ly']
    # 创建表名
    sheet = db['jrtj']

    while True:
        # 读取redis中数据， 保存到 mongodb 中
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["jrtj:items"])

        item = json.loads(data)
        sheet.insert(item)

        try:
            print u"Processing: %(name)s <%(link)s>" % item
        except KeyError:
            print u"Error procesing: %r" % item













if __name__ == '__main__':
    save_mysql()
    save_mongodb()