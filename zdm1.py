# -*- coding: utf-8 -*-
#什么值得买
import requests
from lxml import etree
import pymysql
#连接到本地数据库，打开游标，新建zdm数据表
conn = pymysql.connect(
       host='localhost',
       user='root',
       password='root',
       db='',
       charset='utf8')
cur = conn.cursor()
#cur.execute("DROP TABLE IF EXISTS zdm")   
#create_sqli = "create table zdm(name char(255), price char(255), zhi char(30), buzhi char(30), create_time char(30))"
#cur.execute(create_sqli)
#伪装浏览器，登陆张大妈，下载首页信息
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
url='https://www.smzdm.com/'
response = requests.get(url, headers=headers)
content = response.content.decode()
html = etree.HTML(content) #解析为xpath能认的
#解析信息，将产品名称、价格、值不值、创建时间保存到列表
name = html.xpath("//div[@class='z-feed-content']/h5[@class='feed-block-title has-price']/a/text()")
price = html.xpath("//div[@class='z-feed-content']/div[@class='z-highlight  ']/a/text()")
zhime = html.xpath("//span[@class='unvoted-wrap']/span/text()")
source = html.xpath("//span[@class='feed-block-extras']/text()")
#处理名称和价格
for i in range(len(name)):
    name[i] = name[i].replace('\n            ','')
    price[i] = price[i].replace('\n                    ','')
#处理值数不值数
zhi = []
bzhi = []
for i in range(len(name)):
    zhi.append(zhime[2*i])
    bzhi.append(zhime[2*i+1])
#处理创建时间
for j in range(len(source)):
    source[j] = source[j].replace('\n','')
    source[j] = source[j].replace('  ','')
j = 0
while j <= len(source):
    if source[j] == '':
        del source[j]
        j += 1
    else:
        j += 1
#将处理好的列表数据依次写入数据库
for j in range(len(name)):
    sql='insert into zdm values("{}", "{}", "{}", "{}", "{}");'.format(name[j], price[j], zhi[j], bzhi[j], source[j])
    cur.execute(sql)
    conn.commit()
#关闭游标，关闭数据库
cur.close()
conn.close()