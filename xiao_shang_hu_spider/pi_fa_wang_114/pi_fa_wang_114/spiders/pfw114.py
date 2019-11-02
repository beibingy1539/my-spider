# -*- coding: utf-8 -*-
import scrapy
from pi_fa_wang_114.items import PiFaWang114Item
import re


class Pfw114Spider(scrapy.Spider):
    name = 'pfw114'
    allowed_domains = ['114pifa.com']
    start_urls = ['http://114pifa.com/']
    # start_urls = ['http://www.114pifa.com/ca/xiangjiakeji']


    '''
    http://www.114pifa.com/ca/leerfilter
    http://www.114pifa.com/ca/sindry
    http://www.114pifa.com/ca/xiangjiakeji
    '''

    def parse(self, response):
        # 大类
        max_class_lsit = response.xpath('//ul[@class="cate_list"]//li//div[@class="detail"]//a')
        print('----- len(max_class_lsit)', len(max_class_lsit))
        if max_class_lsit != []:
            for max_class in max_class_lsit:
                min_class_url = max_class.xpath('./@href')
                if min_class_url != []:
                    m_c_url = 'http://www.114pifa.com' + min_class_url.extract()[0]
                    yield scrapy.Request(url=m_c_url, callback=self.parse_min)

    def parse_min(self, response):
        # 小类
        print('***** ', response.url)
        min_class_list = response.xpath('//ul[@class="classifyList"]//dl')
        if min_class_list != []:
            for min_class in min_class_list:
                page_data_url = min_class.xpath('./a/@href')
                if page_data_url != []:
                    p_d_url = 'http://www.114pifa.com' + page_data_url.extract()[0]
                    yield scrapy.Request(url=p_d_url, callback=self.parse_page_data)

    def parse_page_data(self, response):
        # 页面上 列表  翻页\
        print('##### ', response.url)
        data_list = response.xpath('//ul[@class="searchResultList"]//p[@class="companyName"]')
        if data_list != []:
            for data in data_list:
                info_url = data.xpath('./a/@href')
                if info_url != []:
                    i_url = 'http://www.114pifa.com' + info_url.extract()[0].replace('/c/', '/ca/')
                    # http://www.114pifa.com/c/sdhyzg1234
                    # http://www.114pifa.com/ca/sdhyzg1234
                    # /c/sdhyzg1234
                    yield scrapy.Request(url=i_url, callback=self.parse_data, meta={'data_info_url': i_url})

        # 翻页
        n_data = response.xpath('//div[@class="pages"]/a[last() - 1]/text()')
        if n_data != []:
            next_data = n_data.extract()[0].replace('\n', '').replace('\t', '').replace('\r','')
            if next_data == '>':
                n_url = response.xpath('//div[@class="pages"]/a[last() - 1]/@href')
                if n_url != []:
                    next_url = 'http://www.114pifa.com' + n_url.extract()[0]
                    print('## next_url = ', next_url)
                    yield scrapy.Request(url=next_url, callback=self.parse_page_data)




    def parse_data(self, response):
        # 详细信息
        print('+++++ ', response.url)
        # 下方联系我们
        # down_data = response.xpath('//div[@class="contact-way1 basetitle basemarb"]//p')
        # 详细信息
        basetitle_data = response.xpath('//div[@class="basetitle"]//ul//li')
        b_data_dict = {}
        if basetitle_data != []:
            for b_data in basetitle_data:
                k = b_data.xpath('./span/text()').extract()
                v = b_data.xpath('./text()').extract()
                # print(k, '\n', v)
                if k != [] and v != []:
                    b_data_dict[k[0]] = ''.join(v).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        print('++ b_data_dict = ', b_data_dict)

        item = PiFaWang114Item()
        # 爬取对应官网名称(siteName) 例： 阿里巴巴商友圈
        item['siteName'] = '114批发网'
        # 爬取对应官网链接(webLinks) 例： https://club.1688.com/
        item['webLinks'] = 'http://www.114pifa.com/'
        # 对应详情页链接(detailLink)：  	https://qiye.gongchang.com/hongyipu/contact/
        item['detailLink'] = response.meta['data_info_url']  # 00000000000000000000000000
        # 企业网址：(Website)			www.csimc.com.cn
        item['Website'] = item['detailLink']
        # 企业名称:(companyName)			中国科学器材有限公司
        item['companyName'] = ''
        companyName = response.xpath('//div[@class="contact-way1 basetitle basemarb"]/p[1]/text()').extract()
        if companyName == []:
            companyName = response.xpath('//div[@class="info-detail"]/p[1]/a/text()').extract()
            if companyName == []:
                companyName = response.xpath('//div[@class="com-name"]/text()').extract()
                if companyName != []:
                    item['companyName'] = companyName[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
            else:
                item['companyName'] = companyName[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        else:
            item['companyName'] = companyName[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')

        # print('************ ', item['companyName'])
        # 企业英文名：(companyEnglishName)			China National Scientific Instruments and Materials Co., Ltd
        item['companyEnglishName'] = ''
        # 注册类型：(registrationType)		供应商
        item['registrationType'] = ''
        registrationType = response.xpath('//ul[@class="com-info"]/li[7]/text()').extract()
        # 企业性质：(companyType)			国有绝对控股企业
        item['companyType'] = ''
        # 成立时间:(establishedTime)   		2015-07-22
        item['establishedTime'] = ''
        try:
            item['establishedTime'] = b_data_dict['成立时间:']
        except:
            pass
        # 营业执照号:(businessLicenseNo)			91331102350072370U
        item['businessLicenseNo'] = ''

        # 经营模式：(businessModel)			贸易型
        item['businessModel'] = ''
        try:
            item['businessModel'] = b_data_dict['经营模式:']
        except:
            pass
        # 注册资本：(registeredCapital)			400000.000000 万元
        item['registeredCapital'] = ''
        # 雇员人数：(employee)			301-500 人
        item['employee'] = ''
        try:
            item['employee'] = b_data_dict['员工人数:']
        except:
            pass
        # 主营产品：(mainProducts)			理化分析仪器、光学仪器、电子仪器及配件、生物技术及生物工程设备、计算机及附属设备
        item['mainProducts'] = ''
        # 联 系 人：(contact)			雷靖行
        item['contact'] = ''
        contact = response.xpath('//div[@class="contact-way1 basetitle basemarb"]/p[2]/small/text()').extract()
        if contact == []:
            contact = response.xpath('//div[@class="info-detail"]/p[2]/span[1]/text()').extract()
            if contact != []:
                # print('contact -- 2', contact)
                item['contact'] = contact[0].split(' ')[0].replace('\n', '').replace('\t', '').replace('\r', '').replace('\xa0', '')
        else:
            # print('contact -- 1', contact)
            c = contact[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '').split('(')[0].replace('\xa0', '')
            # print('--------------', c)
            if '（' in c:
                item['contact'] = c.split('（')[0]
            elif '(' in c:
                item['contact'] = c.split('(')[0]
            else:
                item['contact'] = c
        # 手机号码：(phoneNumber)			18117451540
        item['phoneNumber'] = ''
        phoneNumber = response.xpath('//div[@class="contact-way1 basetitle basemarb"]/p[3]/small/text()').extract()
        if phoneNumber == []:
            phoneNumber = response.xpath('//div[@class="info-detail"]/p[2]/span[2]/text()').extract()
            if phoneNumber == []:
                # print('phoneNumber -- 2', phoneNumber)
                item['phoneNumber'] = re.findall(r'\d+', phoneNumber[0], re.DOTALL)[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t','').replace('\r', '').replace(' ', '')
        else:
            # print('phoneNumber -- 1', phoneNumber)
            item['phoneNumber'] = phoneNumber[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t','').replace('\r', '').replace(' ', '')
        # 联系电话：(telephone)			0755-00000000
        item['telephone'] = ''
        telephone = response.xpath('//div[@class="contact-way1 basetitle basemarb"]/p[4]/small/text()').extract()
        if telephone == []:
            telephone = response.xpath('//div[@class="info-detail"]/p[3]/text()').extract()
            if telephone != []:
                item['telephone'] = re.findall('\d+', telephone[0], re.DOTALL)[0]
        else:
            item['telephone'] = telephone[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t','').replace('\r', '').replace(' ', '')
        # 公司传真：(companyFax)			0755-00000000
        item['companyFax'] = ''
        companyFax = response.xpath('//div[@class="contact-way1 basetitle basemarb"]/p[5]/small/text()').extract()
        if companyFax == []:
            companyFax = response.xpath('//div[@class="info-detail"]/p[4]/text()').extract()
            if companyFax != []:
                item['companyFax'] = re.findall(r'\d+', companyFax[0], re.DOTALL)[0]
        else:
            item['companyFax'] = companyFax[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t','').replace('\r', '').replace(' ', '')
        # E-MAIL  : (Email)  		18641572818@163.com
        item['Email'] = ''
        # 企业地址：(businessAddress)			北京市朝阳区太阳宫中路19号院1号楼4层
        item['businessAddress'] = ''
        businessAddress = response.xpath('//div[@class="contact-way1 basetitle basemarb"]/p[6]/small/text()').extract()
        if businessAddress == []:
            pass
            # print('businessAddress -- 1', businessAddress)
        else:
            item['businessAddress'] = businessAddress[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t', '').replace('\r', '')
        # Q Q号 码：(qq)   		282278944
        item['qq'] = ''
        # 微信： (wechat)  		mdjx6673
        item['wechat'] = ''
        # 邮政编码：	(postcode)		210000
        item['postcode'] = ''
        postcode = response.xpath('//div[@class="contact-way1 basetitle basemarb"]/p[7]/small/text()').extract()
        if postcode != []:
            item['postcode'] = postcode[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t', '').replace('\r', '')
        # 客服旺旺：	(angelBeauty)		**********
        item['angelBeauty'] = ''

        print('item = ', item)
        if item['phoneNumber'] != '':
            yield item













