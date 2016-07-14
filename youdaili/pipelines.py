# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging


class Write2FilePipiline(object):
  def __init__(self):
    self.file = open('ipitems.jl', 'wb')

  def process_item(self, item, spider):
    line = json.dumps(dict(item)) + "\n"
    self.file.write(line)
    logging.info("######process_item:successfully")
    return item

  def close_spider(self,spider):
    print("ok you're closing spider")
    self.all_file.close()
