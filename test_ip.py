# -*- coding: utf-8 -*-
"""
  通过给定的网址 测试代理ip是否可以访问
  有时间了 改成多进程的
  sys.argv[0] 是否从file导入数据  True:是 False:否   如果是则从ip.json  否则从mongodb
  sys.argv[1] 测试的网址 比如：https://www.baidu.com
  sys.argv[2] 等待时间  按秒计
"""
import json
import sys
from pymongo import MongoClient
import requests

def connect_mongodb():
  client = MongoClient("139.129.45.40",27017)
  db=client.youdaili
  return db.ips

def test_ip(item):
  try:
    proxy_str="http://"+str(item["ip"])+":"+str(item["port"])
    print("%s %s %s",proxy_str,str(sys.argv[3]),sys.argv[2])
    r=requests.get(sys.argv[2], proxies={"http":proxy_str},timeout=int(sys.argv[3]))
    return (r.status_code==200 and [True] or [False])[0]
  except: return False

def get_ips_from_file():
  strt,strf="",""
  with open("ips.json","rb") as jsonfile:
    for line in jsonfile.readlines():
      try: item=json.loads(line)
      except: continue
      line=json.dumps(item)+"\n"
      if test_ip(dict(item)): strt+=line
      else: strf+=line
      # (test_ip(dict(item)) and [strt=strt+line] or [strf=strf+line])[0]
  return [strt,strf]

def get_ips_from_db():
  strt,strf="",""
  db_ips=connect_mongodb()
  for item in db_ips.find({},{"_id":False}):
    if test_ip(dict(item)): strt+=line
    else: strf+=line
    # (test_ip(dict(item)) and [strt=strt+line] or [strf=strf+line])[0]
  return [strt,strf]

if __name__ == '__main__':
  strt,strf=(sys.argv[1] and [get_ips_from_file()] or [get_ips_from_db()])[0]
  with open("ip_success.json","wb") as file: 
    file.write(strt)
  with open("ip_failed.json","wb") as file:
    file.write(strf)
