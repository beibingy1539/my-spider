# -*- coding: utf-8 -*-
'''
今日推荐
http://www.365128.com/
'''
import scrapy
import time
# ----1 导入scrapy_redis类
import sys
sys.path.append('C:\\Users\\ly115\\Desktop\\20181111\\scrapy-redis')
from scrapy_redis.spiders import RedisSpider
from jin_ri_tui_jian.items import JinRiTuiJianItem

# ----2 修改继承类
# class JrtjSpider(scrapy.Spider):
class JrtjSpider(RedisSpider):
    name = 'jrtj'
    # ----3 注销允许的域名和起始的URL列表
    # allowed_domains = ['www.365128.com',
    #                    'm.365128.com'
    #                    ]
    # start_urls = ['http://m.365128.com/']

    # ----4 编写__init__,动态获取允许的域名
    def __init__(self, *args, **kwargs):
        # 获取域名
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        # 调用父类初始化方法
        super(JrtjSpider, self).__init__(*args, **kwargs)

    # ----5 编写redis_key，用于从redis中获取起始url
    redis_key = "jrtj:start_urls"

    def parse(self, response):
        # 大分类列表
        class_list = response.xpath('//div[@class="nr1"]//div[@id="dl"]/ul//li')
        print('---> len(class_list) - ', len(class_list))
        if class_list != []:
            for c in range(len(class_list)):
                c_list = class_list[c]
                # http://m.365128.com/fz.php?f=3701000
                c_h = c_list.xpath('./a/@href').extract()[0]
                if 'http' in c_h or 'fz' not in c_h:
                    pass
                else:
                    time.sleep(10)
                    class_url = 'http://m.365128.com/' + c_h
                    print('---> class_url = ', class_url)
                    yield scrapy.Request(url=class_url, callback=self.parse_min_class)

    def parse_min_class(self, response):
        # 小分类连接
        min_class_list = response.xpath('//div[@class="nr1"][2]//li')
        if min_class_list != []:
            for m in range(len(min_class_list)):
                m_list = min_class_list[m]
                m_h = m_list.xpath('./strong/a/@href').extract()[0]
                time.sleep(10)
                min_class_url = 'http://m.365128.com/' + m_h
                item = JinRiTuiJianItem()
                print('>>>>>> 下一个是 %s' % m)
                print('++++++++++ > min_class_url = ', min_class_url)
                item['min_class_url'] = min_class_url
                yield item



