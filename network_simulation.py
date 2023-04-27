
from network import Network
from scenario import Scenario
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--contentfile', type=str, default='ht_test')
parser.add_argument('--generating_method', type=str, default='gaussian')
parser.add_argument('--allocation_algorithm', type=str, default='LCE')
parser.add_argument('--replacement_algorithm', type=str, default='LFU')
args = parser.parse_args()

# TODO : Main 에서 설정해줘야할 것들.
# TODO 1. network scenario 설정
# TODO 2. network caching algorithm 설정.

import numpy as np
from matplotlib import pyplot as plt

if __name__=="__main__":

    scenario = Scenario(args)
    network = Network(scenario,args)
    network.simulate()
    network.print_results()
    
