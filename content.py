import pandas as pd
import config as cf

class Content(object):
    def __init__(self, keys, values):
        for i in range(len(keys)):
            setattr(self,keys[i], values[i])

    def get_title(self):
        return getattr(self, 'title')


class contentStorage(object):
    def __init__(self, _size):
        self.capacity = _size
        self.stored = 0
        self.content_storage=[]
        # Using only for Least Frequently Used 
        self.content_req_cnt_list=[]
        
    def abletostore(self,c:Content):
        freeSpace = self.capacity-self.stored
        if(freeSpace>=c.size):
            return 1
        else:
            return 0

    def isfull(self):
        freeSpace = self.capacity-self.stored
        if(freeSpace <= 0):
            return 1
        else:
            return 0

    def addContent(self,c:Content):
        self.content_storage.append(c)
        self.content_req_cnt_list.append(1)
        self.stored = self.stored + c.size

    def updateReqCnt(self):
        self.content_req_cnt_list.append(1)
    
    def isstored(self,c:Content):
        if len(self.content_storage)>0:
            for i in self.content_storage:
                if i.id == c.id:
                    return 1
        return 0

    def getindex(self,c:Content):
        if len(self.content_storage)>0:
            for idx, ele in enumerate(self.content_storage):
                if ele.id == c.id:
                    return idx
        return 0

    def delContent(self,c:Content):
        newstorage=[]
        newContent_req_cnt_list=[]
        for i in range(len(self.content_storage)):
            if self.content_storage[i].id is c.id:
                self.stored = self.stored-c.size
            else:
                newstorage.append(self.content_storage[i])
                newContent_req_cnt_list.append(self.content_req_cnt_list[i])
        self.content_storage=newstorage
        self.content_req_cnt_list=newContent_req_cnt_list

    def delFirstStored(self):
        self.stored = self.stored - self.content_storage[0].size 
        self.content_storage=self.content_storage[1:]
        self.content_req_cnt_list=self.content_req_cnt_list[1:]

    def showStorage(self):
        for i in range(len(self.content_storage)):
            print(self.content_storage[i].__dict__, self.content_req_cnt_list[i])

