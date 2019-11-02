# coding=utf-8
# scrapy-redis 使用说明文档
'''
-------------------------准备工作------------------:
自己下载：
# clone github scrapy-redis源码文件
git clone https://github.com/rolando/scrapy-redis.git
# 直接拿官方的项目范例，改名为自己的项目用
mv scrapy-redis/example-project ~/scrapy-youyuan

或者：

直接用本文件里下载好的 scrapy-redis 文件


安装模块：
pip install scrapy scrapy-redis


# ------------------------修改-----------------------
可以提前写好scrapy爬虫，做分布式时  直接修改 settings.py  和  spider.py

修改 settings.py:
复制scrapy-redis文件里示例的 settings.py 内容，替换掉自己写的scrapy爬虫配置文件， 修改里边爬虫名；
具体区别可以看 jin_ri_tui_jian 爬虫里的 settings.py

修改 spider.py:
# ----1 导入scrapy_redis类
# ----2 修改继承类
# ----3 注销允许的域名和起始的URL列表
# ----4 编写__init__,动态获取允许的域名
# ----5 编写redis_key，用于从redis中获取起始url

具体区别可以看 jin_ri_tui_jian 爬虫里的 jrtj.py


#  ------------------------------- 保存数据 ----------------------：
jin_ri_tui_jian ----- save_data.py  文件里

直接运行此文件




'''
