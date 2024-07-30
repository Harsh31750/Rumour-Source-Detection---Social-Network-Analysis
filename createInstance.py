# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 14:30:17 2023

@author: barbh
"""

import random
import os
import csv
import networkx as nx
from cluster import gatewayNodes
import numpy as np

def createInstance(G, g_w):
    tot_g=[]
    tot_graphs=[]
    for i in range(0, 5):
        g = G.copy()
        gatew = g_w.copy()
        attr = {(u, v): {"weight": round(random.uniform(0.01,1),2)} for (u, v) in G.edges()}
        nx.set_edge_attributes(g, attr)
        tot_g.append(g.subgraph(gatew))
        tot_graphs.append(g)
    return tot_graphs, tot_g
        
# def find_m_most_likely_graphs(Gs, m):
#     prob_of_graph = []
#     for i in range(len(Gs)):
#         prob_of_graph.append(np.prod([Gs[i].get_edge_data(*e)['weight'] for e in Gs[i].edges()]))
#     Gs_new = [prob for _,prob in sorted(zip(prob_of_graph, Gs))]
#     print(prob_of_graph)
#     return Gs_new[:m]

# G_m = find_m_most_likely_graphs(Gs, 2)

