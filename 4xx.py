#!/usr/bin/python
#-*- coding: utf-8 -*-

from datetime import datetime,timedelta
import socket,smtplib,string
from socket import *

hostname = gethostname()


hours_1_ago = datetime.now() + timedelta(hours= -1)

result = dict()

for i in range(60):
    min = hours_1_ago + timedelta(minutes = i)
    file = "/home/web_log/haproxy_access/" + min.strftime("%Y%m%d%H") + "/" + hostname +"." + min.strftime("%Y%m%d%H%M")
    
    try:
        open(file)
    except IOError:
        break
    for line in open(file).readlines():
        parts = line.split()
        domain = line.split('{')[1].split('|')[0].split('?')[0]
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
HOST = '220.181.167.47'
PORT = 21568
BUFSIZE =1024
ADDR = (HOST, PORT) 
#
tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
count = 0

#data = "分析日志文件时间点：" + minutes_5_ago.strftime("%Y%m%d%H%M") + "--" + timenow.strftime("%Y%m%d%H%M") + '\n'
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

tcpCliSock.send(data)
tcpCliSock.close()
