import config as cf
import node as nd
import random
import math
import random
import content as ct
import caching as ch
import numpy as np


class Network(list):
    def __init__(self, Scenario, args):
        # implementing Scenario
        self.scenario = Scenario

        # Generating nodes
        self.nodeList = nd.generateNode()
        self.microBSList = nd.generateMicroBS()
        self.BSList = nd.generateBS()
        self.dataCenter = nd.dataCenter(0,0)
        
        self.mbsToBSLink=[]

        self.CoreNodeList = []
        self.DataCenterNodeList = []
        self.BSNodeList = []
        self.MicroBSNodeList = []
        self.days = []

        self.get_c_nodeList()
        self.generate_days()
        self.requested_content:ct.Content
        self.mbsLink()

        # For network caching algorithm comparsion
        self.set_cache_hit_count()
        self.set_total_hop()
        self.set_total_latency()

        # caching algorithm configuration
        self.cache_allocation_algorithm = args.allocation_algorithm
        self.cache_replacement_algorithm = args.replacement_algorithm

        print('cache_allocation_algorithm : ',self.cache_allocation_algorithm)
        print('cache_replacement_algorithm : ',self.cache_replacement_algorithm)

    def set_cache_hit_count(self):
        self.total_cache_hit_count = 0

    def get_cache_hit_count(self):
        return self.total_cache_hit_count

    def update_total_cache_hit_count(self):
        if cf.CORE_ID not in self.path:
            self.total_cache_hit_count += 1

    def set_total_hop(self):
        self.total_hop = 0

    def get_total_hop(self):
        return self.total_hop

    def update_hop(self, hop):
        self.total_hop += hop

    def set_total_latency(self):
        self.total_latency = 0

    def get_total_latency(self):
        return self.total_latency
    
    def update_total_latency(self, latency):
        self.total_latency += latency

    def set_content_diversity(self):
        self.content_diversity = 0

    def get_content_diversity(self):
        return self.content_diversity
    
    def update_content_diversity(self):
        ct_list = []
        for idx in range(cf.NB_NODES, cf.coreidx):
            for ct_idx in range(len(self.getBS(idx).storage.content_storage)):
                ct_list.append(self.getBS(idx).storage.content_storage[ct_idx].id)

        print(ct_list)
        # 네트워크 내에 있는 모든 content의 갯수
        ct_cnt = len(ct_list)
        print(ct_cnt)
        # identical 한 content 의 갯수 세기.
        ct_list = set(ct_list)
        ct_list = list(ct_list)
        print(ct_list)
        identical_ct_cnt = len(ct_list)

        # content_diversity 구하기.
        self.content_diversity = identical_ct_cnt/ct_cnt
        print(self.content_diversity)
    
    def set_content_redundancy(self):
        self.cotent_redundancy = 0

    def get_content_redundancy(self):
        return self.cotent_redundancy

    def update_content_redundancy(self):
        ct_list = []
        for idx in range(cf.NB_NODES, cf.coreidx):
            for ct_idx in range(len(self.getBS(idx).storage.content_storage)):
                ct_list.append(self.getBS(idx).storage.content_storage[ct_idx].id)


        # 네트워크 내에 있는 모든 content의 갯수
        ct_cnt = len(ct_list)

        # identical 한 content 의 갯수 세기.
        ct_list = set(ct_list)
        ct_list = list(ct_list)
 
        identical_ct_cnt = len(ct_list)

        # content_redundancy 구하기.
        self.content_redundancy = 1 - (identical_ct_cnt/ct_cnt)
        print(self.content_redundancy)

    def print_results(self):
        print(f'round : {self.round+1}')
        print('avg_latency : {}'.format(self.get_total_latency()/cf.MAX_ROUNDS))
        print('avg_hop : {}'.format(self.get_total_hop()/cf.MAX_ROUNDS))
        print('Cache Hit Ratio : {}'.format(self.get_cache_hit_count()/cf.MAX_ROUNDS))

    def generate_days(self):
        total_day = 7*cf.TOTAL_PRIOD
        days = random.choices(range(total_day), k=cf.MAX_ROUNDS)
        days.sort()
        self.days = days

    def simulate(self):
        for round_nb in range(cf.MAX_ROUNDS):
            self.round= round_nb
            round_day = self.days[round_nb] % 7
            self.run_round(round_day)
            #self.run_round(round_nb)

    def run_round(self, _day):
        self.requested,self.path = self.request_and_get_path(_day)
        self.update_results()
        self.caching()
    
    def caching(self):
        ch.caching(self)

    def update_results(self):
        self.update_total_cache_hit_count()
        self.update_hop(len(self.path) - 1)
        self.update_total_latency(self.get_latency(self.path))

    def search_parent_node(self,x,y,index):
        #type node:0, microbs:1 bs:2
        if index < cf.microStartidx:
            type = 0
        elif index < cf.bsStartidx:
            type = 1
        if type is 0:
            minRange = cf.AREA_LENGTH
            closestNode:nd.microBS
            closestID:int
            for i in self.microBSList:
                range=  math.sqrt(math.pow((x-i.pos_x),2) + math.pow((y-i.pos_y),2))
                if minRange>range:
                    closestNode=i
                    minRange=range
                    closestID=closestNode.id

        if type is 1:
            minRange = cf.AREA_LENGTH
            closestNode:nd.BS
            closestID:int
            for i in self.BSList:
                range =  math.sqrt(math.pow((x-i.pos_x), 2) + math.pow((y-i.pos_y),2))
                if minRange>range:
                    closestNode=i
                    minRange=range
                    closestID=closestNode.id
                    
        return closestID

    def hierarchical_request_and_get_path(self,_day):
        path=[]
        #시작 
        id = random.choice(range(0,cf.NB_NODES))
        time_delay = 0 
        #요청 content 선택
        requested_content = self.scenario.requestGenerate(_day)
        path.append(id)#노드
        
        micro_hop = self.search_parent_node(self.nodeList[id].pos_x,self.nodeList[id].pos_y,path[-1])
        path.append(micro_hop)#microBS
        if self.search(self.microBSList,micro_hop).storage.isstored(requested_content)==0:
            bs_hop = self.search_parent_node(self.search(self.microBSList,micro_hop).pos_x, self.search(self.microBSList,micro_hop).pos_y, path[-1])
            path.append(bs_hop)#BS
            if self.search(self.BSList, bs_hop).storage.isstored(requested_content)==0:
                path.append(cf.DATACENTER_ID)#center
                if self.dataCenter.storage.isstored(requested_content)==0:
                    path.append(cf.CORE_ID)
        
        return requested_content,path 
        
    def request_and_get_path(self,_day):
        path=[]
        #시작 
        id = random.choice(range(0,cf.NB_NODES))
        time_delay = 0 
        #요청 content 선택
        requested_content = self.scenario.requestGenerate(_day)
        path.append(id)#노드
        #바로 윗micro BS 탐색
        micro_hop = self.search_parent_node(self.nodeList[id].pos_x,self.nodeList[id].pos_y,path[-1])
        path.append(micro_hop)#microBS
        #요청한 컨텐츠 없을경우 parent BS 탐색
        if self.search(self.microBSList,micro_hop).storage.isstored(requested_content)==0:
            bs_hop = self.search_parent_node(self.search(self.microBSList,micro_hop).pos_x,self.search(self.microBSList,micro_hop).pos_y, path[-1])
            path.append(bs_hop)#BS
            #없으면 아래 micro BS 탐색
            next_microPath = 0
            if self.search(self.BSList, bs_hop).storage.isstored(requested_content)==0:
                #print(bs_hop,cf.bsStartidx)
                for i in self.mbsToBSLink[bs_hop-cf.bsStartidx]:
                    if self.search(self.microBSList,i).storage.isstored(requested_content)==1:
                        #print(self.search(self.microBSList,i).storage.storage)
                        next_microPath=i
                if next_microPath is not 0:
                    path.append(next_microPath)
                elif next_microPath is 0:
                    path.append(cf.DATACENTER_ID)#center
                    if self.dataCenter.storage.isstored(requested_content)==0:
                        path.append(cf.CORE_ID)
        #print("최종path:",path)
        #print("requested content",requested_content.__dict__)

        return requested_content,path

    def get_forward_transmission_time(self,index_i,index_j):
        # forward 에서는 ack delay time 을 계산
        # 마지막 부분은 3 hand shake를 구현

        # 아직 수식 구현에 있어서 변수 값 정해줘야함.
        
        i_x, i_y = self.checkBS_and_getPosition(index_i)
        j_x, j_y = self.checkBS_and_getPosition(index_j)

        # DATACENTER 와 CORE 인 경우 둘다 (0,0) 좌표
        # Latency 는 config Latency_Internet
        if (i_x == 0) & (i_y == 0) & (j_x == 0) & (j_y ==0):
            print('datacenter <-> core')
            return cf.LATENCY_INTERNET

        # uplink latency
        if index_i < index_j:
            print('uplink : {'+ str(index_i) + '} -> {' + str(index_j) + '}')
            traffic_intensity = 1-abs(np.random.normal(0, 0.1, 1))
            range = math.sqrt(math.pow(i_x - j_x, 2) + math.pow(i_y - j_y, 2))
            propagation_delay = range/ cf.LIGHT_SPEAD
            transmission_delay = cf.ACK_PACKET_SIZE/cf.ULthroughput
            queuing_delay = traffic_intensity*(1-traffic_intensity)*cf.ACK_PACKET_SIZE/cf.ULthroughput
            
        # downlink latency
        else:
            print('downlink : {'+ str(index_i) + '} -> {' + str(index_j) + '}')
            traffic_intensity = 1-abs(np.random.normal(0, 0.3, 1))
            range = math.sqrt(math.pow(i_x - j_x, 2) + math.pow(i_y - j_y, 2))
            propagation_delay = range/ cf.LIGHT_SPEAD
            transmission_delay = cf.ACK_PACKET_SIZE/cf.DLthroughput
            queuing_delay = traffic_intensity*(1-traffic_intensity)*cf.ACK_PACKET_SIZE/cf.DLthroughput

        return propagation_delay+transmission_delay+queuing_delay
    
    def get_backward_transmission_time(self,index_i,index_j):
        # index 를 보고 Node/MicroBS/BS/DataCenter/Core 인지 확인 후 transmission time 결정
        transmission_time = 0
        
        i_x, i_y = self.checkBS_and_getPosition(index_i)
        j_x, j_y = self.checkBS_and_getPosition(index_j)


        # DATACENTER 와 CORE 인 경우 둘다 (0,0) 좌표
        # Latency 는 config Latency_Internet
        if (i_x == 0) & (i_y == 0) & (j_x == 0) & (j_y ==0):
            print('datacenter <-> core')
            return cf.LATENCY_INTERNET

        # uplink latency
        if index_i < index_j:
            print('uplink : {'+ str(index_i) + '} -> {' + str(index_j) + '}')
            traffic_intensity = 1-abs(np.random.normal(0, 0.1, 1))
            range = math.sqrt(math.pow(i_x - j_x, 2) + math.pow(i_y - j_y, 2))
            propagation_delay = range/ cf.LIGHT_SPEAD
            transmission_delay = cf.PACKET_SIZE/cf.ULthroughput
            queuing_delay = traffic_intensity*(1-traffic_intensity)*cf.PACKET_SIZE/cf.ULthroughput
            
        # downlink latency
        else:
            print('downlink : {'+ str(index_i) + '} -> {' + str(index_j) + '}')
            traffic_intensity = 1-abs(np.random.normal(0, 0.3, 1))
            range = math.sqrt(math.pow(i_x - j_x, 2) + math.pow(i_y - j_y, 2))
            propagation_delay = range/ cf.LIGHT_SPEAD
            transmission_delay = cf.PACKET_SIZE/cf.DLthroughput
            queuing_delay = traffic_intensity*(1-traffic_intensity)*cf.PACKET_SIZE/cf.DLthroughput

        return propagation_delay+transmission_delay+queuing_delay

    def get_transmission_time(self,index_i,index_j):
        # index 를 보고 Node/MicroBS/BS/DataCenter/Core 인지 확인 후 transmission time 결정
        transmission_time = 0
        
        i_x, i_y = self.checkBS_and_getPosition(index_i)
        j_x, j_y = self.checkBS_and_getPosition(index_j)


        # DATACENTER 와 CORE 인 경우 둘다 (0,0) 좌표
        # Latency 는 config Latency_Internet
        if (i_x == 0) & (i_y == 0) & (j_x == 0) & (j_y ==0):
            #print('datacenter <-> core')
            return cf.LATENCY_INTERNET

        # uplink latency
        if index_i < index_j:
            #print('uplink : {'+ str(index_i) + '} -> {' + str(index_j) + '}')
            traffic_intensity = 1-abs(np.random.normal(0, 0.1, 1))
            range = math.sqrt(math.pow(i_x - j_x, 2) + math.pow(i_y - j_y, 2))
            propagation_delay = range/ cf.LIGHT_SPEAD
            transmission_delay = cf.PACKET_SIZE/cf.ULthroughput
            queuing_delay = traffic_intensity*(1-traffic_intensity)*cf.PACKET_SIZE/cf.ULthroughput
            
        # downlink latency
        else:
            #print('downlink : {'+ str(index_i) + '} -> {' + str(index_j) + '}')
            traffic_intensity = 1-abs(np.random.normal(0, 0.3, 1))
            range = math.sqrt(math.pow(i_x - j_x, 2) + math.pow(i_y - j_y, 2))
            propagation_delay = range/ cf.LIGHT_SPEAD
            transmission_delay = cf.PACKET_SIZE/cf.DLthroughput
            queuing_delay = traffic_intensity*(1-traffic_intensity)*cf.PACKET_SIZE/cf.DLthroughput

        #print(propagation_delay+transmission_delay+queuing_delay)

        return propagation_delay+transmission_delay+queuing_delay

    def get_latency(self, path):

        # index NODE 부터 CORE 까지 0부터 시작
        # 따라서 n번째 index 가 n+1번째 index 보다 작으면 uplink latency
        # n번째 index 가 n+1번째 index 보다 크면 downlink latency
        
        latency = 0
        #print('===forward===')
        #print('path : {}'.format(path))
        # forward
        for n in range(len(path)-1):
            latency += self.get_transmission_time(path[n],path[n+1])
        
        # backward
        path.reverse()
        #print('===backward===')
        #print('path : {}'.format(path))
        for n in range(len(path)-1):
            latency += self.get_transmission_time(path[n],path[n+1])

        # 다시 원상복구
        path.reverse()

        #print('total latency : {}'.format(latency))

        return latency


# 내가 만든 함수들 
# 목록 : reset, request, get_simple_path, get_c_nodeList

    def reset(self):
        self.__init__()

    def get_simple_path(self, nodeId):

        path=[]
        #시작 
        id = nodeId
        path.append(id)#노드
        # 노드 x,y 좌표를 통해 [node - micro - BS - Data center - Core Internet]
        micro_hop = self.search_parent_node(self.nodeList[id].pos_x,self.nodeList[id].pos_y,path[-1])
        path.append(micro_hop)#microBS
        bs_hop = self.search_parent_node(self.search(self.microBSList,micro_hop).pos_x, self.search(self.microBSList,micro_hop).pos_y, path[-1])
        path.append(bs_hop)# Base Station
        path.append(cf.dcidx)# Data Center
        path.append(cf.coreidx)# Core Internet
        return path

    def get_c_nodeList(self):

        # TODO : Core Internet --> 모든 노드
        # TODO : Data Center --> 모든 노드
        # 각각 따로 for 문이 돌아갈 필요 X
        for id in range(cf.NB_NODES):
            self.CoreNodeList.append(id)
            self.DataCenterNodeList.append(id)

        # TODO : 먼저 모든 노드들의 path를 구한뒤 배열로 각각 따로 저장하자
        # TODO : Micro Base Station --> Node들을 저장
        # TODO : Base Station --> 연결 되어있는 Micro Base Station 저장

        nodePathList = []
        tmpPath = []
        for id in range(cf.NB_NODES):
            tmpPath = self.get_simple_path(id)
            #print(tmpPath)
            nodePathList.append(tmpPath)
            tmpPath = []
        
        #print(nodePathList)

        # MicroBS_Id 는 cf.NB_NODES ~ cf.NUM_microBS[0]*cf.NUM_microBS[1] - 1 범위에 있다.
        for MicroBS_Id in range(cf.NB_NODES + cf.NUM_microBS[0]*cf.NUM_microBS[1]):

            tmpMicroNodeList = []
            if MicroBS_Id < cf.NB_NODES:
                tmpMicroNodeList.append(-1)

            else:
                for i in range(cf.NB_NODES):
                    # nodePathList = [[0, 64, 7, 0, 0], ... , [300, 5, 2, 0, 0]]
                    # MicroNodePathList 에는 MicroBS 의 id 가 index 
                    # 해당 index 에 node id 들이 append 됌
                    
                    if MicroBS_Id == nodePathList[i][1]:
                        #print("node의 id : " + str(nodePathList[i][0]) + " 추가")
                        tmpMicroNodeList.append(nodePathList[i][0])

                if len(tmpMicroNodeList) == 0:
                    tmpMicroNodeList.append(-1)
            #print("MicroBSID 에 포함되는 NodeList : " + str(tmpMicroNodeList))
            self.MicroBSNodeList.append(tmpMicroNodeList)
        
        #print('self.MicroBSNodeList : {}'.format(self.MicroBSNodeList))
        # BS_Id 는 cf.NUM_microBS[0]*cf.NUM_microBS[1] ~ cf.NUM_BS[0]*cf.NUM_BS[1] - 1 범위에 있다.
        for BS_Id in range(cf.NB_NODES + cf.NUM_microBS[0]*cf.NUM_microBS[1] + cf.NUM_BS[0]*cf.NUM_BS[1]):
            tmpBSNodeList = []
            if BS_Id < (cf.NB_NODES + cf.NUM_microBS[0]*cf.NUM_microBS[1]):
                tmpBSNodeList.append(-1)

            else:
                for i in range(cf.NB_NODES):
                    # BSNodePathList 에는 BS 의 id 가 index 
                    # 해당 index 에 MicroBS id 들이 append 됌
                    if BS_Id == nodePathList[i][2]:

                        if nodePathList[i][1] not in tmpBSNodeList:
                            tmpBSNodeList.append(nodePathList[i][1])

                if len(tmpMicroNodeList) == 0:
                    tmpBSNodeList.append(-1)
            #print(tmpBSNodeList)
            self.BSNodeList.append(tmpBSNodeList)
        #print('self.BSNodeList : {}'.format(self.BSNodeList))

    def search(self, _list:list, _id):
        for index, element in enumerate(_list):
             if element.id == _id:
                return element

    def checkBS(self, _id):
        # NODE
        if _id < cf.NB_NODES:
            return 'NODE'
        # MicroBS
        elif _id < cf.NB_NODES + cf.NUM_microBS[0] * cf.NUM_microBS[1]:
            return 'MicroBS'
        # BS
        elif _id < cf.NB_NODES + cf.NUM_microBS[0] * cf.NUM_microBS[1] + cf.NUM_BS[0]*cf.NUM_BS[1]:
            return 'BS'
        # DataCenter
        elif _id == cf.DATACENTER_ID:
            return 'DataCenter'
        # Core
        else:
            return 'CORE'
    
    def checkBS_and_getPosition(self, _id):
        # NODE
        if _id < cf.NB_NODES:
            #print('NODE')
            element = self.search(self.nodeList, _id)
            return element.pos_x, element.pos_y
        # MicroBS
        elif _id < cf.NB_NODES + cf.NUM_microBS[0] * cf.NUM_microBS[1]:
            #print('MicroBS')
            element = self.search(self.microBSList, _id)
            return element.pos_x, element.pos_y
        # BS
        elif _id < cf.NB_NODES + cf.NUM_microBS[0] * cf.NUM_microBS[1] + cf.NUM_BS[0]*cf.NUM_BS[1]:
            #print('BS')
            element = self.search(self.BSList, _id)
            return element.pos_x, element.pos_y
        # DataCenter
        elif _id == cf.DATACENTER_ID:
            #print('DataCenter')
            return self.dataCenter.pos_x, self.dataCenter.pos_y
        # Core
        else:
            #print('CORE')
            return 0, 0

    def getBS(self, BS_id):
        BS_type = self.checkBS(BS_id)
        if BS_type == 'MicroBS':
            return self.search(self.microBSList, BS_id)
        elif BS_type == 'BS':
            return self.search(self.BSList, BS_id)
        elif BS_type == 'DataCenter':
            return self.dataCenter
        else:
            print('It\'s NODE or CORE.')


    def mbsLink(self):

        temp_BS=[]
        for i in range(cf.NUM_BS[0]*cf.NUM_BS[1]):
            temp_BS.append([])
        for i in range(cf.NUM_microBS[0]*cf.NUM_microBS[1]):
            BS_index = self.search_parent_node(self.microBSList[i].pos_x,self.microBSList[i].pos_y,i+cf.microStartidx)-cf.bsStartidx
            temp_BS[BS_index].append(i+cf.microStartidx)
            
        self.mbsToBSLink=temp_BS
        #print(self.mbsToBSLink)

