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
from firstStage import *
from secondStage import *

# Initialise the graph
G = nx.Graph()
gr = pd.read_csv('ER_500_5_giant_edge_list.csv')
edge = [(gr['Source'][i], gr['Target'][i])
        for i in range(0, len(gr['Source']))]
G.add_edges_from(edge)
node = max([max(x[0], x[1]) for x in edge])

clusters = community_louvain.best_partition(G)
g_w = gatewayNodes(G, clusters)

# Create multiple instances with varting edge weights
tot_graphs, tot_gw = createInstance(G, g_w)
time_of_diffusion = diffusion(G)

errors = []
for i in range(20):

    # First Stage
    cluster_nodes = FC(g_w, tot_gw, clusters, time_of_diffusion)

    # Second Stage
    cg = G.subgraph(cluster_nodes)
    tot_cg = [g.subgraph(cg) for g in tot_graphs]
    predicted_source = FS(G, cg, tot_cg)

    indices = [i for i, x in enumerate(
        list(time_of_diffusion.values())) if x == 0]
    actual_sources = [list(time_of_diffusion.keys())[index]
                      for index in indices]

    error = min([nx.shortest_path_length(G, actual_source, predicted_source)
                for actual_source in actual_sources])
    errors.append(error)


df = pd.DataFrame({'freq': errors})

(df.groupby('freq').size()/len(errors)).plot(kind='bar')
plt.show()

