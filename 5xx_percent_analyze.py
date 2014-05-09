#!/usr/bin/python
#-*- coding: utf-8 -*-
#

#ha 日志5xx五分钟统计 错误原因分析脚本
from datetime import datetime,timedelta
import socket,smtplib,string,sys
from socket import *

dst_domain_url = sys.argv[1] #str
time_ago = sys.argv[2] #ie. 201405091150


hostname = gethostname()
minutes_5_ago = datetime.strptime(time_ago,"%Y%m%d%H%M")

result = dict()

for i in range(5):
    min = minutes_5_ago + timedelta(minutes = i)
    file = "/home/web_log/haproxy_access/" + min.strftime("%Y%m%d%H") + "/" + hostname +"." + min.strftime("%Y%m%d%H%M")
    
    try:
        open(file)
    except IOError:
        break
    for line in open(file).readlines():
        parts = line.split()
        domain = line.split('{')[1].split('|')[0].split('?')[0].split(':')[0]
        url = parts[-2].split('?')[0]
	if url.startswith('"'):
	    url = '/'
        respond_code = int(parts[10])
        domain_url = domain + url
        if domain_url == dst_domain_url and respond_code >= 500:
            if result.has_key(str(respond_code)):
                result[str(respond_code)] += 1
            else:
                result[str(respond_code)] = 1
print result
