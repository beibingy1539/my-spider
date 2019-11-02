# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WangShangZhiChuangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 爬取对应官网名称(siteName) 例： 阿里巴巴商友圈
    siteName = scrapy.Field()
    # 爬取对应官网链接(webLinks) 例： https://club.1688.com/
    webLinks = scrapy.Field()
    # 对应详情页链接(detailLink)：  	https://qiye.gongchang.com/hongyipu/contact/
    detailLink = scrapy.Field()
    # 企业名称:(companyName)			中国科学器材有限公司
    companyName = scrapy.Field()
    # 企业英文名：(companyEnglishName)			China National Scientific Instruments and Materials Co., Ltd
    companyEnglishName = scrapy.Field()
    # 注册类型：(registrationType)		供应商
    registrationType = scrapy.Field()
    # 企业性质：(companyType)			国有绝对控股企业
    companyType = scrapy.Field()
    # 成立时间:(establishedTime)   		2015-07-22
    establishedTime = scrapy.Field()
    # 营业执照号:(businessLicenseNo)			91331102350072370U
    businessLicenseNo = scrapy.Field()
    # 经营模式：(businessModel)			贸易型
    businessModel = scrapy.Field()
    # 注册资本：(registeredCapital)			400000.000000 万元
    registeredCapital = scrapy.Field()
    # 雇员人数：(employee)			301-500 人
    employee = scrapy.Field()
    # 联 系 人：(contact)			雷靖行
    contact = scrapy.Field()
    # 手机号码：(phoneNumber)			18117451540
    phoneNumber = scrapy.Field()
    # 联系电话：(telephone)			0755-00000000
    telephone = scrapy.Field()
    # 公司传真：(companyFax)			0755-00000000
    companyFax = scrapy.Field()
    # E-MAIL  : (Email)  		18641572818@163.com
    Email = scrapy.Field()
    # Q Q号 码：(qq)   		282278944
    qq = scrapy.Field()
    # 微信： (wechat)  		mdjx6673
    wechat = scrapy.Field()
    # 邮政编码：	(postcode)		210000
    postcode = scrapy.Field()
    # 客服旺旺：	(angelBeauty)		**********
    angelBeauty = scrapy.Field()
    # 主营产品：(mainProducts)			理化分析仪器、光学仪器、电子仪器及配件、生物技术及生物工程设备、计算机及附属设备
    mainProducts = scrapy.Field()
    # 企业地址：(businessAddress)			北京市朝阳区太阳宫中路19号院1号楼4层
    businessAddress = scrapy.Field()
    # 企业网址：(Website)			www.csimc.com.cn
    Website = scrapy.Field()

