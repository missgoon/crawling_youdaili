# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from youdaili.items import *
import requests

class AnjukeSpider(CrawlSpider):
  name="youdaili"
  allowed_domains=["youdaili.net"]
  start_urls=[
    "http://www.youdaili.net/Daili/QQ/list_1.html",
    "http://www.youdaili.net/Daili/guonei/list_1.html",
    "http://www.youdaili.net/Daili/http/list_1.html",
    "http://www.youdaili.net/Daili/guowai/list_1.html",
    "http://www.youdaili.net/Daili/Socks/list_1.html"
  ]
  
  def parse(self,response):
    self.logger.info("######parse:%s",response.url)
    sel=Selector(response=response)
    div=sel.xpath("//div[@class='newslist_body']")[0]
    ul=div.xpath("./ul[@class='newslist_line']")[0]
    for li in ul.xpath("./li"):
      url=li.xpath("./a/@href")[0].extract()	
      yield scrapy.Request(url,self.parse_ip)
    url,page_num=response.url.split("list_")
    page_num=int(page_num.split(".html")[0])+1
    url=url+"list_"+str(page_num)+".html"
    if requests.get(url).status_code==200: yield scrapy.Request(url,self.parse)

  def parse_ip(self,response):
    self.logger.info("######parse_ip:%s",response.url)
    sel=Selector(response=response)
    if len(sel.xpath("//span[@style='font-size:14px;']"))>=1:
	    for item in sel.xpath("//span[@style='font-size:14px;']/text()"):
	      # handle_item(item)
	      print(item)
	  elif len(sel.xpath("//div[@class='cont_font']/p/text()"))>0:
	    for item in sel.xpath("//div[@class='cont_font']/p/text()"):
	      # handle_item(item)
	      print(item)
	  





def run(url):
  html=lxml.html.fromstring(requests.get(url).content)
  if len(html.xpath("//span[@style='font-size:14px;']"))>=1:
    for item in html.xpath("//span[@style='font-size:14px;']/text()"):
      handle_item(item)
  elif len(html.xpath("//div[@class='cont_font']/p/text()"))>0:
    for item in html.xpath("//div[@class='cont_font']/p/text()"):
      handle_item(item)
  r.set("process_cnt",int(r.get("process_cnt"))-1)

def handle_item(item):
  try:
    if item.strip().count("@")!=0: item=item.strip().split("@")[0]
    elif item.strip().count("#")!=0: item=item.strip().split("#")[0]
    if not len(item)>0: raise
    proxies = {'http':"http://"+item}
    response=requests.get(test_url,proxies=proxies,timeout=1)
    print(proxies,response)
    if response.status_code!=200: raise
    r.lpush("ip_proxies",item)
    print("%s\t%d"%(item,r.llen("ip_proxies")))
  except Exception,e:
    print(e)

