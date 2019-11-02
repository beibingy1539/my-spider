#coding:utf-8
# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'

# 启用scrapy_redis的重复过滤器,那么这个时候，原来的过滤器将会被停用
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 替换调度器为scrapy_redis的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 是否能从从断点(断掉的地方)继续爬取
SCHEDULER_PERSIST = True
# # 优先级队列
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# # 普通队列
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# # 栈
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = {
    'example.pipelines.ExamplePipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 3

REDIS_URL = 'redis://172.16.123.128:6379'
