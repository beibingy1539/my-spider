# -*- coding: utf-8 -*-
import scrapy
from wang_shang_zhi_chuang.items import WangShangZhiChuangItem
import re


class WszcSpider(scrapy.Spider):
    name = 'wszc'
    allowed_domains = ['53info.com']
    start_urls = ['http://www.53info.com/sell/']
    # start_urls = ['http://www.53info.com/com/qa7335/contact/']

    #    http://53info.com/

    '''
    http://www.53info.com/com/li19910225/contact/
    http://www.53info.com/com/qa7335/contact/
    http://www.53info.com/com/szfxcl1/contact/
    http://www.53info.com/com/qa7335/contact/
    '''

    def parse(self, response):
        # 大类
        class_list = response.xpath('//div[@class="profl"]//td[@valign="top"]//a')
        print('----- ', len(class_list))
        if class_list != []:
            for c_list in class_list:
                page_data_url = c_list.xpath('./@href')
                if page_data_url != []:
                    p_d_url = page_data_url.extract()[0]
                    yield scrapy.Request(url=p_d_url, callback=self.parse_page)

    def parse_page(self, response):
        # 列表    翻页
        data_list = response.xpath('//div[@class="list"]//ul/li[last()]')
        print('***** ', len(data_list))
        if data_list != []:
            for data in data_list:
                info_url = data.xpath('./a/@href')
                if info_url != []:
                    i_url = info_url.extract()[0] + 'contact/'
                    yield scrapy.Request(url=i_url, callback=self.parse_data, meta={'data_info_url':i_url})

        # 翻页
        n_data = response.xpath('//div[@class="pages"]/a[last()]/text()').extract()
        if n_data != []:
            next_data = n_data[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '').replace('\xa0', '')
            if '下一页»' in n_data[0] or '尾页' in n_data[0]:
                n_url = response.xpath('//div[@class="pages"]/a[last()]/@href').extract()
                if n_url != []:
                    next_url = n_url[0]
                    print('next_url = ', next_url)
                    yield scrapy.Request(url=next_url, callback=self.parse_page)


    def parse_data(self, response):
        print('+++++ ', response.url)
        # print(response.xpath('//div[@class="main_body"]//table//tr[8]/td[2]//a/@href').extract())
        datas = response.xpath('//div[@class="main_body"]//table//tr')
        if datas != []:
            data_dict = {}
            for d in datas:
                k = d.xpath('./td[1]/text()').extract()[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ','').replace('：', '').replace(':', '')
                vv = d.xpath('./td[2]/text()').extract()
                # [0].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ','').replace('：', '').replace(':', '')
                v = ''
                # print(k, '<---> ', vv)
                if vv == []:
                    vv = d.xpath('./td[2]//a/@href').extract()
                    if vv != []:
                        v = '-or-'.join(vv).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ','')
                else:
                    if vv == ['\r\n', '\xa0', '\xa0']:
                        vv = d.xpath('./td[2]//a/@href').extract()
                        if vv != []:
                            v = '-or-'.join(vv).replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
                    else:
                        v = vv[0].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ','').replace('：', '').replace(':', '')
                # print(k, '<---> ', v)

                data_dict[k] = v
            # print('++ data_dict = ', data_dict)

            item = WangShangZhiChuangItem()
            # 详细信息
            # 爬取对应官网名称(siteName) 例： 阿里巴巴商友圈
            item['siteName'] = '网商之窗'
            # 爬取对应官网链接(webLinks) 例： https://club.1688.com/
            item['webLinks'] = 'http://www.53info.com/'
            # 对应详情页链接(detailLink)：  	https://qiye.gongchang.com/hongyipu/contact/
            item['detailLink'] = response.meta['data_info_url']  # 00000000000000000000000000
            # 企业网址：(Website)			www.csimc.com.cn
            item['Website'] = ''
            if '公司网址' in data_dict.keys():
                item['Website'] = data_dict['公司网址']
            # 企业名称:(companyName)			中国科学器材有限公司
            item['companyName'] = ''
            if '公司名称' in data_dict.keys():
                item['companyName'] = data_dict['公司名称']
            # print('************ ', item['companyName'])
            # 企业英文名：(companyEnglishName)			China National Scientific Instruments and Materials Co., Ltd
            item['companyEnglishName'] = ''
            # 注册类型：(registrationType)		供应商
            item['registrationType'] = ''
            # 企业性质：(companyType)			国有绝对控股企业
            item['companyType'] = ''
            # 成立时间:(establishedTime)   		2015-07-22
            item['establishedTime'] = ''
            if '成立时间' in data_dict.keys():
                item['establishedTime'] = data_dict['成立时间']
            # 营业执照号:(businessLicenseNo)			91331102350072370U
            item['businessLicenseNo'] = ''
            # 经营模式：(businessModel)			贸易型
            item['businessModel'] = ''
            # 注册资本：(registeredCapital)			400000.000000 万元
            item['registeredCapital'] = ''
            # 雇员人数：(employee)			301-500 人
            item['employee'] = ''
            # 主营产品：(mainProducts)			理化分析仪器、光学仪器、电子仪器及配件、生物技术及生物工程设备、计算机及附属设备
            item['mainProducts'] = ''
            # 联 系 人：(contact)			雷靖行
            item['contact'] = ''
            if '联系人' in data_dict.keys():
                item['contact'] = data_dict['联系人']
            # 手机号码：(phoneNumber)			18117451540
            item['phoneNumber'] = ''
            if '手机号码' in data_dict.keys():
                item['phoneNumber'] = data_dict['手机号码']
            # 联系电话：(telephone)			0755-00000000
            item['telephone'] = ''
            if '公司电话' in data_dict.keys():
                item['telephone'] = data_dict['公司电话']

            # 公司传真：(companyFax)			0755-00000000
            item['companyFax'] = ''
            if '公司传真' in data_dict.keys():
                item['companyFax'] = data_dict['公司传真']

            # E-MAIL  : (Email)  		18641572818@163.com
            item['Email'] = ''
            if '电子邮件' in data_dict.keys():
                item['Email'] = data_dict['电子邮件']

            # 企业地址：(businessAddress)			北京市朝阳区太阳宫中路19号院1号楼4层
            item['businessAddress'] = ''
            if '公司地址' in data_dict.keys():
                item['businessAddress'] = data_dict['公司地址']

            # Q Q号 码：(qq)   		282278944
            item['qq'] = ''
            if '即时通讯' in data_dict.keys():
                if '.qq.com' in data_dict['即时通讯']:
                    print('------ ', data_dict['即时通讯'])
                    qq = re.findall(r'uin=(.*?)site=', data_dict['即时通讯'], re.DOTALL)
                    if qq != []:
                        item['qq'] = qq[0].replace('&', '').replace('\n', '').replace('\t', '').replace('\r', '').replace(' ','')
            # q = response.xpath('//div[@class="main_body"]//table//tr[8]/td[2]//a/@href').extract()
            # if item['qq'] == '':
            #     print('----', q)
            #     if q != []:
            #         qq = re.findall(r'uin=(.*?)site=', ''.join(q), re.DOTALL)
            #         if qq != []:
            #             item['qq'] = qq[0].replace('&', '').replace('\n', '').replace('\t', '').replace('\r', '').replace(' ','')

            # 微信： (wechat)  		mdjx6673
            item['wechat'] = ''
            # 邮政编码：	(postcode)		210000
            item['postcode'] = ''
            if '邮政编码' in data_dict.keys():
                item['postcode'] = data_dict['邮政编码']

            # 客服旺旺：	(angelBeauty)		**********
            item['angelBeauty'] = ''

            print('item = ', item)

            if item['phoneNumber'] != '':
                yield item
