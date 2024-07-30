# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:00:05 2023

@author: barbh
"""

import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import matplotlib.pyplot as plt
import numpy as np

# Network topology

def diffusion_bfs(G, v):
    
    # Model selection
    bfs_tree = nx.bfs_tree(G, source = v)
    model = ep.SIModel(bfs_tree)

    # Model Configuration
    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', 0.03)
    cfg.add_model_parameter("fraction_infected", 0.7)
    model.set_initial_status(cfg)

    # Simulation execution
    iterations = model.iteration_bunch(200)

    #Mapping diffusion_time_to_each_node
    time_of_diffusion={}
    for i in range(1, G.number_of_nodes() + 1):
        time_of_diffusion[i]=-1
    for i in iterations:
        for j in i['status']:
            if(i['status'][j]==1):
                time_of_diffusion[j]=i['iteration']
    for node in G.nodes():
        if node not in time_of_diffusion.keys():
            time_of_diffusion[node] = -1
    return time_of_diffusion

def diffusion(G):
    model = ep.SIModel(G)

    # Model Configuration
    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', 0.03)
    cfg.add_model_parameter("fraction_infected", 0.07)
    model.set_initial_status(cfg)

    # Simulation execution
    iterations = model.iteration_bunch(200)

    #Mapping diffusion_time_to_each_node
    time_of_diffusion={}
    for i in range(1, G.number_of_nodes() + 1):
        time_of_diffusion[i]=-1
    for i in iterations:
        for j in i['status']:
            if(i['status'][j]==1):
                time_of_diffusion[j]=i['iteration']
    return time_of_diffusion
    
def diffusion_cluster(cg, G):
    model = ep.SIModel(cg)
    
    # Model Configuration
    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', 0.03)
    cfg.add_model_parameter("fraction_infected", 1/max([max(x[0],x[1]) for x in cg.edges()]))
    model.set_initial_status(cfg)
    
    # Simulation execution
    iterations = model.iteration_bunch(200)
    
    #Mapping diffusion_time_to_each_node
    time_of_diffusion_cg={}
    for i in range(1, G.number_of_nodes() + 1):
        time_of_diffusion_cg[i]=-1
    for i in iterations:
        for j in i['status']:
            if(i['status'][j]==1):
                time_of_diffusion_cg[j]=i['iteration']
    for node in cg.nodes():
            if node not in time_of_diffusion_cg.keys(): 
                time_of_diffusion_cg[node]=-1
    
    return time_of_diffusion_cg

def delta_t(time_of_diffusion, sensor_nodes):
    delta_t = []
    min_v = min([time_of_diffusion[i] for i in sensor_nodes])
    min_n = -1
    for i in sensor_nodes:
        if time_of_diffusion[i] == min_v:
            min_n = i
            break
    delta_t = [abs(time_of_diffusion[i] - min_v) for i in sensor_nodes if (i != min_n)]
    return delta_t







# inf = []

# for i in iterations:
#     nodes_status = i['status']
#     inf.extend([node for (node, status) in nodes_status.items() if status == 1])
    
# print("total nodes", len(g))
# print("infected nodes", len(inf))
# h = g.subgraph(inf)
# nx.draw(h)
# plt.show()

# edgesOfInfectedGraph = list(h.edges())
# f = open('DiffusionModel/InfectedGraph.txt', 'w')
# f.write(str(inf[0]) + '\n')
# for t in edgesOfInfectedGraph:
#     line = ' '.join(str(x) for x in t)
#  	#print(line)
#  	f.write(line + '\n')
#  	f.close()