# -*- coding: utf-8 -*-
import scrapy
from yun_shang_wang.items import YunShangWangItem
import re


class YswSpider(scrapy.Spider):
    name = 'ysw'
    allowed_domains = ['www.ynshangji.com',
                       'ynshangji.com'
                       ]
    start_urls = ['http://www.ynshangji.com/']
    # start_urls = ['http://13281188246.ynshangji.com/liuyan/']


    '''
    http://shunda03.ynshangji.com/liuyan/
    http://zhisheng123.ynshangji.com/liuyan/
    ttp://13281188246.ynshangji.com/liuyan/
    
    '''

    def parse(self, response):
        # 大分类
        class_list = response.xpath('//ul[@class="m_zl"]//li//a')
        print('----- len(class_list)', len(class_list))
        if class_list != []:
            for min_class in class_list:
                p_d_url = min_class.xpath('./@href')
                if p_d_url != []:
                    page_data_url = p_d_url.extract()[0]
                    yield scrapy.Request(url=page_data_url, callback=self.parse_page_data)

    def parse_page_data(self, response):
        # 页面上列表  翻页
        print('***** ',response.url)
        data_list = response.xpath('//div[@class="s-list s-pro-list"]/ul//li')
        n_url = response.xpath('//div[@class="paging mb30"]/a[last()]/@href')
        print('**** len(data_list) = ', len(data_list))
        if data_list != []:
            for data_info in data_list:
                d_url = data_info.xpath('.//div[@class="company"]/a[2]/@href')
                if d_url != []:
                    data_url = d_url.extract()[0] + '/liuyan/'
                    yield scrapy.Request(url=data_url, callback=self.parse_data, meta={'info_url':data_url})

        # 翻页
        if n_url != []:
            next_url = 'http://www.ynshangji.com' + n_url.extract()[0]
            print('next_url = ', next_url)
            yield scrapy.Request(url=next_url, callback=self.parse_page_data)

    def parse_data(self, response):
        # 详细信息
        print('+++++ ', response.url)
        data_info = response.xpath('//table[@class="bgcolor3"]//tr')
        print('++++++++ ', len(data_info))
        # print('+++ ', response.body.decode('gbk'), '+++')

        item = YunShangWangItem()
        # 爬取对应官网名称(siteName) 例： 阿里巴巴商友圈
        item['siteName'] = '云商网'
        # 爬取对应官网链接(webLinks) 例： https://club.1688.com/
        item['webLinks'] = 'http://www.ynshangji.com/'
        # 对应详情页链接(detailLink)：  	https://qiye.gongchang.com/hongyipu/contact/
        item['detailLink'] = response.meta['info_url']
        data_list = response.xpath('//table[@id="viewAttribute"]//tr')
        # 企业名称:(companyName)			中国科学器材有限公司
        item['companyName'] = ''
        companyName = response.xpath('//table[@class="bgcolor3"]//tr[1]/td[2]/text()').extract()
        print('companyName = ', companyName)
        if companyName == []:
            companyName = response.xpath('//div[@id="bodyleft"]//li[1]/text()').extract()
            if companyName != []:
                item['companyName'] = companyName[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '')
        else:
            item['companyName'] = companyName[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '')

        # print('************ ', item['companyName'])
        # 企业英文名：(companyEnglishName)			China National Scientific Instruments and Materials Co., Ltd
        item['companyEnglishName'] = ''
        # 注册类型：(registrationType)		供应商
        item['registrationType'] = ''
        # 企业性质：(companyType)			国有绝对控股企业
        item['companyType'] = ''
        # 成立时间:(establishedTime)   		2015-07-22
        item['establishedTime'] = ''
        # 营业执照号:(businessLicenseNo)			91331102350072370U
        item['businessLicenseNo'] = ''
        # 经营模式：(businessModel)			贸易型
        item['businessModel'] = ''
        # 注册资本：(registeredCapital)			400000.000000 万元
        item['registeredCapital'] = ''
        # 雇员人数：(employee)			301-500 人
        item['employee'] = ''
        # 联 系 人：(contact)			雷靖行
        item['contact'] = ''
        contact = response.xpath('//table[@class="bgcolor3"]//tr[1]/td[4]/text()').extract()
        if contact == []:
            contact = response.xpath('//div[@id="bodyleft"]//li[3]/text()').extract()
            if contact != []:
                item['contact'] = contact[0].replace(' ', '').replace(':', '').replace('：', '').replace('\n', '').replace('\t', '').replace('\r', '').replace('联系人', '')
        else:
            item['contact'] = contact[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '')
        # 手机号码：(phoneNumber)			18117451540
        item['phoneNumber'] = ''
        phoneNumber = response.xpath('//table[@class="bgcolor3"]//tr[2]/td[4]/text()').extract()
        if phoneNumber == []:
            phoneNumber = response.xpath('//div[@id="bodyleft"]//li[5]/text()').extract()
            if phoneNumber != []:
                item['phoneNumber'] = phoneNumber[0].replace(' ', '').replace(':', '').replace('：', '').replace('\n', '').replace('\t', '').replace('\r', '').replace('手机', '')
        else:
            item['phoneNumber'] = phoneNumber[0].replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
        # 联系电话：(telephone)			0755-00000000
        item['telephone'] = ''
        telephone = response.xpath('//table[@class="bgcolor3"]//tr[2]/td[2]/text()').extract()
        if telephone == []:
            telephone = response.xpath('//div[@id="bodyleft"]//li[4]/text()').extract()
            if telephone != []:
                item['telephone'] = telephone[0].replace(' ', '').replace(':', '').replace('：', '').replace('\n', '').replace('\t', '').replace('\r','').replace('电话', '')
        else:
            item['telephone'] = telephone[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r','')
        # 公司传真：(companyFax)			0755-00000000
        item['companyFax'] = ''
        # E-MAIL  : (Email)  		18641572818@163.com
        item['Email'] = ''
        Email = response.xpath('//table[@class="bgcolor3"]//tr[3]/td[4]/text()').extract()
        if Email != []:
            if '系统已隐藏' not in Email[0]:
                item['Email'] = Email[0].replace('\n', '').replace('\t', '').replace('\r','')

        # Q Q号 码：(qq)   		282278944
        item['qq'] = ''
        qq = response.xpath('//table[@class="bgcolor3"]//tr[4]/td[4]/a/@href').extract()
        if qq == []:
            qq = response.xpath('//table[@class="bgcolor3"]//tr[4]/td[4]/a/img/@src').extract()
            if qq != []:
                item['qq'] = qq[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(':', ':').replace('：', ':').split(':')[2]
        else:
            item['qq'] = re.findall(r'uin=(.*?)&Site', qq[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', ''), re.DOTALL)[0]
        # 微信： (wechat)  		mdjx6673
        item['wechat'] = ''
        # 邮政编码：	(postcode)		210000
        item['postcode'] = ''
        # 客服旺旺：	(angelBeauty)		**********
        item['angelBeauty'] = ''
        # 主营产品：(mainProducts)			理化分析仪器、光学仪器、电子仪器及配件、生物技术及生物工程设备、计算机及附属设备
        item['mainProducts'] = ''
        # 企业地址：(businessAddress)			北京市朝阳区太阳宫中路19号院1号楼4层
        item['businessAddress'] = ''
        businessAddress = response.xpath('//table[@class="bgcolor3"]//tr[3]/td[2]/text()').extract()
        if businessAddress == []:
            businessAddress = response.xpath('//div[@id="bodyleft"]//li[6]/text()').extract()
            if businessAddress != []:
                item['businessAddress'] = businessAddress[0].replace(' ', '').replace(':', '').replace('：', '').replace('\xa0', '').replace('\n', '').replace('\t','').replace('\r', '').replace('地址', '')
        else:
            item['businessAddress'] = businessAddress[0].replace('\xa0', '').replace('\n', '').replace('\t','').replace('\r', '')
        # 企业网址：(Website)			www.csimc.com.cn
        item['Website'] = ''
        Website = response.xpath('//table[@class="bgcolor3"]//tr[5]/td[2]/a/@href').extract()
        if Website == []:
            pass
        else:
            item['Website'] = Website[0].replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', '')
        print('item = ', item)
        # if item['phoneNumber'] != '':
        yield item




