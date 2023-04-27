import content as ct
import numpy as np
import random
import pandas as pd 
import config as cf
import genearal_distribution as gd
import time
from tqdm import tqdm
# TODO : 여기서는 ContentList 를 Scenario로 반환
# TODO : input --> Content List

class Scenario(object):
    def __init__(self, args):
        self.args = args
        self.contentList = self.set_contentList(contentfile = args.contentfile)
        #self.titleList = self.set_titleList()
        self.weightList = self.set_weigthList()

    def set_contentList(self, contentfile):
        contentList = []
        df = pd.read_csv(f'./data/{contentfile}.csv')
        #rows, _ = df.shape
        keys = list(df.keys())
        for row in tqdm(df.to_numpy(), total = len(df), position=0, leave=True):
            ct_keys = keys
            ct_values = row
            if 'size' not in ct_keys:
                ct_keys = np.append(ct_keys, ['size'])
                ct_values = np.append(ct_values, [20])
            content = ct.Content(ct_keys, ct_values)
            contentList.append(content)
            
    
        return contentList
    '''
    def set_titleList(self):
        titleList = []
        for i in range(len(self.contentList)):
            titleList.append(self.contentList[i].id)
            #titleList.append(self.contentList[i].title)
        titleList = set(titleList)
        titleList = list(titleList)
        return titleList
    '''  
    def get_titleList(self):
        return self.titleList

    def set_weigthList(self):
        if self.args.generating_method == 'sequential':
            return None
        elif self.args.generating_method == 'gaussian':
            return None
        else:
            weightList = getattr(gd, self.args.generating_method)(self.contentList)
        return weightList
    
    # 우리가 실험하던거
    def requestGenerate_tmp(self,_day):
        weightList = getattr(gd, self.args.generating_method)(self, _day)
        choice = random.choices(self.contentList, weights = weightList, k = 1)
        return choice[0]

    def requestGenerate(self,_day):
        #! for the zipf
        if self.args.generating_method == 'zipf':
            choice = random.choices(self.contentList, weights = self.weightList, k = 1)
            #print(choice[0].__dict__)
            return choice[0]
        
        #! for the squential 
        elif self.args.generating_method == 'sequential': 
            choice = self.contentList[_day]
            return choice
        
        #! for gaussian
        elif self.args.generating_method == 'gaussian':
            self.weightList = getattr(gd, self.args.generating_method)(self.contentList, _day)
            choice = random.choices(self.contentList, weights = self.weightList, k = 1)
            #print(choice[0].__dict__)
            return choice[0]

    def generateRequest(self, _i):
        # TODO : contentList 에서 원하는 generating_method에 따라 data generating
        #weightList = getattr(gd, self.args.generating_method)(self)
        choice = random.choices(self.contentList, weights = self.weightList, k = 1)
        return choice[0]



