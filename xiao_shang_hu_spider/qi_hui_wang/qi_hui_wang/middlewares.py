# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
from qi_hui_wang.proxy_test import Proxy_start
from qi_hui_wang.logging_app import *
import random, re
from qi_hui_wang.config_user_agent import web_user_agent



class QiHuiWangSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class QiHuiWangDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 更换User-agent
class RotateUserAgentMiddleware(UserAgentMiddleware):
    user_agent_list = web_user_agent
    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            # 记录
            print('Current UserAgent: ' + ua)
            logger.info('Current UserAgent: ' + ua)
            # request.headers.setdefault(b'User-Agent', ua)
            request.headers['User-Agent'] = ua


# 更换代理IP
class ProxyMiddleWare(HttpProxyMiddleware):
    """docstring for ProxyMiddleWare"""

    ps = Proxy_start()
    proxy_1 = ''

    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        proxy = self.ps.get_check_proxy()
        self.proxy_1 = proxy
        # logger.info("1、this is request ip: " + self.proxy_1)
        print("1、this is request ip: " + self.proxy_1)
        request.meta['proxy'] = self.proxy_1

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            try:
                # 查找问题IP
                proxy = re.search(".*?@(.*?)", self.proxy_1).group(1)
                # 删除问题IP
                error_msg = self.ps.delete_proxy(proxy)
                logger.info("问题 ip: " + proxy, error_msg)
            except:
                pass
            proxy_2 = self.ps.get_check_proxy()
            logger.info("2、this is response ip: " + proxy_2)
            print("2、this is response ip: " + proxy_2)
            # 对当前reque加上代理
            request.meta['proxy'] = proxy_2
            return request
        return response

