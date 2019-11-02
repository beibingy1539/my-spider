# coding=utf-8
import re
a = 'tencent://message/?uin=1067896922&Site=山东森动轴承有限公司&Menu=yes'
print(re.findall(r'uin=(.*?)&Site', a.replace('\xa0', '').replace('\n', '').replace('\t', '').replace('\r', ''), re.DOTALL)[0])


