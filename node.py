import config as cf
import numpy as np
import content as ct

class Node(object):

    def __init__(self, _id):
        self.pos_x = np.random.uniform(0, cf.AREA_WIDTH)
        self.pos_y = np.random.uniform(0, cf.AREA_LENGTH)
        self.id=_id

class microBS(object):

    def __init__(self, _id,x,y):
        self.pos_x =x
        self.pos_y =y
        self.id= _id
        self.storage = ct.contentStorage(cf.microBS_SIZE)

class BS(object):

    def __init__(self, _id,x,y):
        self.pos_x =x
        self.pos_y =y
        self.id= _id
        self.storage = ct.contentStorage(cf.BS_SIZE)

class dataCenter(object):

    def __init__(self,x,y):
        self.pos_x =x
        self.pos_y =y
        self.storage = ct.contentStorage(cf.CENTER_SIZE)


def generateNode():
    nodelist=[]
    for i in range(cf.NB_NODES):
        node= Node(i)
        nodelist.append(node)
    return nodelist

def generateMicroBS():
    MicroBSlist=[]
    id = cf.NB_NODES
    for i in range(cf.NUM_microBS[0]):
        for j in range(cf.NUM_microBS[1]):
            #print('Micro_BS_id : {}'.format(id))
            pos_x = (i+1)*cf.AREA_WIDTH/(cf.NUM_microBS[0]+1)
            pos_y = (j+1)*cf.AREA_LENGTH/(cf.NUM_microBS[1]+1)
            MicroBS = microBS(id,pos_x,pos_y)
            MicroBSlist.append(MicroBS)
            id = id + 1
    return MicroBSlist

def generateBS():
    BSlist=[]
    id = cf.NB_NODES + cf.NUM_microBS[0]*cf.NUM_microBS[1]
    for i in range(cf.NUM_BS[0]):
        for j in range(cf.NUM_BS[1]):
            #print('BS_id : {}'.format(id))
            pos_x = (i+1)*cf.AREA_WIDTH/(cf.NUM_BS[0]+1)
            pos_y = (j+1)*cf.AREA_LENGTH/(cf.NUM_BS[1]+1)
            BSlist.append(BS(id,pos_x,pos_y))
            id= id+1
    return BSlist
