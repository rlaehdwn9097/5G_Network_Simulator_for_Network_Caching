import math
from platform import node

# CONFIGURATION FOR NETWORK SIMULATOR

MAX_EPISODE_NUM = 2000
TOTAL_PRIOD = 24 
MAX_ROUNDS = 5000  
MAX_REQ_PER_ROUND = 1

# info of node
NB_NODES = 300 # number of nodes
TX_RANGE = 30 # meters

# area definition
AREA_WIDTH = 5000.0
AREA_LENGTH = 5000.0

# Basestation configuration
NUM_microBS = [3,3] # 36개
NUM_BS = [2,2] # 9개
DATACENTER_ID = NB_NODES + NUM_microBS[0]*NUM_microBS[1] + NUM_BS[0]*NUM_BS[1]
CORE_ID = DATACENTER_ID + 1

# Basestation idx info
microStartidx = NB_NODES
bsStartidx = microStartidx + NUM_microBS[0]*NUM_microBS[1] 
dcidx = bsStartidx + NUM_BS[0]*NUM_BS[1]
coreidx = dcidx + 1


# storage size
CONTENT_SIZE = 20
microBS_SIZE = 100
BS_SIZE = 100
CENTER_SIZE = 200
#scenario info




#잠깐 정리
# network latency = propagation delay + transmission delay + processing delay 
# propagation delay = distance / speed
# transmission delay = packet size (bits)/throughput
# serialization delay = packet size (bits) / Transmission Rate (bps)
# reference : https://5g-tools.com/5g-nr-throughput-calculator/
mu = 30
BW = 50

# J : number of aggregated component carriers, maximum number (3GPP 38.802): 16
J = 1

# maximum number of MIMO layers, 3GPP 38.802: maximum 8 in DL, maximum 4 in UL
v_layers = 4

# modulation order
Q_m =  6

# scaling factor
f = 1

# R_max : Target code Rate R / 1024
R_max = 0.92578125

# maximum # of PRB
# 3GPP 38.213 Table 5.3.2-1 Transmission bandwidth configuration NRB for FR1
# BW = 50MHz , FR1 = 30kHz --> NRB = 133
N_bwPRB = 133

# average OFDM symbol duration in a subframe
t_us = math.pow(10, -3)/(14*math.pow(2,1))

# overhead for control channels
UL_OH = 0.08
DL_OH = 0.14

# TDD throughput(bps)
ULthroughput = J * v_layers * Q_m * f * R_max * (N_bwPRB*12)/ t_us * (1 - UL_OH) * 0.214
DLthroughput = J * v_layers * Q_m * f * R_max * (N_bwPRB*12)/ t_us * (1 - DL_OH) * 0.771

DLpackets_per_second = 108281.25
ULpackets_per_second = 29687.5

LIGHT_SPEAD = 299792458
PACKET_SIZE = 12800 #(1500byte)

#packet size embb 1500byte
#packet size urllc 32bytes
#pacekt size mMTC 32bytes

LATENCY_INTERNET = 0.0025#0.0422 #ms
