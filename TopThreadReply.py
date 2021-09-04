# -*- coding: UTF-8 -*-

rootdir="./"

import re
import json
from pathlib import Path
import datetime
import requests,os,time

rootpath = './'


def getdate(beforeOfDay):
        today = datetime.datetime.today()
        # 计算偏移量
        offset = datetime.timedelta(days=-beforeOfDay)
        # 获取想要的日期的时间
        re_date = (today + offset).strftime('%Y-%-m-%-d')
        return re_date

if __name__ == '__main__':
    p = Path(rootpath)
    threaddict = {}
    replydict = {}
    for file in p.rglob('*.md'):
        if(('虚拟主播区专楼' not in str(file) ) and ('游戏区专楼' not in str(file))):
            print(str(file))
            with open (file, 'r',encoding='UTF-8') as f:
                lines = f.readlines() 
                a = ''
                for line in lines:
                    a += line.strip()
                    # a += line
                b = a.split("*****")
                res = []
                for post in b:
                    post1 = post
                    post2 = post
                    data={}
                    data['id'] = ''.join(re.findall(r"^[\*]{0,2}####\s\s([^#]+)#", post))
                    # data['level'] = str(filepath)+''.join(re.findall(r"#####\s(\d+)#", post1))
                    data['time'] = ''.join(re.findall(r"^.*?发表于\s(\d{4}-\d{1,2}-\d{1,2}) \d{2}:\d{2}", post2))
                    if(data['id']):
                        res.append(data)
                threadid = re.findall(r"\d{5,9}", str(file))[0]
                temptimedict = {}
                for i in res:
                    if i['time'] in temptimedict.keys():
                        temptimedict[i['time']]['num'] = temptimedict[i['time']]['num'] + 1
                    else:
                        temptimedict[i['time']] = {}
                        temptimedict[i['time']]['num'] = 1
                    if i['id'] in temptimedict[i['time']].keys():
                        temptimedict[i['time']][i['id']] = temptimedict[i['time']][i['id']] + 1
                    else:
                        temptimedict[i['time']][i['id']] = 1
                today = str(getdate(1))
                if today in temptimedict.keys():
                    # if today not in threaddict.keys():
                    #     threaddict[today] = {}
                    # if threadid not in threaddict[today].keys():
                    #     threaddict[today][threadid] = 0
                    # threaddict[today][threadid] = threaddict[today][threadid] + temptimedict[today]['num']
                    if today not in replydict.keys():
                        replydict[today] = {}
                    for k in temptimedict[today].keys():
                        if k not in replydict[today].keys():
                            replydict[today][k] = {}
                            replydict[today][k]['num'] = 0
                        if threadid not in replydict[today][k].keys():
                            replydict[today][k][threadid] = 0
                        replydict[today][k]['num'] = replydict[today][k]['num'] + temptimedict[today][k]
                        replydict[today][k][threadid] = replydict[today][k][threadid] + temptimedict[today][k]
            # for k in list(threaddict.keys()):
            #     if not threaddict[k]:
            #         del threaddict[k]
    rstr = '[b]统计日期：[/b]'
    rstr = rstr + (datetime.datetime.today()+datetime.timedelta(days=-1)).strftime('%Y年%-m月%-d日')+'\n'
    rstr = rstr + '[b]该日统计回帖数：[/b]'+str(replydict[today]['num']['num'])+'\n\n'
    rstr = rstr + '[b]回帖数量前20的帖子：[/b]\n'
    thdict = replydict[today]['num']
    thdict.pop('num')
    threadorder=sorted(thdict.items(),key=lambda x:x[1],reverse=True)
    namedict = {}
    replydict1 = replydict
    replydict1[today].pop('num')
    for i in replydict1[today].keys():
        namedict[i] = replydict1[today][i]['num']
    # namedict.pop('num')
    nameorder = sorted(namedict.items(),key=lambda x:x[1],reverse=True)
    with open(rootdir+'RefreshingData.json',"r",encoding='utf-8') as f:
        thdata=json.load(f)
    for i in range(20):
        rstr = rstr +str(i+1)+'. [url=https://bbs.saraba1st.com/2b/thread-'+threadorder[i][0]+'-1-1.html]'+thdata[threadorder[i][0]]['title'] +'[/url]（[b]+'+str(threadorder[i][1])+'[/b]）\n'
    rstr = rstr + '\n' + '[b]回帖数量前20的用户：[/b]\n'
    for i in range(20):
        nameth = replydict1[today][nameorder[i][0]]
        nameth.pop('num')
        norder = sorted(nameth.items(),key=lambda x:x[1],reverse=True)
        rstr = rstr +str(i+1)+'. '+nameorder[i][0]+'（[b]+'+str(nameorder[i][1]) +'[/b]）：\n'+'[url=https://bbs.saraba1st.com/2b/thread-'+norder[0][0]+'-1-1.html]'+thdata[norder[0][0]]['title'] +'[/url]（[b]+'+str(norder[0][1])+'[/b]）\n'
    rstr = rstr + '\n[color=7c6f64]提示：\n1. 本统计仅包括外野、漫区、游戏区\n[/color]'
    cookie_str1 = os.getenv('S1_COOKIE')
    cookie_str = repr(cookie_str1)[1:-1]
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'}
    ''' 获取formhash'''
    RURL = 'https://bbs.saraba1st.com/2b/forum.php?mod=viewthread&tid=334540&extra=page%3D1'
    s1 = requests.get(RURL, headers=headers,  cookies=cookies)
    content = s1.content
    while True:
        rows = re.findall(r'<input type=\"hidden\" name=\"formhash\" value=\"(.*?)\" />', str(content)) #正则匹配找到formhash值
        if len(rows)!=0:
            formhash = rows[0]
            print('formhash is: ' + formhash)
            subject = u''
            # Aurl = 'https://raw.fastgit.org/TomoeMami/S1PlainTextBackup/master/A-Thread-id.txt'
            # s = requests.get(Aurl)
            # threadid = s.content.decode('utf-8')
            '''回帖ID，手动修改'''
            threadid = 2023780
            '''回帖ID，手动修改'''
            replyurl = 'https://bbs.saraba1st.com/2b/forum.php?mod=post&action=reply&fid=151&tid='+str(threadid)+'&extra=page%3D1&replysubmit=yes'
            #url为要回帖的地址
            Data = {'formhash': formhash,'message': rstr,'subject': subject,'posttime':int(time.time()),'wysiwyg':1,'usesig':1}
            req = requests.post(replyurl,data=Data,headers=headers,cookies=cookies)
            print(req)
            break
        else:
            print('none formhash!')
            continue
