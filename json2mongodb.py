# -*- coding: utf-8 -*-

import json
from pymongo import MongoClient

def connect_mongodb():
  client = MongoClient("139.129.45.40",27017)
  db=client.youdaili
  return db.ips

def get_data_from_jsonfile():
  db_ips=connect_mongodb()
  cntf,cntt,cntr=0,0,0
  with open("ipitems.jl","rb") as jsonfile:
    for line in jsonfile.readlines():
      try: 
        item=json.loads(line)
        db_item=db_ips.find({"ip":item["ip"],"port":item["port"]})	
        if db_item.count()==0: db_ips.insert_one(dict(item))
        else: cntr+=1
        cntt+=1
      except: 
        cntf+=1
        continue
      print(cntt,cntf,cntr)

get_data_from_jsonfile()