#encoding:utf-8
from pymongo import MongoClient

class Task:
    def __init__(self,my_set):
        self.my_set=my_set

    def insert(self, dic):
        try:
            self.my_set.insert(dic)
            return True
        except Exception,e:
            return False

    def update(self, dic, newdic):
        try:
            self.my_set.update(dic,newdic,upsert=True)
            return True
        except Exception, e:
            return False

    def deleted(self,dic):
        try:
            self.my_set.remove(dic)
            return True
        except Exception,e:
            return False

    def dbFind(self, dic):
        data = self.my_set.find(dic)
        data = list(data)
        return data

    def findAll(self):
        for i in self.my_set.find():
            print(i)

settings = {
    "ip":'172.16.39.170',   #ip
    "port":27017,
    "db_name" : "rule",
    "set_name" : "rule"
}
try:
    conn = MongoClient(settings["ip"], settings["port"])
    db = conn[settings["db_name"]]
    my_set = db[settings["set_name"]]
except Exception as e:
    print(e)

def findif(product):
    dic={'product':product}
    fi=Task(my_set)
    try:
        if fi.dbFind(dic):
            return True
        else:
            return False
    except Exception,e:
        return False

product='99'
print findif(product)