# -*- coding: UTF-8 -*-
import codecs
import sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import os
import json
import io
import time

rootdir="/home/ubuntu/S1PlainTextBackup/"

with open(rootdir+'RefreshingData.json',"r",encoding='utf-8') as f:
    thdata=json.load(f)
for i in range(len(thdata)):
    if(((int(time.time()) -thdata[i]['lastedit']) < 2592000 ) and thdata[i]['totalpage'] > 1) :
        thdata[i]['active'] = True
with open(rootdir+'RefreshingData.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(thdata,indent=2,ensure_ascii=False))
