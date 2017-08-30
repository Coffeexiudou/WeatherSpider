#coding=utf-8
import requests
from bs4 import BeautifulSoup
import pymysql
from multiprocessing import Process,Queue
import time
from city import citys_pinyin
from sql import connDB,closeDB

def getPage(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = requests.get(url,headers=headers)
        return req.text 
    except Exception,e:
        print  'page disconnect',e
        return None
def worker1(url):
    page = getPage(url)
    soup = BeautifulSoup(page,'lxml')
    content = soup.find('div',class_='tqtongji1')
    url_list = []
    for item in content.find_all('ul'):
        for i in item.find_all('li'):
            month_url = i.find('a').get('href')
            url_list.append(month_url)
    return url_list
def worker2(url_list,q):
    for item in url_list:
        page = getPage(item)
        soup = BeautifulSoup(page,'lxml')
        content = soup.find('div',class_='tqtongji2')
        for item in content.find_all('ul')[1:]:
            info = []
            for i in item.find_all('li'):
                    info.append(i.string)
            q.put(info)

def worker3(q,cur,conn,city):
    time.sleep(0.5)
    while True:
        if not q.empty():
            value = q.get()
            insert(cur,conn,value,city)
            time.sleep(0.1)
        else:
            print 'empty'
            break

def insert(cur,conn,data,city):
    date = data[0].string
    MaxTemperature = data[1]
    MinTemperature = data[2]
    Weather = data[3]
    WindDirection = data[4]
    AirClassification = data[5]
    cur.execute("insert into T_%s_weather"%city+"(Date,MaxTemperature,MinTemperature,Weather,WindDirection,AirClassification) values(%s,%s,%s,%s,%s,%s)", (date,MaxTemperature,MinTemperature,Weather,WindDirection,AirClassification))
    conn.commit()


if __name__ == '__main__':
    for city in citys_pinyin:
        baseurl = 'http://lishi.tianqi.com/%s/index.html'%(city)
        num = 7
        month_url = worker1(baseurl)
        ave = len(month_url)/7
        q = Queue()
        conn,cur = connDB()
        for i in xrange(num+1):
            a,b = i*ave,(i+1)*ave if (i+1)*ave<len(month_url)else len(month_url)
            spider = Process(target=worker2,args=(month_url[a:b],q))
            spider.start()
        store_p = Process(target=worker3,args=(q,cur,conn,city))
        store_p.start()
        print 'crawl'+city
        store_p.join()
        spider.join()
        print 'crawl'+city+' finish'
        closeDB(cur,conn)
    print 'end '
    
