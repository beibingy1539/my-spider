'''
# -*- coding: utf-8 -*-

# Scrapy settings for jin_ri_tui_jian project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jin_ri_tui_jian'

SPIDER_MODULES = ['jin_ri_tui_jian.spiders']
NEWSPIDER_MODULE = 'jin_ri_tui_jian.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jin_ri_tui_jian (+http://www.yourdomain.com)'



# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16


# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jin_ri_tui_jian.middlewares.JinRiTuiJianSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'jin_ri_tui_jian.middlewares.JinRiTuiJianDownloaderMiddleware': 543,
     'jin_ri_tui_jian.middlewares.RandomUserAgent': 101,
    # 'jin_ri_tui_jian.middlewares.RandomProxy': 100,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'jin_ri_tui_jian.pipelines.JinRiTuiJianPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


DOWNLOAD_TIMEOUT = 180
DOWNLOAD_DELAY = 5
RANDOMIZE_DOWNLOAD_DELAY = True
# Disable cookies (enabled by default)
COOKIES_ENABLED = False
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

'''
# ---------------------------- 以上为普通 scrapy 爬虫 配置-----------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------- 以下为  scrapy-redis 分布式 配置-----------------------------------------------------------------------------------------
#coding:utf-8
# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

SPIDER_MODULES = ['jin_ri_tui_jian.spiders']
NEWSPIDER_MODULE = 'jin_ri_tui_jian.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'

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
   # 'jin_ri_tui_jian.pipelines.JinRiTuiJianPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_TIMEOUT = 180
DOWNLOAD_DELAY = 5
RANDOMIZE_DOWNLOAD_DELAY = True
# Disable cookies (enabled by default)
COOKIES_ENABLED = False
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

REDIS_URL = 'redis://192.168.3.9:6379'

# *****************************************************************************************************************
PROXIES = [
   # {"ip_port": "121.41.8.23:16816", "user_passwd": "morganna_mode_g:ggc22qxp"},
    {"ip_port": "61.135.217.7	80"},
    {"ip_port": "58.53.128.83	3128"},
    {"ip_port": "59.110.240.249:8080"},
]
USER_AGENT_LIST = [
'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3178.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3178.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3178.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3178.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Mozilla/5.0 (Linux; U; Android 4.3; zh-cn; R8007 Build/JLS36C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 4.3; zh-cn; R8007 Build/JLS36C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 V1_AND_SQ_5.0.0_146_YYB_D QQ/5.0.0.2215 ',
    'Mozilla/5.0 (Linux; U; Android 4.3; zh-cn; SM-N9009 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.3 Mobile Safari/537.36  ',
    'Mozilla/5.0 (Linux; Android 4.2.2; zh-cn; SCH-I959 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19',
    'Mozilla/5.0 (Linux; U; Android 4.3; zh-CN; SM-N9009 Build/JSS15J) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-CN; Coolpad 5891 Build/JZO54K) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.9.3.478 U3/0.8.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-CN; Coolpad 5891 Build/JZO54K) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.9.3.478 U3/0.8.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; Coolpad 5891 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 V1_AND_SQ_5.0.0_146_YYB2_D QQ/5.0.0.2215',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 QQ/5.0.0.165',
    'Mozilla/5.0 (Linux; Android 4.3; zh-cn; SAMSUNG-GT-I9308_TD/1.0 Android/4.3 Release/11.15.2013 Browser/AppleWebKit534.30 Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 4.1.1; zh-cn; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 SogouMSE,SogouMobileBrowser/3.2.3',
    'Mozilla/5.0 (Linux; U; Android 4.2.2; zh-cn; SCH-I959 Build/JDQ39) AppleWebKit/534.24 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.24 T5/2.0 baidubrowser/5.0.3.10 (Baidu; P1 4.2.2)',
    'Mozilla/5.0 (Linux; U; Android 4.2.2; zh-cn; SCH-I959 Build/JDQ39) AppleWebKit/534.24 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.24 T5/2.0',
    'Mozilla/5.0 (Linux; Android 4.3; SM-N9009 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.117 Mobile Safari/537.36 OPR/24.0.1565.82529',
    'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-CN; Nexus 4 Build/KTU84P) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; zh-cn; HUAWEI C8825D Build/HuaweiC8825D) AppleWebKit/534.24 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.24 T5/2.0 baidubrowser/5.2.3.0 (Baidu; P1 4.0.4)',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; zh-cn; HUAWEI C8825D Build/HuaweiC8825D) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.3 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.0.4; HUAWEI C8825D Build/HuaweiC8825D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.117 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; zh-cn; HUAWEI C8825D Build/HuaweiC8825D) AppleWebKit/535.19 (KHTML, like Gecko) Version/4.0 LieBaoFast/2.12.0 Mobile Safari/535.19',
    'Opera/9.80 (Android; Opera Mini/7.0.31907/34.2499; U; zh) Presto/2.8.119 Version/11.10',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; zh-cn; HW-HUAWEI_C8825D/C8825DV100R001C92B943SP01; 480*800; CTC/2.0) AppleWebKit/534.30 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-CN; SGP521 Build/17.1.2.A.0.314) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; Android 4.4.2; SGP521 Build/17.1.2.A.0.314) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.117 Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; zh-CN; HUAWEI C8825D Build/HuaweiC8825D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.8.5.442 U3/0.8.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 4.1.1; zh-cn; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; Android 4.4.2; zh-cn; SAMSUNG-SM-N9009 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.2.2; zh-CN; HTC HTL22 Build/JDQ39) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; Android 4.3; SM-N9009 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.117 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.2.1; zh-cn; AMOI A920W Build/JOP40D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; Android 4.3; SM-N9009 Build/JSS15J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.135 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.1.1; zh-CN; GT-N7100 Build/JRO03C) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Linux; U; Android 4.3; zh-cn; R8007 Build/JLS36C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'


]