# -*- coding: utf-8 -*-
import scrapy
from qi_hui_wang.items import QiHuiWangItem
import re


class QhwSpider(scrapy.Spider):
    name = 'qhw'
    allowed_domains = ['qihuiwang.com']
    start_urls = ['http://qihuiwang.com/']
    # start_urls = ['http://qtsy021.company.qihuiwang.com/contact.html']


    '''
    http://tjw_15110915010135.company.qihuiwang.com/contact.html
    http://savant.company.qihuiwang.com/contact.html
    http://chaoqiangqp.company.qihuiwang.com/contact.html
    http://qtsy021.company.qihuiwang.com/contact.html
    '''

    def parse(self, response):
        # 分类
        max_class_list = response.xpath('//ul[@class="nav-sub"]//li[@class="mCate"]//dd/a')
        print(' ---- len(max_class_list) = ', len(max_class_list))
        if max_class_list != []:
            for max_list in max_class_list:
                min_list_url = max_list.xpath('./@href')   # 进入列表页
                if min_list_url != []:
                    m_l_url = min_list_url.extract()[0]
                    yield scrapy.Request(url=m_l_url, callback=self.parse_min)

    def parse_min(self, response):
        # 列表页  翻页
        print('***** ', response.url)
        min_class_list = response.xpath('//div[@class="productShowGrid"]/ul//li//div[@class="companyName"]')
        n_url = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href')
        if min_class_list != []:
            for min_list in min_class_list:
                data_url = min_list.xpath('./a/@href')
                if data_url != []:
                    d_url = data_url.extract()[0] + '/contact.html'
                    yield scrapy.Request(url=d_url, callback=self.parse_data, meta={'data_info_url':d_url})

        # 翻页
        if n_url != []:
            next_url = 'http://product.qihuiwang.com' + n_url.extract()[0]
            print('** next_utl = ', next_url)
            yield scrapy.Request(url=next_url, callback=self.parse_min)



    def parse_data(self, response):
        print('++++++ ', response.url)

        item = QiHuiWangItem()
        # 爬取对应官网名称(siteName) 例： 阿里巴巴商友圈
        item['siteName'] = '企汇网'
        # 爬取对应官网链接(webLinks) 例： https://club.1688.com/
        item['webLinks'] = 'http://www.qihuiwang.com/'
        # 对应详情页链接(detailLink)：  	https://qiye.gongchang.com/hongyipu/contact/
        item['detailLink'] = response.meta['data_info_url']    # 00000000000000000000000000
        # 企业名称:(companyName)			中国科学器材有限公司
        item['companyName'] = ''
        companyName = response.xpath('//div[@class="topQyInfoTel"]/h1/text()').extract()
        if companyName == []:
            companyName = response.xpath('//div[@class="companyName"]//h3/text()').extract()
            if companyName != []:
                item['companyName'] = companyName[0].replace('\n', '').replace('\t', '').replace('\r', '')
        else:
            item['companyName'] = companyName[0].replace('\n', '').replace('\t', '').replace('\r','')

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
        # 营业执照号:(businessLicenseNo)			91331102350072370U
        item['businessLicenseNo'] = ''
        # 经营模式：(businessModel)			贸易型
        item['businessModel'] = ''
        businessModel = response.xpath('//ul[@class="companyInfo"]/li[5]/p/text()').extract()
        if businessModel != []:
            item['businessModel'] = businessModel[0].replace('\n', '').replace('\t', '').replace('\r', '')
        # 注册资本：(registeredCapital)			400000.000000 万元
        item['registeredCapital'] = ''
        # 雇员人数：(employee)			301-500 人
        item['employee'] = ''
        # 主营产品：(mainProducts)			理化分析仪器、光学仪器、电子仪器及配件、生物技术及生物工程设备、计算机及附属设备
        item['mainProducts'] = ''
        mainProducts = response.xpath('//ul[@class="companyInfo"]/li[4]//a/text()').extract()
        if mainProducts != []:
            item['mainProducts'] = '|'.join(mainProducts).replace('\n', '').replace('\t', '').replace('\r','').replace(' ', '').replace(':', '').replace('：', '')
        # 企业网址：(Website)			www.csimc.com.cn
        item['Website'] = ''
        # ----------------------------------------------------------------------------------------------------------
        # 联 系 人：(contact)			雷靖行
        item['contact'] = ''
        contact = response.xpath('//ul[@class="contactUs"]/li[1]/p/text()').extract()
        if contact == []:
            contact = response.xpath('//ul[@class="companyInfo"]/li[2]/p/text()').extract()
            if contact == []:
                # print('contact -- 3', contact)
                contact = response.xpath('//ul[@class="contactInfo"]/li[1]/text()').extract()
                if contact != []:
                    item['contact'] = contact[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '').replace(':', '').replace('：', '').replace('联系人', '')
            else:
                # print('contact -- 2', contact)
                item['contact'] = contact[0].replace('\n', '').replace('\t', '').replace('\r','').replace(' ', '')
        else:
            # print('contact -- 1', contact)
            item['contact'] = contact[0].replace('\n', '').replace('\t', '').replace('\r', '')
        # 手机号码：(phoneNumber)			18117451540
        item['phoneNumber'] = ''
        phoneNumber = response.xpath('//div[@class="topQyInfoTel"]//em/text()').extract()
        if phoneNumber == []:
            phoneNumber = response.xpath('//ul[@class="contactUs"]/li[2]/p/text()').extract()
            if phoneNumber == []:
                # print('phoneNumber -- 2', phoneNumber)
                phoneNumber = response.xpath('//ul[@class="contactInfo"]/li[2]/text()').extract()
                if phoneNumber != []:
                    phone = re.findall(r'\d+', phoneNumber[0].replace('\n','').replace('\t', '').replace('\r', '').replace(' ', ''), re.DOTALL)
                    if phone != []:
                        item['phoneNumber'] = phone[0].replace(':', '').replace('：', '').replace('\n','').replace('\t','').replace('\r', '').replace(' ', '')
            else:
                item['phoneNumber'] = phoneNumber[0].replace(':', '').replace('：', '').replace('\n','').replace('\t', '').replace('\r', '').replace(' ', '')
        else:
            # print('phoneNumber -- 1', phoneNumber)
            item['phoneNumber'] = phoneNumber[0].replace(':', '').replace('：', '').replace('\n','').replace('\t', '').replace('\r', '').replace(' ', '')
        # 联系电话：(telephone)			0755-00000000
        item['telephone'] = ''
        telephone = response.xpath('//*[@id="dialogBody"]/div[1]/ul/li[2]/text()').extract()
        if telephone == []:
            item['telephone'] = item['phoneNumber']

        # 公司传真：(companyFax)			0755-00000000
        item['companyFax'] = ''
        companyFax = response.xpath('//ul[@class="contactInfo"]/li[3]/text()').extract()
        if companyFax != []:
            item['companyFax'] = companyFax[0].replace(':', '').replace('：', '').replace('\n','').replace('\t', '').replace('\r', '').replace(' ', '').replace('传真', '')

        # E-MAIL  : (Email)  		18641572818@163.com
        item['Email'] = ''
        Email = response.xpath('//ul[@class="contactInfo"]/li[4]/text()').extract()
        # Email = response.xpath('//div[@class="loginwrap"]div[1]/ul/li[6]/text()').extract()
        if Email == []:
            pass
        else:
            # print('Email -- 1', Email)
            item['Email'] = Email[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t', '').replace('\r', '').replace('邮箱', '').replace('电子邮件', '')
        # 企业地址：(businessAddress)			北京市朝阳区太阳宫中路19号院1号楼4层
        item['businessAddress'] = ''
        businessAddress = response.xpath('//ul[@class="contactInfo"]/li[5]/text()').extract()
        if businessAddress == []:
            businessAddress = response.xpath('//ul[@class="companyInfo"]/li[6]//a/text()').extract()
            if businessAddress != []:
                item['businessAddress'] = ''.join(businessAddress).replace(':', '').replace('：', '').replace('\n','').replace('\t','').replace('\r', '')
        else:
            # print('businessAddress -- 1', businessAddress)
            item['businessAddress'] = businessAddress[0].replace(':', '').replace('：', '').replace('\n', '').replace('\t', '').replace('\r', '').replace('地址', '')

        # Q Q号 码：(qq)   		282278944
        item['qq'] = ''
        if 'qq' in item['Email']:
            try:
                item['qq'] = str(int(item['Email'].replace('www.', '').replace('@qq.com', '')))
            except:
                pass
        # 微信： (wechat)  		mdjx6673
        item['wechat'] = ''
        # 邮政编码：	(postcode)		210000
        item['postcode'] = ''
        # 客服旺旺：	(angelBeauty)		**********
        item['angelBeauty'] = ''

        print('item = ', item)
        # if item['phoneNumber'] != '':
        yield item
