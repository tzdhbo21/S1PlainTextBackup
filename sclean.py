# -*- coding: UTF-8 -*-
import codecs
import sys
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import os
import json
import io
import time

rootdir="/home/riko/S1PlainTextBackup/"
activethdata=[]
with open(rootdir+'RefreshingData.json',"r",encoding='utf-8') as f:
    thdata=json.load(f)
for i in range(len(thdata)):
    if(thdata[i]['active']):
        activethdata.append(thdata[i])
with open(rootdir+'RefreshingData.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(activethdata,indent=2,ensure_ascii=False))
