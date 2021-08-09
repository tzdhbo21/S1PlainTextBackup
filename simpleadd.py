# -*- coding: UTF-8 -*-
import codecs
import sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import os
import json
import io
import time
import requests
from bs4 import BeautifulSoup
import re
import math

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
# # # 浏览器登录后得到的cookie，也就是刚才复制的字符串
# cookie_str1 = r'_uab_collina=158915957090898555395583; __gads=ID=1b2e63b0116e499e:T=1589159571:S=ALNI_MbI4dT9moXx9c6JMgrLoNH-9yg_bA; _ga=GA1.2.962496872.1589159572; UM_distinctid=1764668d83e20f-06f0ba162f2728-5a301d45-e1000-1764668d83f1bd; __yjs_duid=1_c69e8ea7f941c1782fbd97570ca6fc741619333738518; CNZZDATA1260281688=697765024-1607495563-%7C1619765638; __cfduid=dbefde9764a01b6227381a595666e8d001620608470; B7Y9_2132_atlist=500945%2C142365; B7Y9_2132_saltkey=A7Y4qvAy; B7Y9_2132_lastvisit=1621323649; B7Y9_2132_auth=67165c2tAZdPjNDfRDoighmXgdtgE1vhu5Jp4uIijLhDhaKv%2BrdE6pnyhcWGsybUJrNClvWne9Xtq0U6gi8rU1NK7dE; B7Y9_2132_lastcheckfeed=523536%7C1621327259; B7Y9_2132_popadv=a%3A0%3A%7B%7D; B7Y9_2132_smile=1465D2; B7Y9_2132_yfe_in=1; B7Y9_2132_pc_size_c=0; B7Y9_2132_st_t=523536%7C1623045946%7C1952a6dc727ff722fe6148c696b32774; B7Y9_2132_forum_lastvisit=D_148_1616482414D_27_1616482416D_87_1617269275D_77_1618191010D_50_1621578960D_135_1622422016D_6_1623026582D_4_1623026647D_75_1623045915D_51_1623045930D_151_1623045946; B7Y9_2132_sid=UZLWBz; B7Y9_2132_lip=183.64.171.98%2C1623049646; B7Y9_2132_ulastactivity=54bfh2C9pvtAziRGDTSH6oAw4HpSqK1ExTQlHZYRFT315JJqExVi; B7Y9_2132_noticeTitle=1; B7Y9_2132_st_p=523536%7C1623054651%7Cc32ad04a12cab6165bcedf092ddee51c; B7Y9_2132_visitedfid=151D75D51D4D6D135D74D50D48D27; B7Y9_2132_viewid=tid_2007615; B7Y9_2132_lastact=1623054651%09index.php%09viewthread'
# cookie_str = repr(cookie_str1)[1:-1]
# # #把cookie字符串处理成字典，以便接下来使用
# cookies = {}
# for line in cookie_str.split(';'):
#     key, value = line.split('=', 1)
#     cookies[key] = value
# # 设置请求头
# headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
# forumlist = {'外野': 75,'虚拟主播':151,'游戏':4,'动漫':6,}
# for i in range(1,50):
#     RURL = 'https://bbs.saraba1st.com/2b/forum-75-.html'+i+'.html'
#     s1 = requests.get(RURL, headers=headers,  cookies=cookies)
#     # s1 = requests.get(RURL, headers=headers)
#     # s1.encoding='utf-8'
#     data = s1.content
#     namelist, replylist,totalpage,newtitles= parse_html(data)

rootdir="/home/riko/S1PlainTextBackup/"
with open(rootdir+'RefreshingData.json',"r",encoding='utf-8') as f:
    thdata=json.load(f)
flag = 1
ids = []
for i in range(len(thdata)):
    ids.append(thdata[i]['id'])
while(flag):
    threadid = input(u"S1 thread ID: ")
    if(threadid == '0'):
        break
    if(threadid in ids):
        print(u"早就有了！更新时间")
        thdata[ids.index(threadid)]['active'] = True
    else:
        print(u'请输入版面分类代号：\n1 = 外野，11 = 外野专楼\n2 = 漫区，22 = 漫区专楼\n3 = 游戏区，33 = 游戏区专楼\n4 = 虚拟主播区专楼，44 = 虚拟主播区专楼')
        threadcategory  = input(u'我选：')
        catechooser = {'1':'外野','11':'外野专楼','2':'漫区','22':'漫区专楼','3':'游戏区','33':'游戏区专楼','4':'虚拟主播区专楼','44':'虚拟主播区专楼'}
        newthread = {"id": threadid,"totalreply": 0,"title": "待更新","lastedit": int(time.time()),"category": catechooser[threadcategory],"active": True}
        thdata.append(newthread)
    with open(rootdir+'RefreshingData.json',"w",encoding='utf-8') as f:
            f.write(json.dumps(thdata,indent=2,ensure_ascii=False))
