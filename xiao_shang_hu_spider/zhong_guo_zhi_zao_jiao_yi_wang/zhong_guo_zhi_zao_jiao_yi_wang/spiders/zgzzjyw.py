# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from zhong_guo_zhi_zao_jiao_yi_wang.items import ZhongGuoZhiZaoJiaoYiWangItem
import re


class ZgzzjywSpider(scrapy.Spider):
    name = 'zgzzjyw'
    allowed_domains = ['www.c-c.com',
                       'ce.c-c.com']
    start_urls = ['http://www.c-c.com']
    # start_urls = ['http://nchxfh.ce.c-c.com/']
    '''
    http://dongzuoshijuhui86949.ce.c-c.com/
    http://tjjinzhongji.ce.c-c.com/
    http://nchxfh.ce.c-c.com/
    '''


    def parse(self, response):
        # 所有大类
        max_class_list = response.xpath('//div[@class="category"]/ul//li[@class="cate-item"]/div[1]')
        print('--- len(max_class_list) = ', len(max_class_list))
        if max_class_list != []:
            for max_class in max_class_list:
                min_url = max_class.xpath('.//a/@href').extract()[0]
                # print('min_url = ', min_url)
                yield scrapy.Request(url=min_url, callback=self.parse_min_class)

    def parse_min_class(self, response):
        # 所有小类
        print('***** ', response.url)
        min_result = response.body.decode('utf-8')
        # print('****** ', min_result)
        min_html = etree.HTML(min_result)
        min_class_list = min_html.xpath('//div[@class="gq-con"]//div[@class="gq-txt clearfix "]/div//a')
        print('+++ len(min_class_list) = ', len(min_class_list))
        if min_class_list != []:
            for min_class in min_class_list:
                page_list = min_class.xpath('./@href')
                if page_list != []:
                    page_url = 'http://www.c-c.com' + page_list[0]
                    print('page_url = ', page_url)
                    yield scrapy.Request(url=page_url, callback=self.parse_page_data)

    def parse_page_data(self, response):
        # 页面列表信息    翻页
        print('>>>>> ', response.url)
        n_url = response.xpath('//a[@class="page-next"]/@href')
        # print('--->>> n_url = ', n_url )
        data_list = response.xpath('//div[@class="goods-list mt10"]//div[@class="gimg-itm"]')
        if data_list != []:
            for data in data_list:
                data_url = data.xpath('.//div[@class="gg-cdr clearfix"]/a/@href')
                if data_url != []:
                    d_url = data_url.extract()[0]
                    print('d_url = ', d_url)
                    yield scrapy.Request(url=d_url, callback=self.parse_data, meta={'data_info_url': d_url})
        # 翻页
        if n_url != []:
            next_url = 'http://www.c-c.com' + n_url.extract()[0]
            print('next_url = ', next_url)
            yield scrapy.Request(url=next_url, callback=self.parse_page_data)

    def parse_data(self, response):
        # 详细信息
        # print('************* ', response.body, '**************')
        print('===== ', response.url)
        # response = response.body.decode('utf-8')
        # data_info_list = response.xpath('//ul[@class="com-info"]//li')
        # print('********* ', len(data_info_list))

        # if data_info_list != []:
        item = ZhongGuoZhiZaoJiaoYiWangItem()
        # item['page_url'] = response.meta['pa_url']
        # 爬取对应官网名称(siteName) 例： 阿里巴巴商友圈
        item['siteName'] = '中国制造交易网'
        # 爬取对应官网链接(webLinks) 例： https://club.1688.com/
        item['webLinks'] = 'http://www.c-c.com/'
        # 对应详情页链接(detailLink)：  	https://qiye.gongchang.com/hongyipu/contact/
        item['detailLink'] = response.meta['data_info_url']
        # 企业名称:(companyName)			中国科学器材有限公司
        item['companyName'] = ''
        companyName = response.xpath('//ul[@class="com-info"]/li[1]/a/text()').extract()
        if companyName == []:
            pass
        else:
            item['companyName'] = companyName[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '')

        # print('************ ', item['companyName'])
        # 企业英文名：(companyEnglishName)			China National Scientific Instruments and Materials Co., Ltd
        item['companyEnglishName'] = ''
        # 注册类型：(registrationType)		供应商
        item['registrationType'] = ''
        registrationType = response.xpath('//ul[@class="com-info"]/li[7]/text()').extract()
        if registrationType == []:
            pass
        else:
            item['registrationType'] = registrationType[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '')

        # 企业性质：(companyType)			国有绝对控股企业
        item['companyType'] = ''
        # 成立时间:(establishedTime)   		2015-07-22
        item['establishedTime'] = ''
        # 营业执照号:(businessLicenseNo)			91331102350072370U
        item['businessLicenseNo'] = ''
        # 经营模式：(businessModel)			贸易型
        item['businessModel'] = ''
        businessModel = response.xpath('//ul[@class="com-info"]/li[5]/text()').extract()
        if businessModel != []:
            item['businessModel'] = businessModel[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '')
        # 注册资本：(registeredCapital)			400000.000000 万元
        item['registeredCapital'] = ''
        registeredCapital = response.xpath('//ul[@class="com-info"]/li[6]/text()').extract()
        if registeredCapital != []:
            item['registeredCapital'] = registeredCapital[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '')
        # 雇员人数：(employee)			301-500 人
        item['employee'] = ''
        # 主营产品：(mainProducts)			理化分析仪器、光学仪器、电子仪器及配件、生物技术及生物工程设备、计算机及附属设备
        item['mainProducts'] = ''
        mainProducts = response.xpath('//ul[@class="com-info"]/li[8]/a/text()').extract()
        if mainProducts != []:
            item['mainProducts'] = mainProducts[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '')
        # 企业网址：(Website)			www.csimc.com.cn
        item['Website'] = ''
        # ----------------------------------------------------------------------------------------------------------
        # 联 系 人：(contact)			雷靖行
        item['contact'] = ''
        contact = response.xpath('//*[@id="dialogBody"]/div[1]/ul/li[1]/b/text()').extract()
        if contact == []:
            contact = response.xpath('//ul[@class="com-info"]/li[3]/text()').extract()
            if contact == []:
                # print('contact -- 3', contact)
                contact = response.xpath('/html/body/div[6]/div[2]/div[2]/div[3]/div[3]/ul/li[2]/text()').extract()
                if contact != []:
                    item['contact'] = contact[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t', '').replace('\r', '').replace('联系人', '')
            else:
                # print('contact -- 2', contact)
                item['contact'] = ''.join(contact).replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        else:
            # print('contact -- 1', contact)
            item['contact'] = contact[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '')
        # 手机号码：(phoneNumber)			18117451540
        item['phoneNumber'] = ''
        phoneNumber = response.xpath('//ul[@class="com-info"]/li[11]/span/text()').extract()
        if phoneNumber == []:
            phoneNumber = response.xpath('//*[@id="dialogBody"]/div[1]/ul/li[4]/text()').extract()
            if phoneNumber != []:
                # print('phoneNumber -- 2', phoneNumber)
                item['phoneNumber'] = re.findall(r'\d+', phoneNumber[0])[0]
        else:
            # print('phoneNumber -- 1', phoneNumber)
            item['phoneNumber'] = phoneNumber[0].replace(':', '').replace('：', '').replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '').replace('手机', '')
        # 联系电话：(telephone)			0755-00000000
        item['telephone'] = ''
        telephone = response.xpath('//*[@id="dialogBody"]/div[1]/ul/li[2]/text()').extract()
        if telephone == []:
            pass
        else:
            item['telephone'] = telephone[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r','')
        # 公司传真：(companyFax)			0755-00000000
        item['companyFax'] = ''

        companyFax = response.xpath('//ul[@class="com-info"]/li[12]/span/text()').extract()
        if companyFax == []:
            companyFax = response.xpath('/html/body/div[6]/div[2]/div[2]/div[3]/div[3]/ul/li[4]/text()').extract()
            if companyFax == []:
                companyFax = response.xpath('//*[@id="dialogBody"]/div[1]/ul/li[3]/text()').extract()
                if companyFax != []:
                    item['companyFax'] = companyFax[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t','').replace('\r', '').replace('传真', '')
            else:
                # print('companyFax -- 2', companyFax)
                item['companyFax'] = companyFax[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t', '').replace('\r','').replace('传真', '')
        else:
            # print('companyFax -- 1', companyFax)
            item['companyFax'] = companyFax[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t','').replace('\r', '').replace('传真', '')
        # E-MAIL  : (Email)  		18641572818@163.com
        item['Email'] = ''
        Email = response.xpath('//ul[@class="com-info"]/li[13]/span/text()').extract()
        # Email = response.xpath('//div[@class="loginwrap"]div[1]/ul/li[6]/text()').extract()
        if Email == []:
            Email = response.xpath('/html/body/div[6]/div[2]/div[2]/div[3]/div[3]/ul/li[7]/text()').extract()
            #/html/body/div[6]/div[2]/div[2]/div[3]/div[3]/ul/li[7]/text()
            # print('Email -- 2', Email)
            if Email == []:
                Email = response.xpath('//*[@id="dialogBody"]/div[1]/ul/li[6]/text()').extract()
                if Email != []:
                    # print('Email -- 3', Email)
                    # if ':' or Email[0] or '：' in Email[0]:
                    item['Email'] = Email[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t','').replace('\r', '').replace('邮箱', '')
            else:
                item['Email'] = Email[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t', '').replace('\r','').replace('邮箱', '')
        else:
            # print('Email -- 1', Email)
            item['Email'] = Email[0].replace(':', '').replace('：', '').replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r','').replace('邮箱', '')
        # 企业地址：(businessAddress)			北京市朝阳区太阳宫中路19号院1号楼4层
        item['businessAddress'] = ''
        businessAddress = response.xpath('//ul[@class="com-info"]/li[9]/text()').extract()
        if businessAddress == []:
            businessAddress = response.xpath('/html/body/div[6]/div[2]/div[2]/div[3]/div[3]/ul/li[6]/text()').extract()
            if businessAddress == []:
                businessAddress = response.xpath('//*[@id="dialogBody"]/div[1]/ul/li[5]/text()').extract()
                if businessAddress != []:
                    # print('businessAddress -- 3', businessAddress)
                    item['businessAddress'] = businessAddress[0].replace('\xa0', '').replace('\n', '').replace('\t','').replace('\r', '')
            else:
                # print('businessAddress -- 2', businessAddress)
                item['businessAddress'] = businessAddress[0].replace(':', '').replace('：', '').replace('\xa0', '').replace('\n', '').replace('\t','').replace('\r', '').replace('地址', '')
        else:
            # print('businessAddress -- 1', businessAddress)
            item['businessAddress'] = businessAddress[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '')
        # Q Q号 码：(qq)   		282278944
        item['qq'] = ''
        # 微信： (wechat)  		mdjx6673
        item['wechat'] = ''
        # 邮政编码：	(postcode)		210000
        item['postcode'] = ''
        # 客服旺旺：	(angelBeauty)		**********
        item['angelBeauty'] = ''


        print('item = ', item)

        if item['phoneNumber'] != '':
            yield item