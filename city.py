#coding=utf-8
from pypinyin import lazy_pinyin,slug


citys = ['北京','上海','天津','重庆','哈尔滨','长春','沈阳','呼和浩特','石家庄','乌鲁木齐','兰州','西宁','西安','银川','郑州','济南','太原','合肥','长沙','武汉','南京','成都','贵阳',
'昆明','南宁','拉萨','杭州','南昌','广州','福州','台北','海口','香港','澳门']

citys_pinyin = [u'beijing', u'shanghai', u'tianjin', u'chongqing', u'haerbin', u'changchun', u'shenyang', u'huhehaote', u'shijiazhuang', u'wulumuqi', u'lanzhou',
 u'xining', u'xian', u'yinchuan', u'zhengzhou', u'jinan', u'taiyuan', u'hefei', u'changsha', u'wuhan', u'nanjing', u'chengdu', u'guiyang', u'kunming', u'nanning', u'lasa', u'hangzhou', u'nanchang', u'guangzhou', u'fuzhou', u'taibei', u'haikou', u'xianggang', u'aomen']

#生成拼音
# for item in citys:
#      citys_pinyin.append(slug(item.decode('utf-8'),heteronym=False, separator=''))

