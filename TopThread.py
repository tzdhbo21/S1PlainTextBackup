# -*- coding: UTF-8 -*-

rootdir="./"

import re
import json
from pathlib import Path
import datetime

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
                    if today not in threaddict.keys():
                        threaddict[today] = {}
                    if threadid not in threaddict[today].keys():
                        threaddict[today][threadid] = 0
                    threaddict[today][threadid] = threaddict[today][threadid] + temptimedict[today]['num']
        # for k in list(threaddict.keys()):
        #     if not threaddict[k]:
        #         del threaddict[k]
    with open ('test.json','w',encoding='utf-8') as f:
        f.write(json.dumps(threaddict,indent=2,ensure_ascii=False))
            
