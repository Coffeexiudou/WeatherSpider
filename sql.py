#coding=utf-8
import pymysql
from city import citys_pinyin
def connDB():
    conn = pymysql.connect(host = 'localhost',port = 3306,user = 'root', passwd = '123456',db = 'WEATHER_INFO',charset="utf8")
    cursor = conn.cursor()
    #print u"数据库连接成功"
    return (conn,cursor)
def closeDB(cursor,conn):
    try:
        cursor.close()
        conn.close()
       # print u"数据库关闭成功"
    except Exception as err:
        print u"数据库关闭异常"
        print err
def creat_weather_table():
    conn,cur = connDB()
    for city in citys_pinyin:
        sql = 'CREATE TABLE T_%s_weather(\
        Date datetime,\
        MaxTemperature int,\
        MinTemperature int,\
        Weather varchar(20),\
        WindDirection varchar(20),\
        AirClassification varchar(20));'%(city)
        cur.execute(sql)
        conn.commit()
    closeDB(cur,conn)

def creat_pm2_5_table():
    conn,cur = connDB()
    for city in citys_pinyin:
        sql = 'CREATE TABLE T_%s_air_quality(\
        Date datetime,\
        AQI int,\
        QualityGrade varchar(20),\
        Rank int,\
        PM25 int,\
        PM10 int,\
        SO2 int,\
        CO int,\
        NO2 int,\
        O3_8h int);'%(city)
        cur.execute(sql)
        conn.commit()
    closeDB(cur,conn)


def drop_table():
    conn,cur = connDB()
    for city in citys_pinyin:
        sql = 'DROP TABLE T_{city}_air_quality;'.format(city=city)
        cur.execute(sql)
        conn.commit()
    closeDB(cur,conn)
if __name__ == '__main__':
    #creat_weather_table()
    creat_pm2_5_table()
    #drop_table()