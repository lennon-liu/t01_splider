#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-04-16 15:44:13
# Project: exact_keyword

from pyspider.libs.base_handler import *
import json
import copy
class Handler(BaseHandler):
    base_url="https://172.16.39.94/fofa/"
    crawl_config = {
        'headers': {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4843.400 QQBrowser/9.7.13021.400',
            "Host":"172.16.39.94",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "DNT": "1",
            "Connection": "keep-alive"
        },
        'cookies':{ "_fofa_EE_session":"Qyt5UFZIY0VxRGVKRmxOZ1IvcE05QmlKUDlSV2F3blJBTFJ6Y2R4WWJZU25DQnJmNVpiUFUyMmtVUlBJSHdyUnFkZUxYc3RmUzBZUm5vQ0I0blJ1enVJUkZWak9CM2pmQW0vV1drd2FISjRRL3ZiVUtvQ25wK3d6bUhQd0ZhUlpOTGsyaVd3TzljUXlYa0loMzBCUVZ0dGZmemZUSEdqWFpUQk5LVHZ2ZndSekJ6TVBsbEFkR1UyTEg5MFFvay9uWjh0Uk1IREhLVytWNzRTbkYyTEZMeFl6SGZ5QXlZNkI2eGRUWE5JNWNqc0p1MjRXMFFwM1VPL3F5Q0tSY2tlWDVLM3FBbHBOUHFONjJIMExqTFJFK2hMTFQwQVJHU0tKQXkxRjhnMWNsbzZZbFkrTnlLS2hGWkwzV3pONFRGNkREZmRGdGFkdUlPbzZvTkhESnNUOEtWV29BTEFPSitqd011VURRSlExT3ZvOG4zWnlDQWNBVWF3bmpVcTNjVkUrcG8xNUwxd0pUaEJUYi9RM0M5ZnVtcTJocGhOekFIMlpXYndrcno5M2dTRnpFZ0Nzc1RSVmVoL2t5cTNWZ2lWUGJjL2JNd3loL1BVQVUrb0lBQ0o3c0hYM3JpallPRkZHWklQVnFoWjNaSk5VM2tHdS9kOEhXY0FRWGpsWnBkNnQtLXJqM2drb1ZqOU4xTGIyNTQvQldUNWc9PQ%3D%3D--c533f8f99b2d2b7d71d46e761fa617e977edb61e",
        "path":"/; HttpOnly"}
     }


    @every(minutes=24 * 60)
    def on_start(self):
        keyword='打印机'
        self.crawl(self.base_url+'rules?keyword=%s'%(keyword), callback=self.index_page,validate_cert=False,save={'c':keyword,'url':self.base_url+'rules?keyword=%s'%(keyword)})  
    
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        sumpage=1
        save=copy.deepcopy(response.save)
        print json.dumps(response.save,ensure_ascii=False)
        for each in  response.doc('#asset-container > div.asset-table > div > div > div.pagination.clearfix.fl> a').items():
            if each.text() == ">":
                break
            sumpage=int(each.text())
        for i in range(1,sumpage+1):
            print response.save["url"]+'&page=%d'%(i)
            self.crawl( response.save["url"]+'&page=%d'%(i), callback=self.detail_page,validate_cert=False,save=response.save)
            
    @config(priority=2)
    def detail_page(self, response):
        for each in  response.doc('#asset-container > div.asset-table > table > tbody > tr').items():
            print each("td:nth-child(1)").text()+'\t',each("td:nth-child(2)").text()+'\t',each("td:nth-child(3)").text()+'\t',each("td:nth-child(4)").text()
            save=copy.deepcopy(response.save)
            save["third"]=each("td:nth-child(2)").text()
            save["app"]=each("td:nth-child(3)").text()
            self.crawl(self.base_url+'rules?keyword=%s'%(each("td:nth-child(3)").text()), callback=self.query_page,validate_cert=False,save=save)
            
            
    @config(priority=2)
    def query_page(self, response):
        print "-->",response.save
        info={
        "components":[
            {
                    "category":"",
                    "subcategory":"",
                    "device_type":"",
					"classify":"",
                    "product": "",
                    "version": "",
                    "description": "",
                    "manufacturer": ""
            }
        ],
		"fingerprint":{}
        }
        manufactory=[]
        for each in  response.doc('#asset-container > div:nth-child(5) > div.item-content >a').items():
            if each.text() == u'全部'  or each.text() == u'其他':
                continue
            manufactory.append(each.text())
        
        info["components"][0]["category"] = u'软件'
        info["components"][0]["product"] = response.save['app']
        if len(manufactory)==0:
            info["components"][0]["manufacturer"]=""
        elif len(manufactory)==1:
            info["components"][0]["manufacturer"]=manufactory[0]
        else:
            info["components"][0]["manufacturer"] = manufactory
        print json.dumps(info,ensure_ascii=False, indent=4)
