# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 20:26:50 2023

@author: barbh
"""
from community import community_louvain
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

def FC(g_w, tot_gw, clusters, time_of_diffusion):
    
    #Find sensor nodes
    BCS = FBCS(tot_gw)
    sensor_nodes = pickSensors(BCS, 3)

    #Find the m most likely graphs
    m_gw = [tot_gw[i] for i in random.sample(range(0, 5), 2)]


    #Compute delta_t
    Delta_t = delta_t(time_of_diffusion, sensor_nodes)

    #Compute likelihood for each Gateway Node
    likelihoods = {}

    for node in g_w:
        bfs_tree = nx.bfs_tree(g_w, source = node)
        likelihoods[node] = likelihood(m_gw, bfs_tree, sensor_nodes, Delta_t)


    #Find the node with maximum likelihood
    v1 = max(likelihoods, key = likelihoods.get)

    #Find the candidate cluster
    cc = [node for node, cluster in clusters.items() if cluster == clusters[v1]]
    return cc

# BCS2 = FBCS(cluster_graphs)
# sensor_nodes2 = pickSensors(BCS2, 5)
# Delta_t2 = delta_t(G, sensor_nodes2)
# likelihoods2= [likelihood(node,cluster_graphs,sensor_nodes2,Delta_t) for node in cc]
# v2 = max_likelihood(cc, likelihoods2)
# print(v2)

# for g in tot_gw:
#     print(len(g.edges()))
#     # Model selection - diffusion time
#     model = ep.SIModel(g)

#     # Model Configuration
#     cfg = mc.Configuration()
#     cfg.add_model_parameter('beta', 0.03)
#     cfg.add_model_parameter("fraction_infected", 1/max([max(x[0],x[1]) for x in g.edges()]))
#     model.set_initial_status(cfg)

#     # Simulation execution
#     iterations = model.iteration_bunch(200)

#     #Mapping diffusion_time_to_each_node
#     time_of_diffusion={}
#     for i in range(g.number_of_nodes()):
#         time_of_diffusion[i]=-1
#     for i in iterations:
#         for j in i['status']:
#             if(i['status'][j]==1):
#                 time_of_diffusion[j]=i['iteration']
#     timeOfDiffusions.append(len(time_of_diffusion))
# print(timeOfDiffusions)



