# -*- coding=utf-8 -*- 
import requests
import time
import base64
from Crypto.Cipher import AES,DES
from Padding import appendPadding,removePadding
import hashlib
import json
from city import citys,citys_pinyin

aes_server_key = "efsdsbafa6xFe8lcg==";
aes_server_iv = "o2muxyVs5cwedbQ==";
aes_client_key = 'weJGsdsdf6FxF9=='
aes_client_iv = 'sewg29nsl='
des_key = "sgfsfKsg8723jF==";
des_iv = "yfw3wexsd=";

#aes加密
def aes_encrypt(text,key,iv):
    #2e1bc1e3ca65a4cb
    sercetykey = str(md5(key)[16:32]).encode('utf-8')
    #c7054589723df4a7
    sercetyiv = str(md5(iv)[:16]).encode('utf-8')
    encryptor=AES.new(sercetykey,AES.MODE_CBC,sercetyiv)
    padded = appendPadding(text.encode('base64'),AES.block_size,mode='CMS')
    ciphertext=encryptor.encrypt(padded)
    return ciphertext.encode('base64')
#aes解密
def aes_devrypt(text,key,iv):
    #d1119693b6a33af8
    sercetykey = str(md5(key)[16:32]).encode('utf-8')
    #7aba45824f51431a
    sercetyiv = str(md5(iv)[:16]).encode('utf-8')
    encryptor=AES.new(sercetykey,AES.MODE_CBC,sercetyiv.decode())
   # padded = appendPadding(text.decode('base64'),AES.block_size,mode='CMS')
    ciphertext=encryptor.decrypt(text.decode('base64'))
    return ciphertext

def des_encrypt(text,key,iv):
    sercetykey = md5(key)[:8].encode('utf-8')
    sercetyiv = md5(iv)[24:32].encode('utf-8')
    encryptor=DES.new(sercetykey,DES.MODE_CBC,sercetyiv)
    padded = appendPadding(text,DES.block_size,mode='CMS')
    ciphertext=encryptor.encrypt(padded)
    return ciphertext

def des_decrypt(text,key,iv):
    #41d96dd9
    sercetykey = str(md5(key)[:8]).encode('utf-8')
    #1bbb415a
    sercetyiv = str(md5(iv)[24:32]).encode('utf-8')
    decryptor=DES.new(sercetykey,DES.MODE_CBC,sercetyiv.decode())
    #padded = appendPadding(text.decode('base64'),DES.block_size,mode='PKCS7')
    ciphertext=decryptor.decrypt(text.decode('base64'))
    return ciphertext

def md5(psw):
    m = hashlib.md5()
    m.update(psw)
    return m.hexdigest()


def decodeData(data):
    data = base64.b64decode(data)
    data = des_decrypt(data,des_key,des_iv)
    data = aes_devrypt(data,aes_server_key,aes_server_iv)
    data = base64.b64decode(data)
    return data 

def getParams(city,month):
    appId = 'b73a4aaa989f54997ef7b9c42b6b4b29'
    clienttype = 'WEB'
    timestamp = str(int(time.time()*1000))#python当前时间有三位小数
    method = 'GETDAYDATA'
    sec = appId+method+timestamp+clienttype+'{"city":"%s","month":"%s"}'%(city,month)
    param = '{"appId":"%s","method":"%s","timestamp":%s,"clienttype":"%s","object":{"city":"%s","month":"%s"},"secret":"%s"}'%(appId,method,timestamp,clienttype,city,month,md5(sec))
    return str(aes_encrypt(param,aes_client_key,aes_client_iv))


def parse(city,month):
    url = 'https://www.aqistudy.cn/historydata/api/historyapi.php' 
    param = getParams(city,month)#构造请求参数
    data = {'hd':param}
    req = requests.post(url,data=data)#post请求
    res = decodeData(req.text)#解析请求结果
    return json.loads(res)

def getData(data):
    for item in data['result']['data']['items']:
        #存储
        print item['time_point'],item['pm2_5'],item['co'],item['o3'],item['quality'],item['rank'],item['so2'],item['aqi'],item['no2']
def crawl(city,year):
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    for month in months:
        getData(parse(city,year+month))
if __name__ == '__main__':
  #  year = ['2013','2014','2015','2016','2017']
    crawl('深圳','2013')
