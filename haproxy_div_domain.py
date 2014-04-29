##############################################################
# Auther: DDR
# Function: calulate tq tw tc tr tt 's avg,p95 of each domain 
# Use: ptyone haproxy_div_domain.sh  $haproxylogfilename
##############################################################
#!/usr/bin/python
#from time import localtime,time,strftime
#import re,os,sys
import sys,re
filenum=1
res={}
reqlist={}
while filenum < len(sys.argv):
    file=sys.argv[filenum]
    filenum+=1
    f1=open(file,'r')
    line=f1.readline()
    while line:
        parts=line.split()
        repstime=parts[9].split('/')
        httpcode=parts[10]
        domainpart=parts[17].split('|')
        domaintmp1=domainpart[0].split('{')
        domaintmp2=domaintmp1[1].split(':')
        domain=domaintmp2[0]
        if (not re.search("funshion",domain)) and (not re.search("btstream",domain)) and (not re.search("th123",domain)) and (not re.search("ibidian",domain)):
            domain="other"
        if  (not res.has_key(domain)) and httpcode < '400':
            res[domain]={}
            res[domain]['rowsum']=0
            res[domain]['ttsum']=0
            res[domain]['tqsum']=0
            res[domain]['twsum']=0
            res[domain]['tcsum']=0
            res[domain]['trsum']=0
            reqlist[domain]={}
            reqlist[domain]['tq']=[]
            reqlist[domain]['tw']=[]
            reqlist[domain]['tc']=[]
            reqlist[domain]['tr']=[]
            reqlist[domain]['tt']=[]
            #print res[domain]
        if httpcode < '400':
                res[domain]['tqsum']+=int(repstime[0])
                res[domain]['twsum']+=int(repstime[1])
                res[domain]['tcsum']+=int(repstime[2])
                res[domain]['trsum']+=int(repstime[3])
                res[domain]['ttsum']+=int(repstime[4])
                res[domain]['rowsum']+=1
                reqlist[domain]['tq'].append(int(repstime[0]))
                reqlist[domain]['tw'].append(int(repstime[1]))
                reqlist[domain]['tc'].append(int(repstime[2]))
                reqlist[domain]['tr'].append(int(repstime[3]))
                reqlist[domain]['tt'].append(int(repstime[4]))
        line=f1.readline()
    f1.close()

print "                        domain       count    tq_avg    tq_p95    tw_avg    tw_p95    tc_avg    tc_p95    tr_avg    tr_p95    tt_avg    tt_p95"
for odomain in res:
    #sort all list to get p95
    for resptimetype in reqlist[odomain]:
        reqlist[odomain][resptimetype].sort(None,None,True)
    if res[odomain]['rowsum']==0: res[odomain]['rowsum']=1
    posofp95=res[odomain]['rowsum']/20
    print "%30s %9s %9d %9d %9d %9d %9d %9d %9d %9d %9d %9d" %(odomain,res[odomain]['rowsum'],res[odomain]['tqsum']/res[odomain]['rowsum'],reqlist[odomain]['tq'][posofp95],res[odomain]['twsum']/res[odomain]['rowsum'],reqlist[odomain]['tw'][posofp95],res[odomain]['tcsum']/res[odomain]['rowsum'],reqlist[odomain]['tc'][posofp95],res[odomain]['trsum']/res[odomain]['rowsum'],reqlist[odomain]['tr'][posofp95],res[odomain]['ttsum']/res[odomain]['rowsum'],reqlist[odomain]['tt'][posofp95])
