#coding=utf-8
item['siteName'] = '志趣网'
        # 爬取对应官网链接(webLinks) 例： https://club.1688.com/

        item['webLinks'] = 'https://www.bestb2b.com/

'
        # 对应详情页链接(detailLink)：  	https://qiye.gongchang.com/hongyipu/contact/

        # item['detailLink'] = response.meta('d_url')
        data_list = response.xpath('//table[@id="viewAttribute"]//tr')
        print('********* ', len(data_list))
        if data_list != []:
            # 企业名称:(companyName)			中国科学器材有限公司
            item['companyName'] = response.xpath('//table[@id="viewAttribute"]/tr[{}]/td[{}]/text()'.format(2, 4)).extract()[0].replace('\xa0', '').replace('\n', '').replace('\t', '')

            # print('************ ', item['companyName'])
            # 企业英文名：(companyEnglishName)			China National Scientific Instruments and Materials Co., Ltd
            item['companyEnglishName'] = None
            # 注册类型：(registrationType)		供应商
            item['registrationType'] = None
            # 企业性质：(companyType)			国有绝对控股企业
            item['companyType'] = None
            # 成立时间:(establishedTime)   		2015-07-22
            item['establishedTime'] = None
            # 营业执照号:(businessLicenseNo)			91331102350072370U
            item['businessLicenseNo'] = None
            # 经营模式：(businessModel)			贸易型
            item['businessModel'] = None
            # 注册资本：(registeredCapital)			400000.000000 万元
            item['registeredCapital'] = None
            # 雇员人数：(employee)			301-500 人
            item['employee'] = None
            # 联 系 人：(contact)			雷靖行
            item['contact'] = response.xpath('//table[@id="viewAttribute"]/tr[{}]/td[{}]/text()'.format(2, 2)).extract()[0].replace('\xa0', '').replace('\n', '').replace('\t', '')
            # 手机号码：(phoneNumber)			18117451540
            item['phoneNumber'] = response.xpath('//table[@id="viewAttribute"]/tr[{}]/td[{}]/text()'.format(4, 4)).extract()[0].replace('\xa0', '').replace('\n', '').replace('\t', '')
            # 联系电话：(telephone)			0755-00000000
            item['telephone'] = response.xpath('//table[@id="viewAttribute"]/tr[{}]/td[{}]/text()'.format(5, 2)).extract()[0].replace('\xa0', '').replace('\n', '').replace('\t', '')
            # 公司传真：(companyFax)			0755-00000000
            item['companyFax'] = None
            # E-MAIL  : (Email)  		18641572818@163.com
            item['Email'] = None
            # Q Q号 码：(qq)   		282278944
            item['qq'] = response.xpath('//table[@id="viewAttribute"]/tr[{}]/td[{}]/text()'.format(5, 4)).extract()[0].replace('\xa0', '').replace('\n', '').replace('\t', '')
            # 微信： (wechat)  		mdjx6673
            item['wechat'] = response.xpath('//table[@id="viewAttribute"]/tr[{}]/td[{}]/text()'.format(4, 2)).extract()[0].replace('\xa0', '').replace('\n', '').replace('\t', '')
            # 邮政编码：	(postcode)		210000
            item['postcode'] = None
            # 客服旺旺：	(angelBeauty)		**********
            item['angelBeauty'] = None
            # 主营产品：(mainProducts)			理化分析仪器、光学仪器、电子仪器及配件、生物技术及生物工程设备、计算机及附属设备
            item['mainProducts'] = None
            # 企业地址：(businessAddress)			北京市朝阳区太阳宫中路19号院1号楼4层
            item['businessAddress'] = response.xpath('//table[@id="viewAttribute"]/tr[{}]/td[{}]/text()'.format(3, 2)).extract()[0].replace('\xa0', '').replace('\n', '').replace('\t', '')
            # 企业网址：(Website)			www.csimc.com.cn
            item['Website'] = 'https://www.bestb2b.com

' + response.xpath('//table[@id="viewAttribute"]/tr[{}]/td[{}]/text()'.format(3, 2)).extract()[0].replace('\xa0', '').replace('\n', '').replace('\t', '')
        print('item = ', item)
