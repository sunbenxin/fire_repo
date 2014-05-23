#!/usr/bin/python
#-*- coding: utf-8 -*-

from datetime import datetime,timedelta
import socket,smtplib,string,gzip,os,os.path
from socket import *

hostname = gethostname()

time_now = datetime.now()
hours_1_ago = time_now + timedelta(hours= -1)

result = dict()

for i in range(1):
    min = hours_1_ago + timedelta(minutes = i)
    file = "/home/web_log/haproxy_access/" + min.strftime("%Y%m%d%H") + "/" + hostname +"." + min.strftime("%Y%m%d%H%M") + ".gz"
    try:
        g = gzip.GzipFile(fileobj=open(file))
    except IOError:
        break
    for line in g.readlines():
        parts = line.split()
        try:
            domain = line.split('{')[1].split('|')[0].split('?')[0].split(':')[0]
        except IndexError:
            continue        
        url = parts[-2].split('?')[0]
	if url.startswith('"'):
	    url = '/'
        respond_code = int(parts[10])
        domain_url = domain + url
        if domain == "":
            continue 
        if 500 > respond_code >= 400:
            if result.has_key(domain_url):
                result[domain_url] += 1
            else:
                result[domain_url] = 1
result_sort = list()
for i in sorted(result.iteritems(), key = lambda asd:asd[1], reverse = True):
    result_sort.append(i)

###
count = 0
data = ""
max = len(result_sort)
if max > 20:
    max = 20
while (count < max):
    if not result_sort[count]:
        pass
    elif result_sort[count][1] > 10:
        data += str(result_sort[count][0]).ljust(100) +  str(result_sort[count][1]) + '\n'
    count += 1
if  data == "":
    exit()
else:
    datas = "分析日志文件时间点：" + hours_1_ago.strftime("%Y%m%d%H%M") + "--" + (time_now + timedelta(minutes = -1)).strftime("%Y%m%d%H%M") + '\n' + data

HOST = "mail.funshion.com"
PORT = 25
USER = "jkfunshion"
PASSWD = "jkmail%"
FROM = "jkfunshion@funshion.com"
#TO = ["wsq@funshion.com","OP-GroupSystem@funshion.com"]
TO = "OP-GroupSystem@funshion.com"
#TO = "sunbx@funshion.com"
SUBJECT = "核心域名一小时4xx统计"
if datas != "":
    BODY = string.join(("From: %s" % FROM, "To: %s" % TO,"SUBJECT: %s" % SUBJECT,"",datas),"\r\n")
else:
    exit()
smtp = smtplib.SMTP()
smtp.connect(HOST,PORT)
smtp.login(USER,PASSWD)
smtp.sendmail(FROM,TO,BODY)
smtp.quit()
