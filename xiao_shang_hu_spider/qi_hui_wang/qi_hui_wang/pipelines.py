# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class QiHuiWangPipeline(object):
    # def process_item(self, item, spider):
        # return item
    def __init__(self, mongo_uri, mongo_port, mongo_db, collection_name, user_name, password):
        self.mongo_uri = mongo_uri
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.collection_name = collection_name
        self.user_name = user_name
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            collection_name=crawler.settings.get('COLLECTION_NAME'),
            user_name=crawler.settings.get('USER_NAME'),
            password=crawler.settings.get('PASSWORD'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.db.authenticate(name=self.user_name, password=self.password, mechanism='SCRAM-SHA-1')

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # print('11111 ', item)
        self.db[self.collection_name].update({'phoneNumber': item['phoneNumber']}, {'$set': dict(item)}, True)
        print('mongodb 保存成功 ')
        return item
