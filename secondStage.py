# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 16:50:33 2023

@author: barbh
"""

import networkx as nx
import numpy as np
import pandas as pd
from findingGateway import *
from createInstance import createInstance
import random
from FBCS import *
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
from SI import *
from FC import *

def FS(G, cg, tot_cg):
    #Find sensor nodes
    BCS = FBCS(tot_cg)
    sensor_nodes = pickSensors(BCS, 3)
    
    #Find the m most likely graphs
    m_cg = [tot_cg[i] for i in random.sample(range(0, 5), 2)]
    
    #Compute delta_t
    
    time_of_diffusion = diffusion_cluster(cg, G)
    
    Delta_t = delta_t(time_of_diffusion, sensor_nodes)
    
    #Compute likelihood for each Gateway Node
    likelihoods = {}

    for node in cg:
        bfs_tree = nx.bfs_tree(cg, source = node)
        likelihoods[node] = likelihood_cg(m_cg, G, bfs_tree, sensor_nodes, Delta_t)


    #Find the node with maximum likelihood
    v2 = max(likelihoods, key = likelihoods.get)
    return v2

