import random
import general_cache_replacement_algorithm as cr
# Leave copy everywhere
def LCE(network):
    path = network.path
    for i in range(1, len(path)):
        BS_id = path[i]
        BS_type = network.checkBS(BS_id)
        if BS_type != 'NODE' and BS_type != 'CORE':
            getattr(cr, network.cache_replacement_algorithm)(network, BS_type, BS_id)

# Leave copy down
def LCD(network):
    path = network.path
    for i in range(2):
        BS_id = path[-(i+1)]
        BS_type = network.checkBS(BS_id)
        if BS_type != 'NODE' and BS_type != 'CORE':
            getattr(cr, network.cache_replacement_algorithm)(network, BS_type, BS_id)

# Random copy
def RND(network):
    path = network.path
    # path의 cache_hit 이 일어난 BS를 제외한 나머지 BS들 중 하나에 랜덤하게 선정 후 cache_hitted_BS 는 cache_replacement_algorithm에 의해 update
    # cache_hitted_BS update
    BS_type = network.checkBS(path[-1])
    BS_id = path[-1]
    getattr(cr, network.cache_replacement_algorithm)(network, BS_type, BS_id)
    # random_BS update
    if len(path) != 2:
        random_BS = random.randrange(1,len(path)-1)
        BS_id = path[random_BS]
        BS_type = network.checkBS(BS_id)
        if BS_type != 'NODE' and BS_type != 'CORE':
            getattr(cr, network.cache_replacement_algorithm)(network, BS_type, BS_id)





       

    

