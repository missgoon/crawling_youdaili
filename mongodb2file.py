# -*- coding: utf-8 -*-

import json
from pymongo import MongoClient

def connect_mongodb():
  client = MongoClient("139.129.45.40",27017)
  db=client.youdaili
  return db.ips

def get_data_from_jsonfile():
  db_ips=connect_mongodb()
  with open("ips.json","wb") as json_file:
    for item in db_ips.find({},{"_id":False}):
      line=json.dumps(dict(item))+"\n"
      json_file.write(line)
  
get_data_from_jsonfile()