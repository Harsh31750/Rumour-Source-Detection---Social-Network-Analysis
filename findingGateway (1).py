# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 18:47:34 2023

@author: barbh
"""

import networkx as nx
import networkx.algorithms.community as nx_comm
import matplotlib.pyplot as plt

# G = nx.Graph()
# G.add_edges_from([(0,1),(1,2),(2,0),(2,3),(3,4),(4,5),(3,5)])
# G = nx.karate_club_graph()


def gatewayNodes(G, ct):
    adj = [[] for i in range(G.number_of_nodes())]
    g_gate = G.copy()
    for node in G.nodes():
        flag = 0
        for n in g_gate[node]:
            if (ct[node] != ct[n]):
                flag = 1
                break
        if flag == 0:
            g_gate.remove_node(node)
    return g_gate

def candidateCluster(G, ct, node):
    clusterNodes = [i for i in range(len(ct)) if ct[i] == ct[node]]
    return G.subgraph(clusterNodes)

# plt.subplot(211)
# nx.draw_networkx(G)
# plt.subplot(212)
# nx.draw_networkx(gatewayNodes(G, ct))
# plt.show()

# labels =  nx.get_edge_attributes(G,'weight')
# values_G = [ct[node] for node in G.nodes()]
# values_gw = [ct[node] for node in gw]
# plt.subplot(211)
# nx.draw_spring(G, cmap = plt.get_cmap('jet'), node_color = values_G, node_size=1000, with_labels= True)
# plt.subplot(212)
# nx.draw_spring(gw, cmap = plt.get_cmap('jet'), node_color = values_gw, node_size=1000, with_labels= True)
# plt.show()